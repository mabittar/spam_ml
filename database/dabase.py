import crud
from sqlalchemy.orm import Session
from crud.user.user import user
from settings import FIRST_SUPERUSER, FIRST_SUPERUSER_PASSWORD, FIRST_SUPERUSER_EMAIL
from models.user import UserSignIn


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = crud.user.get_by_email(db, email=FIRST_SUPERUSER)  # type: ignore
    if not user:
        user_in = UserSignIn(
            full_name=FIRST_SUPERUSER,  # type: ignore
            password=FIRST_SUPERUSER_PASSWORD,
            role="super admin",
            email=FIRST_SUPERUSER_EMAIL  # type: ignore
            
        )
        user = crud.user.create(db, obj_in=user_in)  # type: ignore 