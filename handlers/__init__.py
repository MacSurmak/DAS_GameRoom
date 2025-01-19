from .admin import admin_router
from .messages import messages_router
from .commands import commands_router
from .dialog import dialog

__all__ = [
    "admin_router",
    "messages_router",
    "commands_router",
    "dialog"
]
