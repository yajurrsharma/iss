from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from track import process

app = FastAPI()

@app.post("/api/track")
def track(email: EmailStr = Form(...), lat: float = Form(...), lon: float = Form(...)):
    pass_f, message = process(email, lat, lon)
    
    if not pass_f:
        raise HTTPException(status_code=400, detail=message)
        
    return {"status": "success", "message": message}

    
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
def frontend():
    with open("index.html", "r") as f:
        return HTMLResponse(content=f.read())