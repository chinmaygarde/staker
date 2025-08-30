[working-directory: 'staker']
staker:
  uv run staker.py

format:
  uvx ruff format staker

check_format:
  uvx ruff format staker --diff

docker:
  docker build . -t staker
