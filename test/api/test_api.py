import asyncio
import os
import subprocess

os.environ["APP_ENV"] = "dev"

from fastapi.testclient import TestClient
from grapechallenge.bin.server import app
from grapechallenge.database.database import DatabaseClient, transactional_session_helper
from grapechallenge.config import get_database_config


# Cleanup functions
async def cleanup_database():
    """Clean up all test data from database"""
    async with transactional_session_helper() as session:
        from grapechallenge.domain.user.repo_user import UserModel
        from grapechallenge.domain.fruit.repo_fruit import FruitModel
        from grapechallenge.domain.mission.repo_mission import MissionModel

        await session.execute(MissionModel.__table__.delete())
        await session.execute(FruitModel.__table__.delete())
        await session.execute(UserModel.__table__.delete())


async def verify_user_in_db(user_id: str):
    """Verify user exists in database"""
    async with transactional_session_helper() as session:
        from grapechallenge.domain.user import RepoUser
        repo_user = await RepoUser.get_by_id(session=session, id=user_id)
        return repo_user


async def verify_fruit_in_db(fruit_id: str):
    """Verify fruit exists in database"""
    async with transactional_session_helper() as session:
        from grapechallenge.domain.fruit.repo_fruit import RepoFruit
        repo_fruit = await RepoFruit.get_by_id(session=session, id=fruit_id)
        return repo_fruit


async def verify_mission_in_db(mission_id: str):
    """Verify mission exists in database"""
    async with transactional_session_helper() as session:
        from grapechallenge.domain.mission import RepoMission
        repo_mission = await RepoMission.get_by_id(session=session, id=mission_id)
        return repo_mission


async def get_fruit_templates():
    """Get available fruit templates"""
    async with transactional_session_helper() as session:
        from grapechallenge.domain.fruit_template import RepoFruitTemplate
        templates = await RepoFruitTemplate.get_all(session=session)
        return templates


async def get_mission_templates():
    """Get available mission templates"""
    async with transactional_session_helper() as session:
        from grapechallenge.domain.mission_template import RepoMissionTemplate
        templates = await RepoMissionTemplate.get_all(session=session)
        return templates


async def setup_test_data():
    """Create test templates for fruits and missions"""
    async with transactional_session_helper() as session:
        from grapechallenge.domain.fruit_template import (
            RepoFruitTemplate, FruitTemplate,
            Name as FruitName, Type as FruitType,
            FirstStatus, SecondStatus, ThirdStatus,
            FourthStatus, FifthStatus, SixthStatus, SeventhStatus
        )
        from grapechallenge.domain.mission_template import (
            RepoMissionTemplate, MissionTemplate,
            Name as MissionName, Content, Type as MissionType
        )

        # Create fruit templates
        fruit_template = FruitTemplate.new(
            name=FruitName.from_str("사과"),
            type=FruitType.from_str("NORMAL"),
            first_status=FirstStatus.from_str("/images/apple_1.png"),
            second_status=SecondStatus.from_str("/images/apple_2.png"),
            third_status=ThirdStatus.from_str("/images/apple_3.png"),
            fourth_status=FourthStatus.from_str("/images/apple_4.png"),
            fifth_status=FifthStatus.from_str("/images/apple_5.png"),
            sixth_status=SixthStatus.from_str("/images/apple_6.png"),
            seventh_status=SeventhStatus.from_str("/images/apple_7.png")
        )
        await RepoFruitTemplate.create(session=session, fruit_template=fruit_template)

        # Create mission templates
        mission_template = MissionTemplate.new(
            name=MissionName.from_str("물주기"),
            content=Content.from_str("식물에 물을 줍니다"),
            type=MissionType.from_str("NORMAL")
        )
        await RepoMissionTemplate.create(session=session, mission_template=mission_template)

    print("✓ Test data created (fruit_template, mission_template)\n")


