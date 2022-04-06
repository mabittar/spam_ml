from .root import router as root
from .health_check import router as health_check
from .user import router as user
from .login import router as login
from .predict_spam import router as spam


endpoints_list = [
    root,
    health_check,
    user,
    login,
    spam
]

