from pydantic import BaseModel
from typing import List, Optional

# User Schemas


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


# Player Schemas
class PlayerBase(BaseModel):
    first_name: str
    last_name: str
    position: str
    nationality: str
    number: int
    birthdate: str


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int
    team_id: int

    class Config:
        orm_mode = True

# Coach Schemas
class CoachBase(BaseModel):
    first_name: str
    last_name: str
    role: str


class CoachCreate(CoachBase):
    pass


class Coach(CoachBase):
    id: int
    team_id: int

    class Config:
        orm_mode = True


# Team Schemas
class TeamBase(BaseModel):
    name: str
    city: str
    stadium: str
    founded_year: int


class TeamCreate(TeamBase):
    pass


class Team(TeamBase):
    id: int
    players: List[Player] = []
    coaches: List[Coach] = []

    class Config:
        orm_mode = True


