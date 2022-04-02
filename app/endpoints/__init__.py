from .root import router as root
from .health_check import router as health_check
from .user import router as user
from .login import router as login


enpoints_list = [
    root,
    health_check,
    user,
    login
]

