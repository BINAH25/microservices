#!/bin/sh
set -e

# Only init if migrations don't exist
if [ ! -d "migrations/versions" ]; then
    echo "Initializing migrations..."
    flask db init
fi

# Always try to make migrations (safe if no changes)
echo "Running migrations..."
flask db migrate -m "Auto migration" || echo "Migration skipped or already up to date"

# Try upgrading, ignore if already at head
flask db upgrade || echo "Upgrade failed. Possible mismatch in migration history."

# Start the app
echo "Starting app..."
python main.py
