# API Router: Routes logisch bündeln (z.B Anlgeug und Löschen von User).
from fastapi import FastAPI, BackgroundTasks, Request
import time
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stdout
)
app = FastAPI()

@app.middleware("http")
async def performance_middle(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    end_time = time.perf_counter()
    logging.info(f"Dauer in Sekunden: {end_time - start_time} für {request.url.path}")
    return response

def send_mail(email: str, message: str):
    with open("log.txt", mode="w") as email_file:
        content = f"Nachricht für {email}: {message}"
        email_file.write(content)

# Background Task läuft im Hintergrund einer HTTP-Anfrage. Z.B. E-Mail versenden, wenn ein User sich registriert.
@app.post("/nachricht/{email}")
async def sende_nachricht(email: str, background_task: BackgroundTasks):
    background_task.add_task(send_mail, email, message="Bestellung aufgegeben")
    return {"message": f"Email ist an {email} verschickt worden"}
