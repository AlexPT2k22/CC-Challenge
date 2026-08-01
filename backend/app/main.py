from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app.db import get_connection
from pydantic import BaseModel, Field
from datetime import date
from app.config import settings

app = FastAPI(
    title="Sewage Pipe Project Challenge API",
    description="Starter API for the coding challenge.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProjectCreate(BaseModel):
    id: int = Field(gt=0)
    customer_id: int = Field(gt=0)
    date: date
    task: str
    location: str = None
    description: str = None
    status: str
    


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/projects", status_code=status.HTTP_200_OK)
async def get_projects(status: str = None ):
    "Gets all projects on the database"
    if status:
        query = f"SELECT * FROM projects WHERE status = \u0027{status}\u0027 ORDER BY date DESC"
    else:
        query = "SELECT * FROM projects ORDER BY date DESC"
    async with get_connection() as connection:
        async with connection.cursor() as cursor:
            try:   
                await cursor.execute(query)
                response = await cursor.fetchall()
                return response
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Bad request: {str(e)} \n Is the database online?")
        
@app.post("/projects", status_code=status.HTTP_201_CREATED)
async def add_project(project: ProjectCreate):
    "Adds a project"
    query = "INSERT INTO projects (id, customer_id, date, task, location, description, status) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *"
    params = (project.id, project.customer_id, project.date, project.task, project.location, project.description, project.status)
    async with get_connection() as connection:
        async with connection.cursor() as cursor:
            try:
                await cursor.execute(query, params)
                response = await cursor.fetchone()
                await connection.commit()
                return response
            except Exception as e:
                await connection.rollback()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))