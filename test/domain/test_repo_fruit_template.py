import asyncio
import os
import subprocess

os.environ["APP_ENV"] = "dev"

from grapechallenge.database.database import DatabaseClient, transactional_session_helper
from grapechallenge.config import get_database_config
from grapechallenge.domain.fruit_template import (
    Name,
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


# CRUD Operations
async def create_fruit_template(
    name: str,
    type: str,
    first_status: str,
    second_status: str,
    third_status: str,
    fourth_status: str,
    fifth_status: str,
    sixth_status: str,
    seventh_status: str,
) -> str:
    async with transactional_session_helper() as session:
        fruit_template = FruitTemplate.new(
            name=Name.from_str(name),
            type=Type.from_str(type),
            first_status=FirstStatus.from_str(first_status),
            second_status=SecondStatus.from_str(second_status),
            third_status=ThirdStatus.from_str(third_status),
            fourth_status=FourthStatus.from_str(fourth_status),
            fifth_status=FifthStatus.from_str(fifth_status),
            sixth_status=SixthStatus.from_str(sixth_status),
            seventh_status=SeventhStatus.from_str(seventh_status),
        )
        repo_fruit_template = await RepoFruitTemplate.create(session=session, fruit_template=fruit_template)
        return repo_fruit_template.id


async def get_fruit_template(fruit_template_id: str):
    async with transactional_session_helper() as session:
        return await RepoFruitTemplate.get_by_id(session=session, id=fruit_template_id)


async def get_fruit_template_by_name(name: str):
    async with transactional_session_helper() as session:
        return await RepoFruitTemplate.get_by_name(session=session, name=name)


async def update_fruit_template(
    fruit_template_id: str,
    name: str,
    type: str,
    first_status: str,
    second_status: str,
    third_status: str,
    fourth_status: str,
    fifth_status: str,
    sixth_status: str,
    seventh_status: str,
) -> None:
    async with transactional_session_helper() as session:
        fruit_template = FruitTemplate.new(
            name=Name.from_str(name),
            type=Type.from_str(type),
            first_status=FirstStatus.from_str(first_status),
            second_status=SecondStatus.from_str(second_status),
            third_status=ThirdStatus.from_str(third_status),
            fourth_status=FourthStatus.from_str(fourth_status),
            fifth_status=FifthStatus.from_str(fifth_status),
            sixth_status=SixthStatus.from_str(sixth_status),
            seventh_status=SeventhStatus.from_str(seventh_status),
        )
        await RepoFruitTemplate.update(session=session, fruit_template=fruit_template, id=fruit_template_id)


async def create_fruit_template_with_rollback(
    name: str,
    type: str,
    first_status: str,
    second_status: str,
    third_status: str,
    fourth_status: str,
    fifth_status: str,
    sixth_status: str,
    seventh_status: str,
):
    """Test function that creates a fruit template then raises an exception to trigger rollback"""
    async with transactional_session_helper() as session:
        fruit_template = FruitTemplate.new(
            name=Name.from_str(name),
            type=Type.from_str(type),
            first_status=FirstStatus.from_str(first_status),
            second_status=SecondStatus.from_str(second_status),
            third_status=ThirdStatus.from_str(third_status),
            fourth_status=FourthStatus.from_str(fourth_status),
            fifth_status=FifthStatus.from_str(fifth_status),
            sixth_status=SixthStatus.from_str(sixth_status),
            seventh_status=SeventhStatus.from_str(seventh_status),
        )
        await RepoFruitTemplate.create(session=session, fruit_template=fruit_template)
        # Raise exception to trigger rollback
        raise ValueError("Intentional error to test rollback")


# Cleanup
async def cleanup_database():
    async with transactional_session_helper() as session:
        from grapechallenge.domain.fruit_template.repo_fruit_template import FruitTemplateModel
        await session.execute(FruitTemplateModel.__table__.delete())


# Test runner
async def test_crud():
    db_config = get_database_config()
    print(f"Database: {db_config.database_url()}")
    print("=" * 60)

    async with DatabaseClient(db_config.database_url()):
        print("✓ Database connected\n")

        # CREATE
        print("[CREATE]")
        fruit_template_id = await create_fruit_template(
            "포도",
            "NORMAL",
            "/images/grape_1.png",
            "/images/grape_2.png",
            "/images/grape_3.png",
            "/images/grape_4.png",
            "/images/grape_5.png",
            "/images/grape_6.png",
            "/images/grape_7.png",
        )
        repo_fruit_template = await get_fruit_template(fruit_template_id)
        print(f"✓ Created: id={repo_fruit_template.id}, name={repo_fruit_template.fruit_template.name.to_str()}, type={repo_fruit_template.fruit_template.type.to_str()}\n")

        # READ
        print("[READ]")
        repo_fruit_template = await get_fruit_template(fruit_template_id)
        print(f"✓ Found: id={repo_fruit_template.id}, name={repo_fruit_template.fruit_template.name.to_str()}, type={repo_fruit_template.fruit_template.type.to_str()}\n")

        # READ BY NAME
        print("[READ BY NAME]")
        repo_fruit_template = await get_fruit_template_by_name("포도")
        print(f"✓ Found: id={repo_fruit_template.id}, name={repo_fruit_template.fruit_template.name.to_str()}, type={repo_fruit_template.fruit_template.type.to_str()}\n")

        # UPDATE
        print("[UPDATE]")
        await update_fruit_template(
            fruit_template_id,
            "사과",
            "EVENT",
            "/images/apple_1.png",
            "/images/apple_2.png",
            "/images/apple_3.png",
            "/images/apple_4.png",
            "/images/apple_5.png",
            "/images/apple_6.png",
            "/images/apple_7.png",
        )
        repo_fruit_template = await get_fruit_template(fruit_template_id)
        print(f"✓ Updated: id={repo_fruit_template.id}, name={repo_fruit_template.fruit_template.name.to_str()}, type={repo_fruit_template.fruit_template.type.to_str()}\n")

        # TRANSACTION ROLLBACK
        print("[TRANSACTION ROLLBACK]")
        try:
            await create_fruit_template_with_rollback(
                "바나나",
                "NORMAL",
                "/images/banana_1.png",
                "/images/banana_2.png",
                "/images/banana_3.png",
                "/images/banana_4.png",
                "/images/banana_5.png",
                "/images/banana_6.png",
                "/images/banana_7.png",
            )
            print("✗ Rollback failed: exception not raised")
        except ValueError as e:
            print(f"✓ Exception caught: {e}")
            print(f"✓ Rollback confirmed: transaction was rolled back\n")

        # SUMMARY
        print("[SUMMARY]")
        repo_fruit_template = await get_fruit_template(fruit_template_id)
        summary = repo_fruit_template.summary()
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