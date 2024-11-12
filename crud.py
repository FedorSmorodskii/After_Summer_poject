import asyncio

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.models import db_helper, User, Post, Profile


# Создаем пользователя
async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print(f'User {username} created')
    return user


# Находим пользователя по имени
async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stnt = select(User).where(User.username == username)
    # result: Result = await session.execute(stnt)
    # user: User | None = result.scalar_one_or_none()
    user = await session.scalar(stnt)
    print(f'User {username, user} retrieved')
    return user


# Создаем профиль пользователя
async def create_user_profile(session: AsyncSession, user_id: int, first_name: str | None = None, last_name: str | None = None,) -> Profile:
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name
    )
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession):
    stnt = select(User).options(joinedload(User.profile)).order_by(User.id)
    users = await session.scalars(stnt)
    for user in users:
        print(user)
        print(user.profile.first_name)


async def create_posts(session: AsyncSession, user_id: int, *posts_titles: str) -> list[Post]:
    posts = [
        Post(title=title, user_id=user_id)
        for title in posts_titles
    ]
    session.add_all(posts)
    await session.commit()
    print(f'Posts created for user {user_id}')
    return posts


async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session, 'user1')
        # await create_user(session, 'user2')
        # await get_user_by_username(session, 'user1')
        user_1 = await get_user_by_username(session, 'user1')
        user_2 = await get_user_by_username(session, 'user2')
        # await create_user_profile(
        #     session = session,
        #     user_id = user_1.id,
        #     first_name = 'John',
        #     last_name = 'Doe'
        # )
        # await create_user_profile(
        #     session=session,
        #     user_id=user_2.id,
        #     first_name='Sam',
        #     last_name='White'
        # )
        # await show_users_with_profiles(session=session)
        await create_posts(session, user_1.id, "SQLA 2.0", "SQLA Joins")
        await create_posts(session, user_2.id, "SQLAlchemy history", "SQLAlchemy creators")


if __name__ == '__main__':
    asyncio.run(main())
