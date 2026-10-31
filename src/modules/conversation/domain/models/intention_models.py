from dataclasses import dataclass

@dataclass
class IntentionResponse:
    intention: str
    context: str