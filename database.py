from sqlmodel import SQLModel, create_engine, Session
engine=create_engine("sqlite:///./database.db", echo=True)
SQLModel.metadata.create_all(engine)
def create_db():
    SQLModel.metadata.create_all(engine)
def get_db():
    with Session(engine)as session:
        yield session