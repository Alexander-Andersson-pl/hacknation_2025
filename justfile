# Path to the virtual environment
venv := "venv"
python := "venv/bin/python"
pip := "venv/bin/pip"

install-env:
    @echo "📦 Creating virtual environment..."
    python3 -m venv {{venv}}
    @echo "Install dependencies by running: just install"

# 2. Install dependencies from requirements.txt
install:
    @echo "📦 Installing Python dependencies..."
    @echo {{pip}}
    {{pip}} install --upgrade pip
    {{pip}} install -r requirements.txt
    @echo "📦 Installing spaCy Polish model..."
#    {{python}} -m spacy download pl_core_news_lg || true

main:
    {{python}} src/main.py

test:
    {{python}} -m pytest -q