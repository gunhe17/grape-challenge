from .auth import router as auth_router
from .users import router as users_router
from .sessions import router as sessions_router
from .fruits import router as fruits_router
from .missions import router as missions_router
from .web import router as web_router

__all__ = [
    'auth_router',
    'users_router',
    'sessions_router',
    'fruits_router',
    'missions_router',
    'web_router'
]