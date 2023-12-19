from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

import auth
import models
import schemas

# User CRUD Operations

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# Team CRUD Operations

def create_team(db: Session, team: schemas.TeamCreate):
    db_team = models.Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Team).offset(skip).limit(limit).all()

def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()

def remove_team(db: Session, team_id: int):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if team:
        db.delete(team)
        db.commit()
        return team
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

# Player CRUD Operations

def create_player(db: Session, player: schemas.PlayerCreate, team_id: int):
    db_player = models.Player(**player.dict(), team_id=team_id)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def get_players(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Player).offset(skip).limit(limit).all()

def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.id == player_id).first()

def remove_player(db: Session, player_id: int):
    player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if player:
        db.delete(player)
        db.commit()
        return player
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")

# Coach CRUD Operations

def create_coach(db: Session, coach: schemas.CoachCreate, team_id: int):
    db_coach = models.Coach(**coach.dict(), team_id=team_id)
    db.add(db_coach)
    db.commit()
    db.refresh(db_coach)
    return db_coach

def get_coaches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Coach).offset(skip).limit(limit).all()

def get_coach(db: Session, coach_id: int):
    return db.query(models.Coach).filter(models.Coach.id == coach_id).first()

def remove_coach(db: Session, coach_id: int):
    coach = db.query(models.Coach).filter(models.Coach.id == coach_id).first()
    if coach:
        db.delete(coach)
        db.commit()
        return coach
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coach not found")