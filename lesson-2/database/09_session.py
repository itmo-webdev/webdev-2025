# Сессия без автокоммита
engine = create_engine("postgresql+asyncpg://user:admin@localhost:5432/webdev")
Session = sessionmaker(engine)
with Session() as session:
    session.add(some_object)
    session.commit()

# Сессия с автокоммитом
engine = create_engine("postgresql+asyncpg://user:admin@localhost:5432/webdev").execution_options(isolation_level="AUTOCOMMIT")
Session = sessionmaker(engine)
with Session() as session:
    session.add(some_object)


    