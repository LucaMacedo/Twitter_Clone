from sqlalchemy.ext.declarative import declarative_base # Funkiton für Klasse, um Usertabellen deklarativ erstellen zu können
from sqlalchemy import Column, Integer, String, Float, create_engine # Spalten für die Tabelle und Datentypen. Engine für DB
from sqlalchemy.orm import sessionmaker # Session für DB-Operationen
# A database engine (or storage engine) is the underlying software component that a database management system (DBMS) uses to create, read, update and delete (CRUD) data from a database.
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr # EmailStr ist ein spezieller Datentyp, der von Pydantic bereitgestellt wird und zur Validierung von E-Mail-Adressen verwendet wird. Er stellt sicher, dass die eingegebene E-Mail-Adresse ein gültiges Format hat.

engine = create_engine("sqlite:///users.db")
Base = declarative_base() # Base-Klasse für die Deklaration der Tabellen

app = FastAPI()

class User(Base): # User-Klasse, die von Base erbt. Sie repräsentiert die Tabelle "users" in der Datenbank.
    __tablename__ = "users" 

    id = Column(Integer, primary_key=True)# Primärschlüssel
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String)
    password = Column(String)
    age = Column(Integer)

class UserModel(BaseModel):
    # sqlchemy legt id selbst an
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    age: int

Base.metadata.create_all(engine) # erstellt die Tabelle in der Datenbank, wenn sie noch nicht existiert   
Session = sessionmaker(bind=engine) # Session-Klasse, die an die Engine gebunden ist. Sie ermöglicht es uns, Transaktionen mit der Datenbank durchzuführen.
session = Session()
# Ersetzt durch Funktion
# new_user = User(firstname="John", lastname="Doe", email="johndeo@example.com", password="123456", age=30)
# session.add(new_user)
# session.commit()

# # user aus db. Übergib Objekte
# all_users = session.query(User).all()

# for user in all_users:
#     print(user.id, user.firstname, user.lastname)

@app.post("/register/", status_code=201)
def create_user(user: UserModel):
    new_user = User(**user.dict()) # dict() konvertiert das Pydantic-Modell in ein Dictionary, das dann an den Konstruktor der User-Klasse übergeben wird.
    #** entpackt dict. Bsp: name: "John", usw. Dict wird nicht komplett übergeben
    session.add(new_user)
    session.commit()
    return {"id": new_user.id, "message": "User erfolgreich registriert"}