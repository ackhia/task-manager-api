# Task Manager API
 
 This is an example Task Tracking API built with FastAPI. It demonstrates best practices for organizing a production-like Python API: clear routing, dependency injection, SQLAlchemy models, Pydantic schemas, authentication using JWT, and a test suite.
 
 **Quickstart / Run locally**
 
 - This project uses `uv` for environment and dependency tooling. To install all required modules for development, install `uv` and run `uv sync`:
```bash
pip install uv
uv sync
```
- Ensure local environment variables are available by renaming the example env file:
```bash
mv .env.example .env
```
- Start the app (development):
```bash
uvicorn app.main:app --reload
```
The API docs will be available at /docs (Swagger UI) and /redoc if the server is running.
 
 **Running tests**
 
 - The project includes pytest tests under app/tests. Run them with:
```bash
pytest
```
The tests use a temporary SQLite database so they will not modify your local development database.
 
**Docker & Docker Compose**

- **Requirements:** Install Docker Engine and Docker Compose (or use the integrated `docker` CLI with `docker compose`).

- **Build the image (optional):**
```bash
docker build -t task-manager-api .
```

- **Run the container using docker run. Make sure you have created a .env file first (see instructions above):**
```bash
docker run --env-file .env -p 8000:8000 task-manager-api
```

- **Run with Docker Compose:** (recommended for development)
```bash
# Build and start services (foreground):
docker-compose up --build
# Or with the modern Docker CLI plugin:
docker compose up --build
# Run detached:
docker-compose up -d --build
```

- **Helpful commands:**
   - Stop and remove containers: `docker-compose down`
   - View service logs: `docker-compose logs -f`

- **Notes:**
   - The provided [docker-compose.yml](docker-compose.yml) mounts `./data:/app/data` to persist database/files and `./:/app:cached` for live code reload during development. For production, remove the source bind mount and persist data using a dedicated volume or managed database.
   - The app will be available at http://localhost:8000 and Swagger UI at http://localhost:8000/docs when the container is running.

 **Authentication**
 
 - Authentication uses OAuth2 with a password. Once you have created an account with /auth/register, you can use the email and password to login via /auth/login. If using the swagger UI, you can use the Authorize button at the top with your email and password to authenticate all of the endpoints.
 
 **API Endpoints**
 
 - **Auth**
    - **POST** /auth/register — register a new user. Accepts UserRegister (email, full_name, password). Returns created user.
    - **POST** /auth/login — login using form data (username is email) and receive an access token (Token).
 
 - **Users**
    - **GET** /users/me — returns the currently authenticated user (UserRead).
    - **GET** /users/{user_id} — returns a user by id (404 if not found).
    - **GET** /users/ — list users (supports skip and limit query parameters).
 
 - **Tasks**
    - **POST** /tasks/ — create a new task (requires auth). Accepts TaskCreate (title, description, due_date...). Returns TaskRead.
     - **GET** /tasks/ — list tasks for the current user.
     - **GET** /tasks/{task_id} — get a task by id (owner-only).
    - **PUT** /tasks/{task_id} — update a task (owner-only). Accepts TaskUpdate.
    - **DELETE** /tasks/{task_id} — delete a task (owner-only). Returns HTTP 204 on success.
 
 Refer to the route implementations in [app/routes](app/routes) for full details and request/response schemas in [app/schemas](app/schemas).
 
 **Best-practice notes**
 
 - Separation of concerns: routes, services, schemas and models are organized into dedicated modules.
 - Dependency injection: database sessions and current user are provided via FastAPI dependencies, making testing and overrides straightforward.
 - Tests: tests are written using TestClient and override dependencies to use an isolated test database.
 
 **Contact / Professional services**
 
 If you need help building a Python infrastructure project, hiring assistance, or consulting on API design and best practices, please reach out via my website:
 
 https://ackhia.github.io/pyjon/
 
 I'm happy to discuss project requirements, offer architecture guidance, or help implement production-ready Python APIs.