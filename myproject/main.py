# Imports
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import os
import crud
import models
import schemas
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import auth
from database import SessionLocal, engine
from typing import List


# Database Initialization
print("We are in the main.......")
if not os.path.exists('.\sqlitedb'):
    print("Making folder.......")
    os.makedirs('.\sqlitedb')

print("Creating tables.......")
models.Base.metadata.create_all(bind=engine)
print("Tables created.......")

# FastAPI App Setup
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://localhost.tiangolo.com",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #Try to authenticate the user
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Add the JWT case sub with the subject(user)
    access_token = auth.create_access_token(
        data={"sub": user.email}
    )
    #Return the JWT as a bearer token to be placed in the headers
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# GET Endpoints
@app.get("/teams/{team_id}", response_model=schemas.Team)
def get_specific_team(team_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    team = crud.get_team(db, team_id)
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return team


@app.get("/players/{player_id}", response_model=schemas.Player)
def get_specific_player(player_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    player = crud.get_player(db, player_id)
    if player is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
    return player


@app.get("/coaches/{coach_id}", response_model=schemas.Coach)
def get_specific_coach(coach_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    coach = crud.get_coach(db, coach_id)
    if coach is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coach not found")
    return coach


@app.get("/teams/", response_model=List[schemas.Team])
def get_all_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return crud.get_teams(db, skip=skip, limit=limit)


@app.get("/players/", response_model=List[schemas.Player])
def get_all_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return crud.get_players(db, skip=skip, limit=limit)


@app.get("/coaches/", response_model=List[schemas.Coach])
def get_all_coaches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return crud.get_coaches(db, skip=skip, limit=limit)


# POST Endpoints
@app.post("/teams/", response_model=schemas.Team)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return crud.create_team(db, team)


@app.post("/players/{team_id}", response_model=schemas.Player)
def create_player(team_id: int, player: schemas.PlayerCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return crud.create_player(db, player, team_id)


@app.post("/coaches/{team_id}", response_model=schemas.Coach)
def create_coach(team_id: int, coach: schemas.CoachCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return crud.create_coach(db, coach, team_id)


# DELETE Endpoints
@app.delete("/teams/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not crud.remove_team(db, team_id):
        raise HTTPException(status_code=404, detail="Team not found")
    return {"message": "Team (Including Players and Coaches) deleted"}


@app.delete("/players/{player_id}")
def delete_player(player_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not crud.remove_player(db, player_id):
        raise HTTPException(status_code=404, detail="Player not found")
    return {"message": "Player deleted"}


@app.delete("/coaches/{coach_id}")
def delete_coach(coach_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not crud.remove_coach(db, coach_id):
        raise HTTPException(status_code=404, detail="Coach not found")
    return {"message": "Coach deleted"}
