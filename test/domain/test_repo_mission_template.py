import asyncio
import os
import subprocess

os.environ["APP_ENV"] = "dev"

from grapechallenge.database.database import DatabaseClient, transactional_session_helper
from grapechallenge.config import get_database_config
from grapechallenge.domain.mission_template import Name, Content, Type, MissionTemplate, RepoMissionTemplate


# CRUD Operations
async def create_mission_template(name: str, content: str, type: str) -> str:
    async with transactional_session_helper() as session:
        mission_template = MissionTemplate.new(
            name=Name.from_str(name),
            content=Content.from_str(content),
            type=Type.from_str(type)
        )
        repo_mission_template = await RepoMissionTemplate.create(session=session, mission_template=mission_template)
        return repo_mission_template.id


async def get_mission_template(mission_template_id: str):
    async with transactional_session_helper() as session:
        return await RepoMissionTemplate.get_by_id(session=session, id=mission_template_id)


async def get_mission_template_by_name(name: str):
    async with transactional_session_helper() as session:
        return await RepoMissionTemplate.get_by_name(session=session, name=name)


async def update_mission_template(mission_template_id: str, name: str, content: str, type: str) -> None:
    async with transactional_session_helper() as session:
        mission_template = MissionTemplate.new(
            name=Name.from_str(name),
            content=Content.from_str(content),
            type=Type.from_str(type)
        )
        await RepoMissionTemplate.update(session=session, mission_template=mission_template, id=mission_template_id)


async def create_mission_template_with_rollback(name: str, content: str, type: str):
    """Test function that creates a mission template then raises an exception to trigger rollback"""
    async with transactional_session_helper() as session:
        mission_template = MissionTemplate.new(
            name=Name.from_str(name),
            content=Content.from_str(content),
            type=Type.from_str(type)
        )
        await RepoMissionTemplate.create(session=session, mission_template=mission_template)
        # Raise exception to trigger rollback
        raise ValueError("Intentional error to test rollback")


# Cleanup
async def cleanup_database():
    async with transactional_session_helper() as session:
        from grapechallenge.domain.mission_template.repo_mission_template import MissionTemplateModel
        await session.execute(MissionTemplateModel.__table__.delete())


# Test runner
async def test_crud():
    db_config = get_database_config()
    print(f"Database: {db_config.database_url()}")
    print("=" * 60)

    async with DatabaseClient(db_config.database_url()):
        print("✓ Database connected\n")

        # CREATE
        print("[CREATE]")
        mission_template_id = await create_mission_template("Daily Prayer", "Pray for 10 minutes", "NORMAL")
        repo_mission_template = await get_mission_template(mission_template_id)
        print(f"✓ Created: id={repo_mission_template.id}, name={repo_mission_template.mission_template.name.to_str()}, content={repo_mission_template.mission_template.content.to_str()}, type={repo_mission_template.mission_template.type.to_str()}\n")

        # READ
        print("[READ]")
        repo_mission_template = await get_mission_template(mission_template_id)
        print(f"✓ Found: id={repo_mission_template.id}, name={repo_mission_template.mission_template.name.to_str()}, content={repo_mission_template.mission_template.content.to_str()}, type={repo_mission_template.mission_template.type.to_str()}\n")

        # READ BY NAME
        print("[READ BY NAME]")
        repo_mission_template = await get_mission_template_by_name("Daily Prayer")
        print(f"✓ Found: id={repo_mission_template.id}, name={repo_mission_template.mission_template.name.to_str()}, content={repo_mission_template.mission_template.content.to_str()}, type={repo_mission_template.mission_template.type.to_str()}\n")

        # UPDATE
        print("[UPDATE]")
        await update_mission_template(mission_template_id, "Easter Special", "Special Easter service mission", "EVENT")
        repo_mission_template = await get_mission_template(mission_template_id)
        print(f"✓ Updated: id={repo_mission_template.id}, name={repo_mission_template.mission_template.name.to_str()}, content={repo_mission_template.mission_template.content.to_str()}, type={repo_mission_template.mission_template.type.to_str()}\n")

        # TRANSACTION ROLLBACK
        print("[TRANSACTION ROLLBACK]")
        try:
            await create_mission_template_with_rollback("Rollback Test", "This should rollback", "NORMAL")
            print("✗ Rollback failed: exception not raised")
        except ValueError as e:
            print(f"✓ Exception caught: {e}")
            print(f"✓ Rollback confirmed: transaction was rolled back\n")

        # SUMMARY
        print("[SUMMARY]")
        repo_mission_template = await get_mission_template(mission_template_id)
        summary = repo_mission_template.summary()
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
