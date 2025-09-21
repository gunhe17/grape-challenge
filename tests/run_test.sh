#!/bin/bash

echo "Grape Challenge API Test Execution Script"
echo "=========================================="

# Change to project root directory
cd "$(dirname "$0")/.."

# 1. Check dependencies
echo "1. Checking dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

# 2. Ensure database directory exists
echo "2. Ensuring database directory exists..."
mkdir -p grape-challenge/database

# 3. Set test environment variables
echo "3. Setting test environment..."
export TEST_MODE=true
export TEST_DB_PATH="$(pwd)/grape-challenge/database/test_db.json"
export PYTHONPATH=.

# 4. Start server in background (with test database)
echo "4. Starting server with test database..."
cd grape-challenge
python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000 &
SERVER_PID=$!
cd ..

# Wait for server to start
echo "   Waiting for server to start... (5 seconds)"
sleep 5

# 5. Run tests (includes DB setup and cleanup)
echo "5. Running API tests with test database..."
python tests/test_api.py

# Save test result
TEST_RESULT=$?

# 6. Stop server
echo "6. Stopping server..."
kill $SERVER_PID > /dev/null 2>&1
wait $SERVER_PID 2>/dev/null

echo "=========================================="
if [ $TEST_RESULT -eq 0 ]; then
    echo "SUCCESS: All tests passed!"
else
    echo "ERROR: Some tests failed!"
fi

exit $TEST_RESULT