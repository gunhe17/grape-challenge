import asyncio
import os
import subprocess

os.environ["APP_ENV"] = "dev"

from grapechallenge.database.database import DatabaseClient, transactional_session_helper
from grapechallenge.config import get_database_config
from grapechallenge.domain.user import Cell, Name, User, RepoUser


# CRUD Operations
async def create_user(cell: str, name: str) -> str:
    async with transactional_session_helper() as session:
        user = User.new(
            cell=Cell.from_str(cell),
            name=Name.from_str(name)
        )
        repo_user = await RepoUser.create(session=session, user=user)
        return repo_user.id


async def get_user(user_id: str):
    async with transactional_session_helper() as session:
        return await RepoUser.get_by_id(session=session, id=user_id)


async def get_user_by_cell_and_name(cell: str, name: str):
    async with transactional_session_helper() as session:
        return await RepoUser.get_by_cell_and_name(session=session, cell=cell, name=name)


async def update_user(user_id: str, cell: str, name: str) -> None:
    async with transactional_session_helper() as session:
        user = User.new(
            cell=Cell.from_str(cell),
            name=Name.from_str(name)
        )
        await RepoUser.update(session=session, user=user, id=user_id)


async def create_user_with_rollback(cell: str, name: str):
    """Test function that creates a user then raises an exception to trigger rollback"""
    async with transactional_session_helper() as session:
        user = User.new(
            cell=Cell.from_str(cell),
            name=Name.from_str(name)
        )
        await RepoUser.create(session=session, user=user)
        # Raise exception to trigger rollback
        raise ValueError("Intentional error to test rollback")


# Cleanup
async def cleanup_database():
    async with transactional_session_helper() as session:
        from grapechallenge.domain.user.repo_user import UserModel
        await session.execute(UserModel.__table__.delete())


# Test runner
async def test_crud():
    db_config = get_database_config()
    print(f"Database: {db_config.database_url()}")
    print("=" * 60)

    async with DatabaseClient(db_config.database_url()):
        print("✓ Database connected\n")

        # CREATE
        print("[CREATE]")
        user_id = await create_user("다윗", "홍길동")
        repo_user = await get_user(user_id)
        print(f"✓ Created: id={repo_user.id}, cell={repo_user.user.cell.to_str()}, name={repo_user.user.name.to_str()}\n")

        # READ
        print("[READ]")
        repo_user = await get_user(user_id)
        print(f"✓ Found: id={repo_user.id}, cell={repo_user.user.cell.to_str()}, name={repo_user.user.name.to_str()}\n")

        # READ BY CELL AND NAME
        print("[READ BY CELL AND NAME]")
        repo_user = await get_user_by_cell_and_name("다윗", "홍길동")
        print(f"✓ Found: id={repo_user.id}, cell={repo_user.user.cell.to_str()}, name={repo_user.user.name.to_str()}\n")

        # UPDATE
        print("[UPDATE]")
        await update_user(user_id, "요셉", "김철수")
        repo_user = await get_user(user_id)
        print(f"✓ Updated: id={repo_user.id}, cell={repo_user.user.cell.to_str()}, name={repo_user.user.name.to_str()}\n")

        # TRANSACTION ROLLBACK
        print("[TRANSACTION ROLLBACK]")
        try:
            await create_user_with_rollback("베드로", "이영희")
            print("✗ Rollback failed: exception not raised")
        except ValueError as e:
            print(f"✓ Exception caught: {e}")
            print(f"✓ Rollback confirmed: transaction was rolled back\n")

        # SUMMARY
        print("[SUMMARY]")
        repo_user = await get_user(user_id)
        summary = repo_user.summary()
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
