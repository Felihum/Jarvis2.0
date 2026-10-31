import json
import os
import time
from threading import Semaphore
from adapters.llm.llm_adapter import LLMAdapter
from adapters.llm.ollama_adapter import OllamaAdapter
from adapters.llm.openai_adapter import OpenAIAdapter
from adapters.llm.gemma_adapter import GemmaAdapter
from config import NPC_CONFIGS, DEFAULT_NPC
from services.bert_service import BertService

OLLAMA_DEFAULT_MODEL = os.environ.get("OPENAI_MODEL", "gpt-6-luna")

MAX_CONCURRENT_LLM = 1
llm_semaphore = Semaphore(MAX_CONCURRENT_LLM)

class LLMService:
    def __init__(self):
        self.bert_service = BertService()
        self.intention_verifier = OpenAIAdapter()

    def generate(self, messages: list[dict], filenames: list | None, model: str, adapter: LLMAdapter):
        with llm_semaphore:

            stream = adapter.stream_chat(
                messages=messages,
                model=model,
            )

            yield f"data: {json.dumps({'type': 'files', 'filenames': filenames})}\n\n"

            first_token_sent = False

            for token in stream:

                if not first_token_sent:
                    first_token_sent = True

                    yield (
                        f"data: {json.dumps({'type': 'metric', 'name': 'first_token_at', 'value': time.time()})}\n\n"
                    )

                print(token, end="", flush=True)

                yield (
                    f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"
                )

            yield f"data: {json.dumps({'type': 'done'})}\n\n"

    def query(self, user_query: list[dict], npc_id: str = DEFAULT_NPC):
        if not user_query:
            yield f"data: {json.dumps({'type': 'error', 'content': 'Campo query é obrigatório.'})}\n\n"
            return

        npc_config = NPC_CONFIGS.get(npc_id, NPC_CONFIGS[DEFAULT_NPC])

        user_content = user_query[-1].get("content", "").strip()

        intention = self.analyse_intention(user_query)

        if npc_config.get("usa_rag") and intention["intention"] == "consulta":
            query_results = self.bert_service.search_query_fast(
                query=intention["context"],
                chunks_num=npc_config.get("top_chunks", 4),
            )

            contexts = query_results.get("context", [])
            filenames = query_results.get("filenames", [])
            titles = query_results.get("titles", [])
            best_distance = query_results.get("best_distance")

            llm_adapter = OpenAIAdapter()
            context_text = ""

            for context in contexts:
                title = context.get("title", "")
                filename = context.get("filename", "")
                page = context.get("page", "")
                chunk = context.get("chunk", "")

                context_text += f"[Fonte: {title} | Arquivo: {filename} | Página: {page}\n"
                context_text += f"{chunk}\n\n"

            prompt = f"""
                {npc_config["system_prompt"]}

                ### CONTEXTO RECUPERADO DA BASE:
                {context_text}

                ### DISSERTAÇÕES/TÍTULOS ENCONTRADOS:
                {", ".join(titles)}

                ### PERGUNTA DO USUÁRIO:
                {user_content}

                ### REGRAS DE RESPOSTA:
                - Responda em português do Brasil.
                - Seja claro, natural e adequado para uma NPC em realidade virtual.
                - Responda de forma objetiva, preferencialmente em até 3 parágrafos.
                - Use apenas o contexto recuperado quando falar das dissertações.
                - Cite os títulos ou arquivos encontrados quando forem relevantes.
                - Se o contexto não for suficiente, diga que não encontrou informação suficiente na base.
                - Não invente autores, títulos, páginas ou arquivos.
                - Quando houver dissertações, informe que o usuário pode clicar nelas para ver mais detalhes.
            """

            messages = [
                {"role": "system", "content": npc_config["system_prompt"]},
                {"role": "user", "content": prompt}
            ]

            yield from self.generate(
                messages=messages,
                filenames=filenames,
                model=os.environ.get("OPENAI_MODEL", "gpt-6-luna"),
                adapter=llm_adapter
            )

        # Se não achar contexto bom, responde como conversa normal da NPC.
        else:
            llm_adapter = OpenAIAdapter()
            messages = [
                {"role": "system", "content": npc_config["system_prompt"]}
            ] + user_query

            yield from self.generate(
                messages=messages,
                filenames=None,
                model=os.environ.get("OPENAI_MODEL", "gpt-6-luna"),
                adapter=llm_adapter
            )

    def analyse_intention(self, messages) -> dict:
        llm_identifier = OpenAIAdapter()

        response = llm_identifier.single_response(
            message=messages,
            system="""
                # ROLE
                Você é um classificador de intenções especializado em filtragem de consultas para um banco de dados de dissertações de mestrado.

                # TASK
                Analíse a entrada do usuário e determine se ele deseja realizar uma consulta de dissertações sobre um assunto acadêmico.

                # REGRAS CRÍTICAS
                1. Para identificar se o usuário deseja realizar uma consulta, analíse todo o contexto, buscando entender se o rumo da conversa leva a essa intenção.
                2. Se o assunto for irrelevante ou o usuário não pedir uma consulta de forma clara, a intenção deve ser "none".
                3. SAÍDA RESTRITA: Responda exclusivamente em formato JSON. Não adicione saudações, explicações ou qualquer texto fora do bloco JSON.

                # FORMATO DE SAÍDA
                {
                "intention": "consulta" | "none",
                "context": "assunto extraído ou null"
                }

                # EXEMPLOS
                - Usuário: "Gostaria de ver dissertações sobre redes neurais."
                Resposta: {"intention": "consulta", "context": "redes neurais"}

                - Usuário: "Estou trabalhando em um projeto de pesquisa sobre aprendizado de máquina."
                - Assistente: "Que legal! Você gostaria de ver dissertações relacionadas a aprendizado de máquina?"
                - Usuário: "Sim."
                Resposta: {"intention": "consulta", "context": "aprendizado de máquina"}

                - Usuário: "Como está o clima hoje?"
                Resposta: {"intention": "none", "context": null}

                - Usuário: "Quero pesquisar trabalhos sobre Machado de Assis."
                Resposta: {"intention": "consulta", "context": "Machado de Assis"}
            """,
            model=os.environ.get("OPENAI_MODEL", "gpt-6-luna"),
            format={
                "type": "json_schema",
                "name": "intention_response",
                "schema": {
                    "type": "object",
                    "properties": {
                        "intention": {
                            "type": "string"
                        },
                        "context": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "intention",
                        "context"
                    ],
                    "additionalProperties": False
                }
            }
        )

        return json.loads(response.output_text)

    def deep_analysing(self, filename: str, context: list[dict]):
        chunks, metadatas = self.bert_service.deep_search(filename=filename)

        messages = [
            {
                "role": "user",
                "content": "Analise os textos fornecidos a seguir e, a partir desse contexto, tire as dúvidas do usuário."
            }
        ]

        for i, chunk in enumerate(chunks):
            page = metadatas[i].get("page") if i < len(metadatas) else ""
            messages.append({
                "role": "user",
                "content": f"Página {page}\n{chunk}"
            })

        messages.extend(context)

        yield from self.generate(
            messages=messages,
            filenames=None,
            model=OLLAMA_DEFAULT_MODEL
        )
