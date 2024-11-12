import asyncio

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

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


# Показываем всех пользователей с профилями
async def show_users_with_profiles(session: AsyncSession):
    stmt = select(User).options(
        joinedload(User.profile)  # Один к одному
    ).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        print(user.profile.first_name)


# Создаем посты для пользователя
async def create_posts(session: AsyncSession, user_id: int, *posts_titles: str) -> list[Post]:
    posts = [
        Post(title=title, user_id=user_id)
        for title in posts_titles
    ]
    session.add_all(posts)
    await session.commit()
    print(f'Posts created for user {user_id}')
    return posts


# Показываем всех пользователей с постами
async def get_users_with_posts(session: AsyncSession) -> list[User]:
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    stmt = select(User).options(
        # joinedload(User.posts),
        selectinload(User.posts)  # Один ко многим
    ).order_by(User.id)
    # users = await session.scalars(stmt)
    result: Result = await session.execute(stmt)
    # users = result.unique().scalars()
    users = result.scalars()

    # for user in users.unique():
    for user in users:
        print("******" * 10)
        print(user)
        for post in user.posts:
            print(post)


async def get_posts_with_authors(session: AsyncSession) -> list[Post]:
    stmt = select(Post).options(
        joinedload(Post.user)  # Один к одному
    ).order_by(Post.id)
    posts = await session.scalars(stmt)
    for post in posts:
        print("post", post)
        print("author", post.user)


async def get_users_with_posts_and_profiles(session: AsyncSession) -> list[User]:
    stmt = (select(User)
        .options(
        joinedload(User.profile),  # Один к одному
        selectinload(User.posts)  # Один ко многим
    ).order_by(User.id))

    users = await session.scalars(stmt)

    # for user in users.unique():
    for user in users:
        print("******" * 10)
        print(user, user.profile and user.profile.first_name)
        for post in user.posts:
            print("-", post)


async def get_profiles_with_users_and_users_with_posts(session: AsyncSession) -> list[Profile]:
    stmt = (select(Profile)
        .join(Profile.user)  # Для будущей фильтрации по имени например
        .options(
        joinedload(Profile.user).selectinload(User.posts)  # Для подгрузки данных

        )
        .where(User.username == 'user1')
        .order_by(Profile.id)
    )

    profiles = await session.scalars(stmt)

    # for profile in profiles.unique():
    for profile in profiles:
        print("******" * 10)
        print(profile.first_name, profile.user)
        print(profile.user.posts)


async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session, 'user1')
        # await create_user(session, 'Alice')
        # await get_user_by_username(session, 'user1')
        # user_1 = await get_user_by_username(session, 'user1')
        # user_2 = await get_user_by_username(session, 'user2')
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
        # await create_posts(session, user_1.id, "SQLA 2.0", "SQLA Joins")
        # await create_posts(session, user_2.id, "SQLAlchemy history", "SQLAlchemy creators")
        # await get_users_with_posts(session=session)
        # await get_posts_with_authors(session=session)
        # await get_users_with_posts_and_profiles(session=session)
        await get_profiles_with_users_and_users_with_posts(session=session)
if __name__ == '__main__':
    asyncio.run(main())
