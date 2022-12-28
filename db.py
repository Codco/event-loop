import configparser
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.exc import SQLAlchemyError


Base = declarative_base()

class Characters(Base):
    __tablename__ = 'characters'
    id = sq.Column(sq.Integer, primary_key=True)
    birth_year = sq.Column(sq.String)
    eye_color = sq.Column(sq.String)
    films = sq.Column(sq.String)
    gender = sq.Column(sq.String)
    hair_color = sq.Column(sq.String)
    height = sq.Column(sq.String)
    homeworld = sq.Column(sq.String)
    mass = sq.Column(sq.String)
    name = sq.Column(sq.String)
    skin_color = sq.Column(sq.String)
    species = sq.Column(sq.String)
    starships = sq.Column(sq.String)
    vehicles = sq.Column(sq.String)


config = configparser.ConfigParser()
config.read("db_config.ini")

# DB config:
type=config['DB']['TYPE']
name=config['DB']['NAME']
host=config['DB']['HOST']
port=config['DB']['PORT']
user=config['DB']['USER']
password=config['DB']['PASSWORD']

db = f'{type}://{user}:{password}@{host}:{port}/{name}'
engine = sq.create_engine(db)


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
