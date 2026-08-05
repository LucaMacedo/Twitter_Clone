# API Router: Routes logisch bündeln (z.B Anlgeug und Löschen von User).
from fastapi import FastAPI, BackgroundTasks

description = """
## Items

* **Create User** (_not implemented_).
"""

# Metadaten, die zur App gehören
app = FastAPI(
    title="Unsere Produkt API",
    version="0.2.0",
    description=description,
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "John Doe",
        "email": "entwickler@example.com",
        "url": "http://example.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }
)
def send_mail(email: str, message: str):
    with open("log.txt", mode="w") as email_file:
        content = f"Nachricht für {email}: {message}"
        email_file.write(content)

# Background Task läuft im Hintergrund einer HTTP-Anfrage. Z.B. E-Mail versenden, wenn ein User sich registriert.
@app.post("/nachricht/{email}")
async def sende_nachricht(email: str, background_task: BackgroundTasks):
    background_task.add_task(send_mail, email, message="Bestellung aufgegeben")
    return {"message": f"Email ist an {email} verschickt worden"}