# Test runner
async def test_api():
    db_config = get_database_config()
    print(f"Database: {db_config.database_url()}")
    print("=" * 60)

    async with DatabaseClient(db_config.database_url()):
        print("✓ Database connected\n")

        # Initialize test client
        client = TestClient(app)

        # Clean up before tests
        await cleanup_database()
        print("✓ Database cleaned up\n")

        # Setup test data (templates)
        await setup_test_data()

        # TEST 1: Create User
        print("[TEST 1: POST /user - Create User]")
        response = client.post("/user", json={
            "cell": "다윗",
            "name": "홍길동"
        })
        assert response.status_code == 201
        user_data = response.json()
        user_id = user_data["id"]
        print(f"✓ API Response: {response.status_code}")
        print(f"✓ Created user_id: {user_id}")

        # Verify in DB
        repo_user = await verify_user_in_db(user_id)
        assert repo_user is not None
        assert repo_user.user.cell.to_str() == "다윗"
        assert repo_user.user.name.to_str() == "홍길동"
        print(f"✓ DB Verification: User exists with cell={repo_user.user.cell.to_str()}, name={repo_user.user.name.to_str()}\n")

        # TEST 2: Login User
        print("[TEST 2: POST /login - Login User]")
        response = client.post("/login", json={
            "cell": "다윗",
            "name": "홍길동"
        })
        assert response.status_code == 200
        login_data = response.json()
        assert login_data["user_id"] == user_id
        print(f"✓ API Response: {response.status_code}")
        print(f"✓ Logged in user_id: {login_data['user_id']}\n")

        # TEST 3: Create Fruit
        print("[TEST 3: POST /fruit - Create Fruit]")
        response = client.post("/fruit", json={
            "user_id": user_id
        })
        assert response.status_code == 201
        fruit_data = response.json()
        fruit_id = fruit_data["id"]
        print(f"✓ API Response: {response.status_code}")
        print(f"✓ Created fruit_id: {fruit_id}")

        # Verify in DB
        repo_fruit = await verify_fruit_in_db(fruit_id)
        assert repo_fruit is not None
        assert repo_fruit.fruit.user_id == user_id
        assert repo_fruit.fruit.status.to_str() == "FIRST_STATUS"
        print(f"✓ DB Verification: Fruit exists with status={repo_fruit.fruit.status.to_str()}\n")

        # TEST 4: Get My Fruits
        print("[TEST 4: GET /fruits/mine - Get My Fruits]")
        response = client.get("/fruits/mine", params={
            "user_id": user_id
        })
        assert response.status_code == 200
        fruits_data = response.json()
        assert fruits_data["count"] >= 1
        print(f"✓ API Response: {response.status_code}")
        print(f"✓ Found {fruits_data['count']} fruit(s)\n")

        # TEST 5: Get In Progress Fruit
        print("[TEST 5: GET /fruit/in-progress - Get In Progress Fruit]")
        response = client.get("/fruit/in-progress", params={
            "user_id": user_id
        })
        assert response.status_code == 200
        progress_data = response.json()
        print(f"✓ API Response: {response.status_code}")
        print(f"✓ In progress fruit: {progress_data}\n")

        # TEST 6: Complete Mission
        print("[TEST 6: POST /mission/complete - Complete Mission]")

        # Use the mission template we created in setup
        mission_name = "물주기"

        response = client.post("/mission/complete", json={
            "user_id": user_id,
            "fruit_id": fruit_id,
            "name": mission_name
        })
        assert response.status_code == 201
        mission_data = response.json()
        mission_id = mission_data["id"]
        print(f"✓ API Response: {response.status_code}")
        print(f"✓ Completed mission_id: {mission_id}")

        # Verify mission in DB
        repo_mission = await verify_mission_in_db(mission_id)
        assert repo_mission is not None
        print(f"✓ DB Verification: Mission exists")

        # Verify fruit status changed
        repo_fruit = await verify_fruit_in_db(fruit_id)
        assert repo_fruit.fruit.status.to_str() == "SECOND_STATUS"
        print(f"✓ DB Verification: Fruit status changed to {repo_fruit.fruit.status.to_str()}\n")

        # TEST 7: Complete Multiple Missions to reach SEVENTH_STATUS and then COMPLETED
        print("[TEST 7: Complete Multiple Missions to reach COMPLETED (7 total missions)]")
        for i in range(2, 9):  # SECOND_STATUS to COMPLETED (7 more missions)
            response = client.post("/mission/complete", json={
                "user_id": user_id,
                "fruit_id": fruit_id,
                "name": mission_name
            })
            assert response.status_code == 201

            if i < 8:
                current_status = ["SECOND_STATUS", "THIRD_STATUS", "FOURTH_STATUS", "FIFTH_STATUS", "SIXTH_STATUS", "SEVENTH_STATUS"][i-2]
            else:
                current_status = "COMPLETED"

            print(f"  Mission {i}/8 completed → {current_status}")

        # Verify fruit is at COMPLETED status
        repo_fruit = await verify_fruit_in_db(fruit_id)
        assert repo_fruit.fruit.status.to_str() == "COMPLETED"
        print(f"✓ Fruit reached COMPLETED status after 8 total missions (1 seed + 7 missions)\n")

        # TEST 8: Verify COMPLETED fruit is not in progress
        print("[TEST 8: GET /fruit/in-progress - Verify COMPLETED fruit not in progress]")
        response = client.get("/fruit/in-progress", params={
            "user_id": user_id
        })
        assert response.status_code == 200
        progress_data = response.json()
        assert progress_data["fruit"]["fruit_id"] is None or progress_data["fruit"]["fruit_id"] != fruit_id
        print(f"✓ COMPLETED fruit is not in progress\n")

        # TEST 9: Create Multiple Users
        print("[TEST 9: POST /users - Create Multiple Users]")
        response = client.post("/users", json={
            "users": [
                {"cell": "요셉", "name": "김철수"},
                {"cell": "베드로", "name": "이영희"}
            ]
        })
        assert response.status_code == 201
        users_data = response.json()
        assert users_data["count"] == 2
        print(f"✓ API Response: {response.status_code}")
        print(f"✓ Created {users_data['count']} users\n")

        # Cleanup after tests
        print("[CLEANUP]")
        await cleanup_database()
        print("✓ Database cleaned up\n")

    print("=" * 60)
    print("All API tests passed!")


if __name__ == "__main__":
    subprocess.run(["./scripts/setup_dev_db.sh"])
    asyncio.run(test_api())