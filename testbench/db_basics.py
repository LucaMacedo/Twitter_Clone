# SQLModel arbeitet mit SQLalchemy intern
#from sqlalchemy.ext.declarative import declarative_base # Funkiton für Klasse, um Usertabellen deklarativ erstellen zu können
#from sqlalchemy import Column, Integer, String, Float, create_engine # Spalten für die Tabelle und Datentypen. Engine für DB
#from sqlalchemy.orm import sessionmaker # Session für DB-Operationen
# A database engine (or storage engine) is the underlying software component that a database management system (DBMS) uses to create, read, update and delete (CRUD) data from a database.
from fastapi import FastAPI
from pydantic import EmailStr # EmailStr ist ein spezieller Datentyp, der von Pydantic bereitgestellt wird und zur Validierung von E-Mail-Adressen verwendet wird. Er stellt sicher, dass die eingegebene E-Mail-Adresse ein gültiges Format hat.
# BaseModel war auch drin, wird ersetzt durch SQLModel
from sqlmodel import SQLModel, Field, Session, create_engine # SQLModel ist eine Erweiterung von Pydantic, die speziell für die Arbeit mit SQL-Datenbanken entwickelt wurde. 
#Es ermöglicht die Definition von Datenmodellen, die sowohl für die Validierung von Daten als auch für die Interaktion mit der Datenbank verwendet werden können. 
# Field wird verwendet, um zusätzliche Informationen über die Felder in einem SQLModel bereitzustellen, wie z.B. den Primärschlüssel oder die Spaltennamen.
from typing import Optional

engine = create_engine("sqlite:///users.db")
#Base = declarative_base() # Base-Klasse für die Deklaration der Tabellen. Ersetzt durch SQLModel, da SQLModel von Base erbt und die gleiche Funktionalität bietet.

app = FastAPI()

# Nicht mehr nötig wegen User Table
# class User(Base): # User-Klasse, die von Base erbt. Sie repräsentiert die Tabelle "users" in der Datenbank.
#     __tablename__ = "users" 

#     id = Column(Integer, primary_key=True)# Primärschlüssel
#     firstname = Column(String)
#     lastname = Column(String)
#     email = Column(String)
#     password = Column(String)
#     age = Column(Integer)

def create_db_and_table():
    SQLModel.metadata.create_all(engine) # erstellt die Tabelle in der Datenbank, wenn sie noch nicht existiert   

class UserModel(SQLModel): # leichter Switch ziwschen pydantic und sqqlchemy, 
    #da SQLModel von beiden erbt. Es definiert die Datenstruktur für die Benutzerdaten, die in der API verwendet wird.
    # sqlchemy legt id selbst an
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    age: int

class UserTable(UserModel,table=True):
    id: Optional[int] = Field(default=None, primary_key=True) # Äquivalent zur id von oben

# Ersetzt durch Context Manager
# Session = sessionmaker(bind=engine) # Session-Klasse, die an die Engine gebunden ist. Sie ermöglicht es uns, Transaktionen mit der Datenbank durchzuführen.
# session = Session()
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
    new_user = UserTable.from_orm(user) # Übergabe in pydantic Modell
    # keine Umwandlung in dict mehr
    #new_user = UserTable(**user.dict()) # dict() konvertiert das Pydantic-Modell in ein Dictionary, das dann an den Konstruktor der User-Klasse übergeben wird.
    #** entpackt dict. Bsp: name: "John", usw. Dict wird nicht komplett übergeben
    with Session(engine) as session: # Context Manager, der automatisch die Session öffnet und schließt. 
    #Er sorgt dafür, dass die Verbindung zur Datenbank ordnungsgemäß verwaltet wird, auch wenn Fehler auftreten.
        session.add(new_user)
        session.commit()
        # srogt dafür, dass kein Server Error auftretet    
        session.refresh(new_user) # Aktualisiert das new_user-Objekt mit den Daten aus der Datenbank, einschließlich der automatisch generierten ID.
    return {"id": new_user.id, "message": "User erfolgreich registriert"}

@app.get("/users/")
def get_all_users():
    with Session(engine) as session:
        users = session.query(UserTable).all()
        return users

@app.on_event("startup") #hook
def on_startup():
    create_db_and_table() # wird immer bei start ausgeführt