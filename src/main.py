import src.models as models
from fastapi import FastAPI
from src.database import engine
from src.auth.router import router as auth_router 
# 1. Import the new task router
from src.tasks.router import router as task_router

app = FastAPI(title="Task Tracker API")


try:
    models.Base.metadata.create_all(bind=engine)
    print("Successfully connected and tables created!")
except Exception as e:
    print(f"Error connecting to database: {e}")

app.include_router(auth_router)


app.include_router(task_router)

@app.get("/")
def read_root():
    return {"message": "API is running and Database is connected!"}