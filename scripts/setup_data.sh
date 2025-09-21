#!/bin/bash
# Setup minimal data for Grape Challenge (Production)

# Stay in root directory for correct database path

echo "🌱 Setting up production data..."

# Run Python setup for production (no TEST_MODE)
PYTHONPATH=grape-challenge python3 << 'EOF'

from usecases.user import CreateUserCommand, create_user
from repositories import fruit as fruit_repo, mission as mission_repo

print("Creating admin user...")
try:
    admin_cmd = CreateUserCommand(name="관리자", cell="관리자", role="admin")
    admin_user = create_user(admin_cmd)
    print(f"✓ Admin user created: {admin_user['name']} (ID: {admin_user['id']})")
except Exception as e:
    print(f"✗ Failed to create admin user: {e}")

print("Creating fruit template...")
try:
    grape_template = fruit_repo.create_fruit_template(
        name="포도",
        type="normal",
        status_images={
            "first": "grape_1.png",
            "second": "grape_2.png",
            "third": "grape_3.png",
            "fourth": "grape_4.png",
            "fifth": "grape_5.png",
            "sixth": "grape_6.png",
            "seventh": "grape_7.png"
        }
    )
    print(f"✓ Fruit template created: {grape_template['name']} (ID: {grape_template['id']})")
except Exception as e:
    print(f"✗ Failed to create fruit template: {e}")

print("Creating Bible reading mission template...")
try:
    bible_mission = mission_repo.create_mission_template(
        name="성경 1장 읽기",
        type="daily",
        content="하루에 성경을 한 장 이상 읽어보세요."
    )
    print(f"✓ Mission template created: {bible_mission['name']} (ID: {bible_mission['id']})")
except Exception as e:
    print(f"✗ Failed to create mission template: {e}")

print("\n🎉 Production setup complete!")
print("📖 Mission: 성경 1장 읽기")
print("🍇 Fruit: 포도 (7단계 성장)")
print("👑 Admin: 관리자 / 관리자")
print("\nDatabase created at: database/db.json")
EOF

echo "✅ Production setup completed!"