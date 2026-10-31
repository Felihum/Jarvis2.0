from dataclasses import dataclass
from enum import Enum

class ConversationRoleEnum(Enum):
    USER = 'user'
    ASSISTANT = 'assistant'
    SYSTEM = 'system'

@dataclass
class ConversationMessage:
    role: ConversationRoleEnum
    content: str