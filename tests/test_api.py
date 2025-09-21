#!/usr/bin/env python3
"""
Grape Challenge API Test Script
grape-challenge/server.py based API tests
"""
import requests
import time
import sys
import os
import json
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://localhost:8000"
PROJECT_ROOT = Path(__file__).parent.parent
TEST_DB_PATH = PROJECT_ROOT / "grape-challenge" / "database" / "test_db.json"

def setup_test_db():
    """Initialize test database"""
    print("Setting up test database...")

    # Create empty test database
    test_db = {
        "users": [],
        "sessions": [],
        "fruits": [],
        "fruit_templates": [],
        "missions": [],
        "mission_templates": []
    }

    # Ensure directory exists
    TEST_DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Write test database
    with open(TEST_DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(test_db, f, indent=2, ensure_ascii=False)

    print(f"  Test database initialized at {TEST_DB_PATH}")

def cleanup_test_db():
    """Clean up test database after tests"""
    print("Cleaning up test database...")

    # Keep test database for debugging if needed
    if TEST_DB_PATH.exists():
        print(f"  Test results kept in {TEST_DB_PATH}")

    print("  Cleanup complete")

def test_api():
    print("Grape Challenge API Test Start")
    print("=" * 50)

    # 1. Health Check
    print("1. Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}, Response: {response.json()}")
        assert response.status_code == 200
        print("SUCCESS: Health check passed")
    except Exception as e:
        print(f"ERROR: Health check failed: {e}")
        return False
    print()

    # 2. User Creation Test
    print("2. User Creation Test")
    users_data = [
        {"name": "김철수", "cell": "010-1234-5678", "role": "user"},
        {"name": "이영희", "cell": "010-2345-6789", "role": "user"},
        {"name": "관리자", "cell": "010-0000-0000", "role": "admin"}
    ]

    created_users = []
    for user_data in users_data:
        try:
            response = requests.post(f"{BASE_URL}/user", json=user_data)
            if response.status_code == 200:
                user = response.json()
                created_users.append(user)
                print(f"SUCCESS: User created: {user['name']} (ID: {user['id']})")
            else:
                print(f"ERROR: User creation failed: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"ERROR: User creation error: {e}")
    print()

    if not created_users:
        print("ERROR: No users created, stopping test")
        return False

    # 3. Login Test
    print("3. Login Test")
    login_tokens = {}
    for user_data in users_data:
        try:
            login_request = {"name": user_data["name"], "cell": user_data["cell"]}
            response = requests.post(f"{BASE_URL}/login", json=login_request)
            if response.status_code == 200:
                login_result = response.json()
                login_tokens[user_data["name"]] = login_result.get("token", "")
                print(f"SUCCESS: Login successful: {user_data['name']}")
            else:
                print(f"ERROR: Login failed: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"ERROR: Login error: {e}")
    print()

    # 4. Fruit Template Creation Test
    print("4. Fruit Template Creation Test")
    fruit_templates_data = [
        {
            "name": "사과",
            "type": "normal",
            "status_images": {
                "first": "apple_1.png",
                "second": "apple_2.png",
                "third": "apple_3.png",
                "fourth": "apple_4.png",
                "fifth": "apple_5.png",
                "sixth": "apple_6.png",
                "seventh": "apple_7.png"
            }
        },
        {
            "name": "바나나",
            "type": "normal",
            "status_images": {
                "first": "banana_1.png",
                "second": "banana_2.png",
                "third": "banana_3.png",
                "fourth": "banana_4.png",
                "fifth": "banana_5.png",
                "sixth": "banana_6.png",
                "seventh": "banana_7.png"
            }
        },
        {
            "name": "포도",
            "type": "special",
            "status_images": {
                "first": "grape_1.png",
                "second": "grape_2.png",
                "third": "grape_3.png",
                "fourth": "grape_4.png",
                "fifth": "grape_5.png",
                "sixth": "grape_6.png",
                "seventh": "grape_7.png"
            }
        }
    ]

    created_fruit_templates = []
    for template_data in fruit_templates_data:
        try:
            response = requests.post(f"{BASE_URL}/fruit-template", json=template_data)
            if response.status_code == 200:
                template = response.json()
                created_fruit_templates.append(template)
                print(f"SUCCESS: Fruit template created: {template['name']} (ID: {template['id']})")
            else:
                print(f"ERROR: Fruit template creation failed: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"ERROR: Fruit template creation error: {e}")
    print()

    # 5. Mission Template Creation Test
    print("5. Mission Template Creation Test")
    mission_templates_data = [
        {"name": "물 1L 마시기", "type": "daily", "content": "하루에 물을 1L 이상 마셔보세요."},
        {"name": "10분 산책하기", "type": "exercise", "content": "10분 이상 야외에서 산책해보세요."},
        {"name": "독서 30분", "type": "study", "content": "30분 동안 책을 읽어보세요."},
        {"name": "스트레칭", "type": "health", "content": "5분간 몸을 스트레칭해보세요."},
        {"name": "감사 일기", "type": "mental", "content": "오늘 감사한 일 3가지를 적어보세요."},
        {"name": "요리하기", "type": "life", "content": "간단한 요리를 만들어보세요."},
        {"name": "친구와 대화", "type": "social", "content": "친구나 가족과 의미있는 대화를 나눠보세요."}
    ]

    created_mission_templates = []
    for template_data in mission_templates_data:
        try:
            response = requests.post(f"{BASE_URL}/mission-template", json=template_data)
            if response.status_code == 200:
                template = response.json()
                created_mission_templates.append(template)
                print(f"SUCCESS: Mission template created: {template['name']} (ID: {template['id']})")
            else:
                print(f"ERROR: Mission template creation failed: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"ERROR: Mission template creation error: {e}")
    print()

    # 6. Random Mission Template Query Test
    print("6. Random Mission Template Query Test")
    try:
        response = requests.get(f"{BASE_URL}/mission-template/random")
        if response.status_code == 200:
            random_template = response.json()
            print(f"SUCCESS: Random mission: {random_template['name']}")
        else:
            print(f"ERROR: Random mission query failed: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"ERROR: Random mission query error: {e}")
    print()

    # 7. User Session Start and Mission Complete Simulation
    print("7. User Session Start and Mission Complete Simulation")
    for user in created_users[:2]:  # First 2 users only
        if user["role"] == "admin":
            continue

        print(f"\nUser: {user['name']}")
        user_id = user["id"]

        # Start session
        print("  Starting session")
        try:
            response = requests.post(f"{BASE_URL}/session", params={"user_id": user_id})
            if response.status_code == 200:
                session = response.json()
                print(f"  SUCCESS: Session created: {session['id']}")
            else:
                print(f"  ERROR: Session creation failed: {response.status_code}, {response.text}")
                continue
        except Exception as e:
            print(f"  ERROR: Session creation error: {e}")
            continue

        # Complete 3 missions
        for i in range(3):
            if created_mission_templates:
                template_id = created_mission_templates[i % len(created_mission_templates)]["id"]
                mission_request = {
                    "user_id": user_id,
                    "mission_template_id": template_id
                }

                print(f"  Mission {i+1} completion attempt")
                try:
                    response = requests.post(f"{BASE_URL}/mission/complete", json=mission_request)
                    if response.status_code == 200:
                        result = response.json()
                        print(f"  SUCCESS: Mission completed")
                        if result.get("fruit"):
                            print(f"    Fruit status: {result['fruit']['status']}")
                    else:
                        print(f"  ERROR: Mission completion failed: {response.status_code}, {response.text}")
                except Exception as e:
                    print(f"  ERROR: Mission completion error: {e}")

                time.sleep(0.5)  # API call interval
    print()

    # 8. In-Progress Session Query Test
    print("8. In-Progress Session Query Test")
    for user in created_users[:2]:
        if user["role"] == "admin":
            continue

        user_id = user["id"]
        try:
            response = requests.get(f"{BASE_URL}/session/user/{user_id}/in-progress")
            if response.status_code == 200:
                session = response.json()
                print(f"SUCCESS: {user['name']} in-progress session: {len(session.get('mission_ids', []))} missions completed")
            elif response.status_code == 404:
                print(f"INFO: {user['name']} has no in-progress session")
            else:
                print(f"ERROR: {user['name']} session query failed: {response.status_code}")
        except Exception as e:
            print(f"ERROR: Session query error: {e}")
    print()

    # 9. Fruit Template List Query Test
    print("9. Fruit Template List Query Test")
    try:
        response = requests.get(f"{BASE_URL}/fruit-templates")
        if response.status_code == 200:
            templates = response.json()
            print(f"SUCCESS: {len(templates)} fruit templates:")
            for template in templates:
                print(f"  - {template['name']} ({template['type']})")
        else:
            print(f"ERROR: Fruit template query failed: {response.status_code}")
    except Exception as e:
        print(f"ERROR: Fruit template query error: {e}")
    print()

    # 10. Mission Template List Query Test
    print("10. Mission Template List Query Test")
    try:
        response = requests.get(f"{BASE_URL}/mission-templates")
        if response.status_code == 200:
            templates = response.json()
            print(f"SUCCESS: {len(templates)} mission templates:")
            for template in templates:
                print(f"  - {template['name']} ({template['type']})")
        else:
            print(f"ERROR: Mission template query failed: {response.status_code}")
    except Exception as e:
        print(f"ERROR: Mission template query error: {e}")
    print()

    # 11. Admin Statistics Query Test
    print("11. Admin Statistics Query Test")
    try:
        response = requests.get(f"{BASE_URL}/admin/statistics")
        if response.status_code == 200:
            stats = response.json()
            print(f"SUCCESS: Total users: {stats['total_users']}")
            for user_stat in stats['users']:
                print(f"  - {user_stat['name']}: {user_stat['statistics']['total_sessions']} sessions, {user_stat['statistics']['completed_sessions']} completed")
        else:
            print(f"ERROR: Admin statistics query failed: {response.status_code}")
    except Exception as e:
        print(f"ERROR: Admin statistics query error: {e}")
    print()

    print("API Test Complete!")
    return True

if __name__ == "__main__":
    success = False
    try:
        # Setup test database
        setup_test_db()

        # Run tests
        success = test_api()

    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to server. Please check if server is running.")
        print("Server run command: cd grape-challenge && python -m uvicorn server:app --reload")

    except Exception as e:
        print(f"ERROR: Test error occurred: {e}")

    finally:
        # Always cleanup database
        cleanup_test_db()

        # Exit with appropriate code
        sys.exit(0 if success else 1)