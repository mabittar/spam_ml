from infrastructure.security import get_password_hash, verify_password
from typing import Any, Dict, Optional, Union
from crud.base import CRUDBase
from sqlalchemy.orm import Session

from models.user import BaseUser, UserSignIn, UserSignOut, User


class CRUDUser(CRUDBase[User, UserSignIn, UserSignOut]):
    async def get_by_email(self, db: Session, *, email: str) -> Optional[BaseUser]:
        return await db.query(BaseUser).filter(BaseUser.email == email).first()

    async def create(self, db: Session, *, obj_in: UserSignIn) -> UserSignIn:
        db_obj = UserSignIn(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: Session, *, db_obj: UserSignIn, obj_in: Union[UserSignIn, Dict[str, Any]]
    ) -> UserSignIn:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    async def authenticate(self, db: Session, *, email: str, password: str) -> Optional[UserSignIn]:
        user: User = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user
    
    
user = CRUDUser(User)
