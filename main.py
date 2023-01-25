import aiohttp
import asyncio
from sqlalchemy.orm import sessionmaker

from db import Characters, engine


class SwApi():
    def __init__(self):
        self.api_url = 'https://swapi.dev/api'

    def request_people(self, id=None):
        _url = f'{self.api_url}/people'
        if id is not None:
            _url += f'/{id}'
        try:
            response = aiohttp.get(_url)
            response.raise_for_status()
            return response
        except (
            aiohttp.exceptions.InvalidSchema,
            aiohttp.exceptions.ConnectionError,
            aiohttp.exceptions.Timeout,
            aiohttp.exceptions.HTTPError,
        ):
            raise


async def record_sw_character(api:SwApi, id:int, session):
    response = api.request_people(id).json()
    char = Characters(
        id = id,
        birth_year = response['birth_year'],
        eye_color = response['eye_color'],
        films = response['films'],
        gender = response['gender'],
        hair_color = response['hair_color'],
        height = response['height'],
        homeworld = response['homeworld'],
        mass = response['mass'],
        name = response['name'],
        skin_color = response['skin_color'],
        species = response['species'],
        starships = response['starships'],
        vehicles = response['vehicles'],
    )
    session.add(char)
    session.commit()

async def record_all_sw_characters(api, count, Session):
    tasks = set()
    with Session() as session:
        for id in range(1, count+1):
            tasks.add(record_sw_character(api, id, session))
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    api = SwApi()
    count = api.request_people().json()['count']
    Session = sessionmaker(bind=engine)
    try:
        asyncio.run(record_all_sw_characters(api, count, Session))
    except Exception as error:
        print(error)
