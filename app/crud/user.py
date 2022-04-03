from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.infrastructure.security import get_password_hash, verify_password
from typing import Any, Dict, Optional, Union

from app.models import User, UserSignIn, UserSignOut, BaseUser


class CRUDUser(CRUDBase[User, UserSignIn, UserSignOut]):
    async def get_by_email(self, session: AsyncSession, *, email: str, username: Optional[str] = None) -> Optional[BaseUser]:
        query = select(User).where(User.email == email)
        if username is not None:
            query = query.where(User.username == username)
        result = await session.execute(query)
        result = result.scalars().one()
        return result

    async def get_by_username(self, session: AsyncSession, *, username: str) -> Optional[BaseUser]:
        query = select(User).where(User.username == username)
        result = await session.execute(query)
        result = result.scalars().one()
        return result

    async def create(self, session: AsyncSession, *, obj_in: UserSignIn) -> UserSignIn:
        # role = "user" if obj_in.role is None else obj_in.role noqa

        db_obj = User(
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
        self, session: AsyncSession, *, db_obj: User, obj_in: Union[UserSignIn, Dict[str, Any]]
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

    async def authenticate(self, session: AsyncSession, *, email: str, password: str) -> Optional[UserSignIn]:
        user: User = await self.get_by_email(session, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user
    
    
user_controller = CRUDUser(User)
