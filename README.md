# First FastAPI Application

This is a simple **FastAPI** application that implements a CRUD (Create, Read, Update, Delete) API for managing items, using **PostgreSQL** as the database. The project uses

- **SQLAlchemy** for ORM.
- **Pydantic** for data validation.
- **databases** for async database operations.

---

## What is FastAPI?

FastAPI is a Python framework for building APIs with asynchronous programming. It’s fast (comparable to Node.js and Go), supports type hints for automatic validation, and generates interactive API documentation (via Swagger UI). It’s built on **Starlette** for web handling and **Pydantic** for data validation.

---

## Features

- Create, read, update, and delete items via RESTful API endpoints.
- PostgreSQL database integration for persistent storage.
- Automatic API documentation with Swagger UI.
- Input validation using Pydantic models.
- Error handling for common cases (e.g., item not found, duplicate IDs).

---

## Installation

1. Clone the Repository:

   ```bash
   git clone https://github.com/Chetan3500/first-fastapi-application.git
   ```

2. Create a Virtual Environment:

   Make sure python is installed, if not [Install Python](https://www.python.org/downloads/).

   ```shell
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. Install dependencies like FastAPI and Uvicorn (Uvicorn is an ASGI server to run your app).
   ```shell
   pip install fastapi uvicorn sqlalchemy databases psycopg2-binary asyncpg python-dontenv
   ```
   OR install `requirements.txt` which contain all necessary dependencies.
   ```shell
   pip install -r requirements.txt
   ```
4. Create a `.env` file to store your database credentials:
   ```
   echo "DATABASE_URL=postgresql://username:password@localhost:5432/fastapi_db" > .env
   ```
   Make sure to replace:
   - username with your_username (postgres)
   - password with username_password (mysecretpassword)
   ```
   postgresql://postgres:mysecretpassword@localhost:5432/fastapi_db
   ```
5. Run the app
   ```shell
   uvicorn main:app --reload
   ```
   `--reload` flag enables auto-reload for development.

- Vist: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs

---

## Usage

1. **API Documentation**: Open http://127.0.0.1:8000/docs in your browser to access the Swagger UI for interactive testing.
2. **Endpoints and Test with SwaggerUI**:
   - `Create`: POST `/items/` with JSON like `{"id": 1, "name": "Laptop", "price": 999.99, "is_available": true}`.
   - `Read All`: GET `/items/` to list all items.
   - `Read One`: GET `/items/{item_id}` to fetch the item with ID 1.
   - `Update`: PUT `/items/{item_id}` with updated JSON like `{"id": 1, "name": "Updated Laptop", "price": 1099.99, "is_available": false}`.
   - `Delete`: DELETE `/items/{item_id}` to remove the item with ID 1.
3. **Verify Database**:

   - Connect to your database using `psql`:
     ```bash
     psql -U your_username -d fast_api -W
     ```
     `-W` - for password
   - Check the `items` table:

     ```
       <!-- item created -->

     fastapi_db=# select * from items;
      id |  name  | price  | is_available
     ----+--------+--------+--------------
       1 | Laptop | 999.99 | t
     (1 row)

       <!-- item updated -->

     fastapi_db=# select * from items;
      id |      name      |  price  | is_available
     ----+----------------+---------+--------------
       1 | Updated Laptop | 1099.99 | f
     (1 row)
     ```

---

## Project Structure

- `main.py`: The main FastAPI application with CRUD endpoints and database logic.
- `.env`: Environment file for database credentials (not tracked in version control).
- `requirements.txt` - Contain necessary dependencies.

## Key-Notes

- **Pydantic’s ORM Mode**: The `orm_mode = True` in the Pydantic model allows FastAPI to convert SQLAlchemy objects to JSON-compatible responses.

## Next Steps

- **Authentication**: Add JWT or OAuth2 for secure endpoints using FastAPI’s security utilities.
- **Pagination**: Modify the read_items endpoint to support `skip` and `limit` query parameters for large datasets.
- **Advanced Queries**: Use SQLAlchemy’s ORM for complex queries (e.g., filtering by price or availability).
- **Deployment**: Deploy your app to a platform like Render or AWS, ensuring your PostgreSQL database is accessible.
