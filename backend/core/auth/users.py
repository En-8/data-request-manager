import uuid

from fastapi_users import FastAPIUsers

from .backend import auth_backend
from .manager import get_user_manager
from .models import User

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

# Dependency for getting the current active user
current_active_user = fastapi_users.current_user(active=True)
