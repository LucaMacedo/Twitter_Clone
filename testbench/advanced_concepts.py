# API Router: Routes logisch bündeln (z.B Anlgeug und Löschen von User).
from fastapi import FastAPI, APIRouter

app = FastAPI() 
# Router ordnet Funktionen zu einem bestimmten Pfad zu.
router1 = APIRouter(tags=["Auth"])
router2 = APIRouter(tags=["Tweets"])

# Background Task läuft im Hintergrund einer HTTP-Anfrage. Z.B. E-Mail versenden, wenn ein User sich registriert.
@router1.get("/hello")
def hello_world():
    return {"message": "Hello World"}

@router1.get("/hello2")
def hello_world():
    return {"message": "Hello World2"}

@router2.get("/hello3")
def hello_world():
    return {"message": "Hello World3"}

@router2.get("/hello4")
def hello_world():
    return {"message": "Hello World4"}

app.include_router(router1)
app.include_router(router2)