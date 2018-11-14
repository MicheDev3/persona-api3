from src.middleware.auth import *
from src.middleware.session import *
from src.middleware.validator import *


__all__ = ['middleware']

middleware = [AuthManager(), ValidatorManager(), SessionManager()]
