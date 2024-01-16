# Generative AI App with Streamlit and OpenAI

This repository contains a Streamlit application that demonstrates the capabilities of a generative AI app powered by OpenAI's API. The application is containerized using Docker for easy deployment and scalability.

## Prerequisites

- Docker
- An API key from OpenAI

## Installation and Setup

### Clone and Set up the Repository

```shell
# Clone this repository to your local machine with
git clone https://github.com/sirendi/case-conference.git

# Set up environment. Edit values appropriately
cp env.example .env

# Add postgresql for Mac machines
brew install postgresql

# Setups the python and conda environment
make init

# Activate your Python env
conda activate case

# Install python libs
make install
```

## Database Setup and Data Import

After setting up the project and starting the PostgreSQL container, you can import the patient data from a CSV file into the database using the following steps:

### Build and Start the Application

```shell
make docker-build
make docker-up
```

### Copy CSV File to the PostgreSQL Container and Import Data into the Database

```shell
make import-data
```

## Usage

After starting the container, the Streamlit app will be accessible at `http://localhost:8501`. Enter your prompts in the provided text area and click 'Generate' to see the AI-generated responses.

### Stop the Docker Container

When you're done and you want to stop the container, use:

```shell
docker-compose down
```

## Pipe a log

```shell
make docker-logs service=<SERVICE>
```

## Connect to the Database

```shell
docker exec -it postgres-db psql -U demo_user -d patient
```

## Outside the scope of the MVP

Unit and integration tests

Retrieval Augmented Generation

Semantic Routing
