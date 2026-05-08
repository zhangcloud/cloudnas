#!/bin/bash
set -e
cd "$(dirname "$0")/.."

if [ ! -d "backend/.venv" ]; then
  python3 -m venv backend/.venv
fi
source backend/.venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt

cd frontend
npm install

echo "安装完成。后端: cd backend && source .venv/bin/activate && uvicorn main:app --reload"
echo "前端: cd frontend && npm run dev"
