from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.infrastructure.security import get_password_hash, verify_password
from typing import Any, Dict, Optional, Union

from app.models import UserModel, UserSignIn, UserSignOut, BaseUser


class CRUDUser(CRUDBase[UserModel, UserSignIn, UserSignOut]):
    async def get_by_email(
            self,
            session: AsyncSession, *,
            email: Optional[str] = None,
            username: Optional[str] = None
    ) -> Optional[BaseUser]:
        query = select(UserModel).where(UserModel.email == email)
        if username is not None:
            query = query.where(UserModel.username == username)
        result = await session.execute(query)
        result = result.first()
        return result

    async def get_by_username(self, session: AsyncSession, *, username: str) -> Optional[BaseUser]:
        query = select(UserModel).where(UserModel.username == username)
        result = await session.execute(query)
        result = result.scalar()
        return result

    async def create(self, session: AsyncSession, *, obj_in: UserSignIn) -> UserSignIn:
        # role = "user" if obj_in.role is None else obj_in.role noqa

        db_obj = UserModel(
            email=obj_in.email, # noqa
            username=obj_in.username, # noqa
            password=get_password_hash(obj_in.password), # noqa
            full_name=obj_in.full_name, # noqa
            phone=obj_in.phone, # noqa
            document_number=obj_in.document_number # noqa


        )
        session.add(db_obj)
        await session.flush()
        return db_obj

    async def update(
        self, session: AsyncSession, *, db_obj: UserModel, obj_in: Union[UserSignIn, Dict[str, Any]]
    ) -> UserSignIn:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["password"] = hashed_password
        return await super().update(session, db_obj=db_obj, obj_in=update_data)

    async def authenticate(self, session: AsyncSession, *, username: str, password: str) -> Optional[UserSignIn]:
        user: UserModel = await self.get_by_username(session, username=username)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user
    
    
user_controller = CRUDUser(UserModel)
