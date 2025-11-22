from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

Base = declarative_base(Metadata())

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

Session = sessionmaker()

with Session() as session:
    user = User(name="John")
    # Привязываем объект к сессии, теперь хранится в базе
    session.add(user)
    # Генерируем первичный ключ, отправляем в базу, но он пока не сохраняется
    session.flush()
    # Коммитим
    session.commit()


