from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey
from database import Base

class House(Base):
    __tablename__ = "houses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    owner_id = Column(BigInteger, nullable=False)
    text_channel_id = Column(BigInteger, nullable=False)
    voice_channel_id = Column(BigInteger, nullable=False)

class Key(Base):
    __tablename__ = "keys"
    id = Column(Integer, primary_key=True, index=True)
    house_id = Column(Integer, ForeignKey('houses.id'))
    user_id = Column(BigInteger, nullable=False)
    role_id = Column(BigInteger, nullable=False)
