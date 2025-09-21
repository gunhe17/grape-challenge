#!/bin/bash
# Reset Database - Clean all data and initialize fresh

echo "🧹 Resetting database..."

# Backup existing database if it exists
if [ -f "database/db.json" ]; then
    BACKUP_FILE="database/db_backup_$(date +%Y%m%d_%H%M%S).json"
    cp "database/db.json" "$BACKUP_FILE"
    echo "📁 Backup created: $BACKUP_FILE"
fi

# Remove existing database files
rm -f database/db.json
rm -f database/test_db.json

echo "🗑️  Database files removed"

# Recreate empty database structure
mkdir -p database

PYTHONPATH=grape-challenge python3 << 'EOF'
import json
from pathlib import Path
from datetime import datetime

# Create empty database structure
empty_db = {
    "users": [],
    "sessions": [],
    "fruits": [],
    "missions": [],
    "fruit_templates": [],
    "mission_templates": [],
    "_metadata": {
        "created_at": datetime.now().isoformat(),
        "last_modified": datetime.now().isoformat()
    }
}

# Save empty production database
db_path = Path("database/db.json")
with open(db_path, 'w', encoding='utf-8') as f:
    json.dump(empty_db, f, indent=2, ensure_ascii=False)

print("📄 Empty database created: database/db.json")

# Save empty test database
test_db_path = Path("database/test_db.json")
with open(test_db_path, 'w', encoding='utf-8') as f:
    json.dump(empty_db, f, indent=2, ensure_ascii=False)

print("📄 Empty test database created: database/test_db.json")
EOF

echo ""
echo "✅ Database reset complete!"
echo ""
echo "Next steps:"
echo "  1. Run setup data: ./scripts/setup_data.sh"
echo "  2. Start server: ./scripts/start.sh"