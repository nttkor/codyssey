문제 3: 파이썬 프로젝트에서 .gitignore 사용 이유
파이썬 개발 시 __pycache__와 .venv 디렉토리가 생성되는 이유를 조사한다.
GitHub에서 .gitignore 템플릿 중 Python을 선택했을 때 포함되는 항목을 확인한다.
Flask 기반 프로젝트를 기준으로 .gitignore에 추가되어야 할 항목들을 나열한다

✅ 기본 Python 관련 항목
markdown
Copy
Edit
# Python bytecode
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
build/
dist/
*.egg-info/
.eggs/
*.egg
pip-wheel-metadata/

# Virtual environment
venv/
ENV/
env/
.venv/
✅ Flask / 프로젝트 환경 관련 항목
bash
Copy
Edit
# Flask instance folder (if used)
instance/

# Flask cache or session files
*.log
*.pid
*.sqlite3
*.db

# Flask dotenv files
.env
.env.*

# Flask-specific config
config.py
config/*.pyc
✅ IDE 및 편집기 관련 (예: VSCode, PyCharm 등)
bash
Copy
Edit
# VSCode
.vscode/

# PyCharm
.idea/

# MacOS
.DS_Store

# Windows
Thumbs.db