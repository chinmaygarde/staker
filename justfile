set dotenv-load := true

format:
  uvx ruff format staker

check_format:
  uvx ruff format staker --diff

up:
  docker compose up --build
