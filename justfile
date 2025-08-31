set dotenv-load := true

# Apply source code formatting fixes in-place.
format:
  uvx ruff format staker

# Check the format of source code.
check_format:
  uvx ruff format staker --diff

# Launch a docker compose setup suitable for solo home staking.
up:
  docker compose up --build
