from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from app.routers import messages
from app.db import Base, engine, get_db

app = FastAPI(title="Messaging Service")


Base.metadata.create_all(bind=engine)

app.include_router(messages.router)


@app.get("/")
def read_root():
    """
    default route.
    """
    return {"message": "Server is up and running"}


@app.get("/schema")
def get_schema(db: Session = Depends(get_db)):
    """
    Endpoint to inspect and return the database schema.
    """
    inspector = inspect(db.bind)
    schema = {}
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        schema[table_name] = [
            {"name": col["name"], "type": str(col["type"])} for col in columns
        ]
    return schema
