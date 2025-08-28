main:
  uv run staker.py

format:
  uvx ruff format .

check_format:
  uvx ruff format . --diff
