from fastapi import FastAPI, Request
import models
from database import engine
from routers import auth, todos
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

template = Jinja2Templates(directory='Template')

#To find css file in static directory
app.mount("/static", StaticFiles(directory="Static"), name="static")


@app.get('/')
def test_html(request: Request):
    return template.TemplateResponse("home.html", {"request": request})


app.include_router(auth.router)
app.include_router(todos.router)

