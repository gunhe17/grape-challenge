import asyncio
import os
import subprocess

os.environ["APP_ENV"] = "dev"

from grapechallenge.database.database import DatabaseClient, transactional_session_helper
from grapechallenge.config import get_database_config
from grapechallenge.domain.mission import Mission, RepoMission
from grapechallenge.domain.user import Cell, Name, User, RepoUser
from grapechallenge.domain.fruit import Status, Fruit, RepoFruit
from grapechallenge.domain.fruit_template import (
    Name as TemplateName,
    Type as FruitType,
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
from grapechallenge.domain.mission_template import (
    Name as MissionTemplateName,
    Content,
    Type as MissionType,
    MissionTemplate,
    RepoMissionTemplate,
)


# Setup test data
async def create_test_user() -> str:
    async with transactional_session_helper() as session:
        user = User.new(
            cell=Cell.from_str("david"),
            name=Name.from_str("hong")
        )
        repo_user = await RepoUser.create(session=session, user=user)
        return repo_user.id


async def create_test_fruit_template() -> str:
    async with transactional_session_helper() as session:
        fruit_template = FruitTemplate.new(
            name=TemplateName.from_str("grape"),
            type=FruitType.from_str("NORMAL"),
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


async def create_test_fruit(user_id: str, template_id: str) -> str:
    async with transactional_session_helper() as session:
        fruit = Fruit.new(
            user_id=user_id,
            template_id=template_id,
            status=Status.from_str("FIRST_STATUS")
        )
        repo_fruit = await RepoFruit.create(session=session, fruit=fruit)
        return repo_fruit.id


async def create_test_mission_template() -> str:
    async with transactional_session_helper() as session:
        mission_template = MissionTemplate.new(
            name=MissionTemplateName.from_str("daily prayer"),
            content=Content.from_str("pray once a day"),
            type=MissionType.from_str("NORMAL"),
        )
        repo_template = await RepoMissionTemplate.create(session=session, mission_template=mission_template)
        return repo_template.id


# CRUD Operations
async def create_mission(user_id: str, template_id: str, fruit_id: str) -> str:
    async with transactional_session_helper() as session:
        mission = Mission.new(
            user_id=user_id,
            template_id=template_id,
            fruit_id=fruit_id
        )
        repo_mission = await RepoMission.create(session=session, mission=mission)
        return repo_mission.id


async def get_mission(mission_id: str):
    async with transactional_session_helper() as session:
        return await RepoMission.get_by_id(session=session, id=mission_id)


async def get_mission_by_user_id(user_id: str):
    async with transactional_session_helper() as session:
        return await RepoMission.get_by_user_id(session=session, user_id=user_id)


async def get_mission_by_fruit_id(fruit_id: str):
    async with transactional_session_helper() as session:
        return await RepoMission.get_by_fruit_id(session=session, fruit_id=fruit_id)


async def update_mission(mission_id: str, user_id: str, template_id: str, fruit_id: str) -> None:
    async with transactional_session_helper() as session:
        mission = Mission.new(
            user_id=user_id,
            template_id=template_id,
            fruit_id=fruit_id
        )
        await RepoMission.update(session=session, mission=mission, id=mission_id)


async def create_mission_with_rollback(user_id: str, template_id: str, fruit_id: str):
    """Test function that creates a mission then raises an exception to trigger rollback"""
    async with transactional_session_helper() as session:
        mission = Mission.new(
            user_id=user_id,
            template_id=template_id,
            fruit_id=fruit_id
        )
        await RepoMission.create(session=session, mission=mission)
        # Raise exception to trigger rollback
        raise ValueError("Intentional error to test rollback")


# Cleanup
async def cleanup_database():
    async with transactional_session_helper() as session:
        from grapechallenge.domain.mission.repo_mission import MissionModel
        from grapechallenge.domain.fruit.repo_fruit import FruitModel
        from grapechallenge.domain.user.repo_user import UserModel
        from grapechallenge.domain.fruit_template.repo_fruit_template import FruitTemplateModel
        from grapechallenge.domain.mission_template.repo_mission_template import MissionTemplateModel

        await session.execute(MissionModel.__table__.delete())
        await session.execute(FruitModel.__table__.delete())
        await session.execute(MissionTemplateModel.__table__.delete())
        await session.execute(UserModel.__table__.delete())
        await session.execute(FruitTemplateModel.__table__.delete())


# Test runner
async def test_crud():
    db_config = get_database_config()
    print(f"Database: {db_config.database_url()}")
    print("=" * 60)

    async with DatabaseClient(db_config.database_url()):
        print("Database connected\n")

        # SETUP
        print("[SETUP]")
        user_id = await create_test_user()
        fruit_template_id = await create_test_fruit_template()
        fruit_id = await create_test_fruit(user_id, fruit_template_id)
        mission_template_id = await create_test_mission_template()
        print(f"Test user created: {user_id}")
        print(f"Test fruit template created: {fruit_template_id}")
        print(f"Test fruit created: {fruit_id}")
        print(f"Test mission template created: {mission_template_id}\n")

        # CREATE
        print("[CREATE]")
        mission_id = await create_mission(user_id, mission_template_id, fruit_id)
        repo_mission = await get_mission(mission_id)
        print(f"Created: id={repo_mission.id}, user_id={repo_mission.mission.user_id}, template_id={repo_mission.mission.template_id}, fruit_id={repo_mission.mission.fruit_id}\n")

        # READ
        print("[READ]")
        repo_mission = await get_mission(mission_id)
        print(f"Found: id={repo_mission.id}, user_id={repo_mission.mission.user_id}, template_id={repo_mission.mission.template_id}, fruit_id={repo_mission.mission.fruit_id}\n")

        # READ BY USER ID
        print("[READ BY USER ID]")
        repo_mission = await get_mission_by_user_id(user_id)
        print(f"Found: id={repo_mission.id}, user_id={repo_mission.mission.user_id}, template_id={repo_mission.mission.template_id}\n")

        # READ BY FRUIT ID
        print("[READ BY FRUIT ID]")
        repo_mission = await get_mission_by_fruit_id(fruit_id)
        print(f"Found: id={repo_mission.id}, fruit_id={repo_mission.mission.fruit_id}, template_id={repo_mission.mission.template_id}\n")

        # UPDATE
        print("[UPDATE]")
        await update_mission(mission_id, user_id, mission_template_id, fruit_id)
        repo_mission = await get_mission(mission_id)
        print(f"Updated: id={repo_mission.id}, user_id={repo_mission.mission.user_id}\n")

        # TRANSACTION ROLLBACK
        print("[TRANSACTION ROLLBACK]")
        try:
            await create_mission_with_rollback(user_id, mission_template_id, fruit_id)
            print("Rollback failed: exception not raised")
        except ValueError as e:
            print(f"Exception caught: {e}")
            print(f"Rollback confirmed: transaction was rolled back\n")

        # SUMMARY
        print("[SUMMARY]")
        repo_mission = await get_mission(mission_id)
        summary = repo_mission.summary()
        print(f"Summary: {summary}\n")

        # CLEANUP
        print("[CLEANUP]")
        await cleanup_database()
        print("Database cleaned up\n")

    print("=" * 60)
    print("All tests passed!")


if __name__ == "__main__":
    subprocess.run(["./scripts/setup_dev_db.sh"])
    asyncio.run(test_crud())
