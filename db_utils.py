from database import SessionLocal
from models import House, Key
from sqlalchemy.future import select, delete

async def add_house(name, owner_id, text_channel_id, voice_channel_id):
    async with SessionLocal() as session:
        new_house = House(name=name, owner_id=owner_id, text_channel_id=text_channel_id, voice_channel_id=voice_channel_id)
        session.add(new_house)
        await session.commit()

async def get_house_by_name(name):
    async with SessionLocal() as session:
        result = await session.execute(select(House).filter(House.name == name))
        return result.scalars().first()

async def add_key(house_id, user_id, role_id):
    async with SessionLocal() as session:
        new_key = Key(house_id=house_id, user_id=user_id, role_id=role_id)
        session.add(new_key)
        await session.commit()

async def remove_key(user_id):
    async with SessionLocal() as session:
        await session.execute(delete(Key).where(Key.user_id == user_id))
        await session.commit()
