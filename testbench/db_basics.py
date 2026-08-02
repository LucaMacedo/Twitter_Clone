# SQLModel arbeitet mit SQLalchemy intern
#from sqlalchemy.ext.declarative import declarative_base # Funkiton für Klasse, um Usertabellen deklarativ erstellen zu können
#from sqlalchemy import Column, Integer, String, Float, create_engine # Spalten für die Tabelle und Datentypen. Engine für DB
#from sqlalchemy.orm import sessionmaker # Session für DB-Operationen
# A database engine (or storage engine) is the underlying software component that a database management system (DBMS) uses to create, read, update and delete (CRUD) data from a database.
from fastapi import FastAPI, Depends, HTTPException # FastAPI ist ein modernes Web-Framework für die Erstellung von APIs mit Python. Es basiert auf Starlette und Pydantic und bietet Funktionen wie automatische Generierung von OpenAPI-Dokumentation, Validierung von Anfragen und Antworten sowie Dependency Injection.
from fastapi.security import OAuth2PasswordRequestForm # OAuth2PasswordRequestForm ist eine Klasse, die von FastAPI bereitgestellt wird und zur Verarbeitung von Formularen für die Authentifizierung verwendet wird. Sie enthält Felder wie "username" und "password", die vom Benutzer ausgefüllt werden müssen.
from pydantic import EmailStr # EmailStr ist ein spezieller Datentyp, der von Pydantic bereitgestellt wird und zur Validierung von E-Mail-Adressen verwendet wird. Er stellt sicher, dass die eingegebene E-Mail-Adresse ein gültiges Format hat.
# BaseModel war auch drin, wird ersetzt durch SQLModel
from sqlmodel import SQLModel, Field, Session, create_engine, UniqueConstraint # SQLModel ist eine Erweiterung von Pydantic, die speziell für die Arbeit mit SQL-Datenbanken entwickelt wurde. 
#Es ermöglicht die Definition von Datenmodellen, die sowohl für die Validierung von Daten als auch für die Interaktion mit der Datenbank verwendet werden können. 
# Field wird verwendet, um zusätzliche Informationen über die Felder in einem SQLModel bereitzustellen, wie z.B. den Primärschlüssel oder die Spaltennamen.
from typing import Optional
from pydantic import validator # validere PW
import bcrypt
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

class UserBase(SQLModel): # leichter Switch ziwschen pydantic und sqqlchemy, 
    #da SQLModel von beiden erbt. Es definiert die Datenstruktur für die Benutzerdaten, die in der API verwendet wird.
    # sqlchemy legt id selbst an
    firstname: str
    lastname: str
    username: str
    email: EmailStr
    password: str
    age: int

class UserCreate(UserBase):
    repeat_password: str
    @validator("repeat_password") # validiert das repeat_password Feld
    def repeat_password_must_match(cls, v, values):
        print(v) # str von repat pw
        print(values) # dict von allen anderen Feldern in UserBase

        if v != values["password"]:
            raise ValueError("Passwords must match")
        return v
    
class UserTable(UserBase,table=True):
    __tablename__ = "users" # Name der Tabelle in der Datenbank
    __table_args__ = (UniqueConstraint("email"), UniqueConstraint("username")) # E-Mail muss eindeutig sein
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

def get_session(): # für Dependency Injection. FastAPI kann diese Funktion aufrufen, um eine Session zu erstellen und sie an die Endpunkte weiterzugeben.
    with Session(engine) as session:
        yield session # mit reurn nur Objekt aber keinen neuen Context

@app.post("/register/", status_code=201)
def create_user(user: UserCreate, session: Session = Depends(get_session)): # Dependency Injection. FastAPI ruft die get_session-Funktion auf, um eine Session zu erstellen und sie an den Endpunkt weiterzugeben.
    user.password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()) # Passwort wird gehashed, bevor es in der Datenbank gespeichert wird. encode() wandelt den String in Bytes um, da bcrypt nur Bytes akzeptiert.
    new_user = UserTable.from_orm(user) # Übergabe in pydantic Modell
    # keine Umwandlung in dict mehr
    #new_user = UserTable(**user.dict()) # dict() konvertiert das Pydantic-Modell in ein Dictionary, das dann an den Konstruktor der User-Klasse übergeben wird.
    #** entpackt dict. Bsp: name: "John", usw. Dict wird nicht komplett übergeben
    #Er sorgt dafür, dass die Verbindung zur Datenbank ordnungsgemäß verwaltet wird, auch wenn Fehler auftreten.
    session.add(new_user)
    session.commit()
    # srogt dafür, dass kein Server Error auftretet    
    session.refresh(new_user) # Aktualisiert das new_user-Objekt mit den Daten aus der Datenbank, einschließlich der automatisch generierten ID.
    return {"id": new_user.id, "message": "User erfolgreich registriert"}

@app.post("/login/")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    db_user = session.query(UserTable).filter(UserTable.username == form_data.username).first() # sucht user in db
    if not db_user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not bcrypt.checkpw(form_data.password.encode("utf-8"), db_user.password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return {"user": f"Eingeloggt als {db_user.username }"}

@app.get("/users/")
def get_all_users(session: Session = Depends(get_session)):
    users = session.query(UserTable).all()
    return users

@app.on_event("startup") #hook
def on_startup():
    create_db_and_table() # wird immer bei start ausgeführt