from src.tables import User, TypeUser
from src.database import async_session
from asyncio import run
from uuid import uuid4


async def create_user_model_context():
    async with async_session() as session:
        types_user = [
            TypeUser(
                name="admin",
                description="admin"
            ),
            TypeUser(
                name="user",
                description="user"
            )
        ]

        user = User(
            login="admin",
            id_type=1
        )
        user.password = "admin"
        session.add_all(types_user)
        session.add(user)

        await session.commit()


async def main():
    await create_user_model_context()


run(main())