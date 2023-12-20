from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    city = Column(String, index=True)
    stadium = Column(String, index=True)
    founded_year = Column(Integer,  index=True)

    # Define relationship for team and players models
    players = relationship("Player", back_populates="team", cascade="all, delete-orphan")
    coaches = relationship("Coach", back_populates="team", cascade="all, delete-orphan")


class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String,  index=True)
    last_name = Column(String,  index=True)
    position = Column(String,  index=True)
    nationality = Column(String,  index=True)
    number = Column(Integer,  index=True)
    birthdate = Column(String, nullable=True)

    # Foreign Key player --> team
    team_id = Column(Integer, ForeignKey("teams.id"))
    # Define relationship for team and players models
    team = relationship("Team", back_populates="players")


class Coach(Base):
    __tablename__ = "coaches"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    role = Column(String, index=True)

    # Foreign key to connect Coach to Team
    team_id = Column(Integer, ForeignKey('teams.id'))

    # Define a back-reference to the Team model
    team = relationship("Team", back_populates="coaches")
