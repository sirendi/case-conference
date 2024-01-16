# Define variables
include .env
IMAGE_NAME=app
CONTAINER_NAME=case-conference
PYTHON_VERSION:=3.11
COV_FAIL:=80
PYTEST_EXPRESSION:=$(if $(exp),-k $(exp),)
PG_CONTAINER:=postgres-db

# add .env to environment vars
export $(shell sed 's/=.*//' .env)

# Deployment
ifdef env
	include .env.$(env)
endif

# initial setup of the python environment
init:
	conda init
	conda create --name $(IMAGE_NAME) python=$(PYTHON_VERSION) --force

poetry-install:
	poetry install

# install python libs from environment.yml
conda-install:
	conda env update --file environment.yml --name $(IMAGE_NAME)

# install python libs from environment.yml and pyproject.toml
install:
	@$(MAKE) conda-install
	@$(MAKE) poetry-install

# Import data into PostgreSQL
import-data:
	docker cp data/data.csv $(PG_CONTAINER):/data.csv
	docker exec -it $(PG_CONTAINER) psql -U demo_user -d patient -c "\COPY patients FROM '/data.csv' CSV HEADER;"

# Default target
default: build

## Start up docker-compose
docker-up:
	docker compose up -d

docker-build:
	docker compose build

docker-down:
	docker compose down

docker-logs:
	docker compose logs $(service) -f

# Stop and remove the Docker container
docker-stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

# Rebuild the Docker image and run the container
rebuild: build run

check-env:
ifndef env
	$(error env is undefined)
endif

# Show help
help:
	@echo "Makefile commands:"
	@echo "build   - Build the Docker image."
	@echo "run     - Run the Docker container."
	@echo "stop    - Stop and remove the Docker container."
	@echo "rebuild - Rebuild the Docker image and run the container."
	@echo "help    - Show this help message."
