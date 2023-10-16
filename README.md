# Docker Template for FastAPI Project

Developed for help to create containerized projects using Docker with FastAPI.

## Installation
1. Install Docker and Docker Compose.
2. Clone this repository or fork this repository:
```bash
git clone https://github.com/heytorvas/template-fastapi-docker.git
```
3. Change directory to repository:
```bash
cd template-fastapi-docker
```
## Development
## Environment
1. Build and up the containers:
```bash
docker-compose up --build &
```

### Code Styleguide
To ensure that the project style guide is being followed, the pre-commit needs to be installed:

1. Install pre-commit
```bash
pip install pre-commit
```
2. Install hooks
```bash
pre-commit install
```

### Include or upgrade library
To add a new library or upgrade one, needs to insert library name on `requirements.in` file and then use the following command to generate library hashes:

```bash
pip-compile --upgrade-package "<PACKAGE>" --generate-hashes --no-header --no-annotate --verbose
```

### Tests
To run the tests, including unit and integration, run the following commands:

```bash
# With API running, access the container
docker-compose exec -it api bash

# Run the tests
python -m pytest tests/
```

## Notes
Run project: ```http://localhost:5000```
