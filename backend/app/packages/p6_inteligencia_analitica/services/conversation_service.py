from uuid import UUID

from sqlalchemy.orm import Session

from app.packages.p6_inteligencia_analitica.models.conversation import Conversation
from app.packages.p6_inteligencia_analitica.models.conversation_message import ConversationMessage


MAX_CONTEXT_MESSAGES = 2
MAX_CONTEXT_CHARS = 800


def get_or_create_conversation(db: Session, user_id: UUID) -> Conversation:
    conversation = db.query(Conversation).filter(Conversation.user_id == user_id).first()
    if conversation is None:
        conversation = Conversation(user_id=user_id)
        db.add(conversation)
        db.flush()
    return conversation


def load_recent_messages(db: Session, conversation: Conversation) -> list[ConversationMessage]:
    messages = (
        db.query(ConversationMessage)
        .filter(ConversationMessage.conversation_id == conversation.id)
        .order_by(ConversationMessage.created_at.desc(), ConversationMessage.id.desc())
        .limit(MAX_CONTEXT_MESSAGES)
        .all()
    )
    messages.reverse()
    selected: list[ConversationMessage] = []
    chars = 0
    for message in reversed(messages):
        if chars + len(message.content) > MAX_CONTEXT_CHARS:
            break
        selected.append(message)
        chars += len(message.content)
    selected.reverse()
    return selected


def list_messages(db: Session, user_id: UUID) -> list[ConversationMessage]:
    conversation = db.query(Conversation).filter(Conversation.user_id == user_id).first()
    if conversation is None:
        return []
    return (
        db.query(ConversationMessage)
        .filter(ConversationMessage.conversation_id == conversation.id)
        .order_by(ConversationMessage.created_at.asc(), ConversationMessage.id.asc())
        .all()
    )


def append_message(
    db: Session,
    conversation: Conversation,
    role: str,
    content: str,
    message_data: dict | None = None,
) -> ConversationMessage:
    message = ConversationMessage(
        conversation_id=conversation.id,
        role=role,
        content=content,
        message_data=message_data,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def clear_conversation(db: Session, user_id: UUID) -> None:
    conversation = db.query(Conversation).filter(Conversation.user_id == user_id).first()
    if conversation is not None:
        db.delete(conversation)
        db.commit()
