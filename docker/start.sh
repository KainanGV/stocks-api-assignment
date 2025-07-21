#!/bin/sh
set -e

# wait for database to be ready
python <<'PY'
import os
import time
import psycopg2
url = os.environ.get('DATABASE_URL')
for _ in range(30):
    try:
        conn = psycopg2.connect(url)
        conn.close()
        break
    except Exception as e:
        print('Waiting for database...', e)
        time.sleep(1)
else:
    raise SystemExit('Database not reachable')
PY

alembic upgrade head
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
