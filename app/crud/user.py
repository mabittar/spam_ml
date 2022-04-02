from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.infrastructure.security import get_password_hash, verify_password
from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session

from app.models import User, UserSignIn, UserSignOut, BaseUser


class CRUDUser(CRUDBase[User, UserSignIn, UserSignOut]):
    async def get_by_email(self, db: Session, *, email: str) -> Optional[BaseUser]:
        query = select(BaseUser).filter(BaseUser.email == email).first()
        result = await db.execute(query)
        return result

    async def create(self, db: AsyncSession, *, obj_in: UserSignIn) -> UserSignIn:
        role = "user" if obj_in.role is None else obj_in.role
        db_obj = UserSignIn(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            phone=obj_in.phone,
            role=role,
            document_number=obj_in.document_number

        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: UserSignIn, obj_in: Union[UserSignIn, Dict[str, Any]]
    ) -> UserSignIn:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["password"] = hashed_password
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def authenticate(self, db: AsyncSession, *, email: str, password: str) -> Optional[UserSignIn]:
        user: User = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user
    
    
user_controller = CRUDUser(User)