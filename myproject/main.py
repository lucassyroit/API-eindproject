# Imports
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import os
# import crud
# import models
# import schemas
# from database import SessionLocal, engine
# from typing import List

# Database Initialization
if not os.path.exists('.\sqlitedb'):
    os.makedirs('.\sqlitedb')
models.Base.metadata.create_all(bind=engine)

# FastAPI App Setup
app = FastAPI()

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()