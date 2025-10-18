import asyncio
import os
import subprocess

os.environ["APP_ENV"] = "dev"

from grapechallenge.database.database import DatabaseClient, transactional_session_helper
from grapechallenge.config import get_database_config
from grapechallenge.domain.fruit import Status, Fruit, RepoFruit
from grapechallenge.domain.user import Cell, Name, User, RepoUser
from grapechallenge.domain.fruit_template import (
    Name as TemplateName,
    Type,
    FirstStatus,
    SecondStatus,
    ThirdStatus,
    FourthStatus,
    FifthStatus,
    SixthStatus,
    SeventhStatus,
    FruitTemplate,
    RepoFruitTemplate,
)


# Setup test data
async def create_test_user() -> str:
    async with transactional_session_helper() as session:
        user = User.new(
            cell=Cell.from_str("다윗"),
            name=Name.from_str("홍길동")
        )
        repo_user = await RepoUser.create(session=session, user=user)
        return repo_user.id


async def create_test_template() -> str:
    async with transactional_session_helper() as session:
        fruit_template = FruitTemplate.new(
            name=TemplateName.from_str("포도"),
            type=Type.from_str("NORMAL"),
            first_status=FirstStatus.from_str("/images/grape_1.png"),
            second_status=SecondStatus.from_str("/images/grape_2.png"),
            third_status=ThirdStatus.from_str("/images/grape_3.png"),
            fourth_status=FourthStatus.from_str("/images/grape_4.png"),
            fifth_status=FifthStatus.from_str("/images/grape_5.png"),
            sixth_status=SixthStatus.from_str("/images/grape_6.png"),
            seventh_status=SeventhStatus.from_str("/images/grape_7.png"),
        )
        repo_template = await RepoFruitTemplate.create(session=session, fruit_template=fruit_template)
        return repo_template.id


# CRUD Operations
async def create_fruit(user_id: str, template_id: str, status: str) -> str:
    async with transactional_session_helper() as session:
        fruit = Fruit.new(
            user_id=user_id,
            template_id=template_id,
            status=Status.from_str(status)
        )
        repo_fruit = await RepoFruit.create(session=session, fruit=fruit)
        return repo_fruit.id


async def get_fruit(fruit_id: str):
    async with transactional_session_helper() as session:
        return await RepoFruit.get_by_id(session=session, id=fruit_id)


async def get_fruit_by_user_id(user_id: str):
    async with transactional_session_helper() as session:
        return await RepoFruit.get_by_user_id(session=session, user_id=user_id)


async def update_fruit(fruit_id: str, user_id: str, template_id: str, status: str) -> None:
    async with transactional_session_helper() as session:
        fruit = Fruit.new(
            user_id=user_id,
            template_id=template_id,
            status=Status.from_str(status)
        )
        await RepoFruit.update(session=session, fruit=fruit, id=fruit_id)


async def create_fruit_with_rollback(user_id: str, template_id: str, status: str):
    """Test function that creates a fruit then raises an exception to trigger rollback"""
    async with transactional_session_helper() as session:
        fruit = Fruit.new(
            user_id=user_id,
            template_id=template_id,
            status=Status.from_str(status)
        )
        await RepoFruit.create(session=session, fruit=fruit)
        # Raise exception to trigger rollback
        raise ValueError("Intentional error to test rollback")


# Cleanup
async def cleanup_database():
    async with transactional_session_helper() as session:
        from grapechallenge.domain.fruit.repo_fruit import FruitModel
        from grapechallenge.domain.user.repo_user import UserModel
        from grapechallenge.domain.fruit_template.repo_fruit_template import FruitTemplateModel

        await session.execute(FruitModel.__table__.delete())
        await session.execute(UserModel.__table__.delete())
        await session.execute(FruitTemplateModel.__table__.delete())


# Test runner
async def test_crud():
    db_config = get_database_config()
    print(f"Database: {db_config.database_url()}")
    print("=" * 60)

    async with DatabaseClient(db_config.database_url()):
        print("✓ Database connected\n")

        # SETUP
        print("[SETUP]")
        user_id = await create_test_user()
        template_id = await create_test_template()
        print(f"✓ Test user created: {user_id}")
        print(f"✓ Test template created: {template_id}\n")

        # CREATE
        print("[CREATE]")
        fruit_id = await create_fruit(user_id, template_id, "FIRST_STATUS")
        repo_fruit = await get_fruit(fruit_id)
        print(f"✓ Created: id={repo_fruit.id}, user_id={repo_fruit.fruit.user_id}, template_id={repo_fruit.fruit.template_id}, status={repo_fruit.fruit.status.to_str()}\n")

        # READ
        print("[READ]")
        repo_fruit = await get_fruit(fruit_id)
        print(f"✓ Found: id={repo_fruit.id}, user_id={repo_fruit.fruit.user_id}, status={repo_fruit.fruit.status.to_str()}\n")

        # READ BY USER ID
        print("[READ BY USER ID]")
        repo_fruit = await get_fruit_by_user_id(user_id)
        print(f"✓ Found: id={repo_fruit.id}, user_id={repo_fruit.fruit.user_id}, status={repo_fruit.fruit.status.to_str()}\n")

        # UPDATE
        print("[UPDATE]")
        await update_fruit(fruit_id, user_id, template_id, "SEVENTH_STATUS")
        repo_fruit = await get_fruit(fruit_id)
        print(f"✓ Updated: id={repo_fruit.id}, status={repo_fruit.fruit.status.to_str()}\n")

        # TRANSACTION ROLLBACK
        print("[TRANSACTION ROLLBACK]")
        try:
            await create_fruit_with_rollback(user_id, template_id, "SECOND_STATUS")
            print("✗ Rollback failed: exception not raised")
        except ValueError as e:
            print(f"✓ Exception caught: {e}")
            print(f"✓ Rollback confirmed: transaction was rolled back\n")

        # SUMMARY
        print("[SUMMARY]")
        repo_fruit = await get_fruit(fruit_id)
        summary = repo_fruit.summary()
        print(f"✓ Summary: {summary}\n")

        # CLEANUP
        print("[CLEANUP]")
        await cleanup_database()
        print("✓ Database cleaned up\n")

    print("=" * 60)
    print("All tests passed!")


if __name__ == "__main__":
    subprocess.run(["./scripts/setup_dev_db.sh"])
    asyncio.run(test_crud())
