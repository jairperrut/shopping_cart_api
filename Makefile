run-server:
	uvicorn src.fastapi.main:app --host 0.0.0.0 --port 8000

run-tests:
	python -m pytest --cov=src --cov-report=term-missing -v
