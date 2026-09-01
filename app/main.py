from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.db.database import engine
from app.api import tasks,auth
from app.core.limiter import limiter
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="Task Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173","http://localhost:56986"],
    allow_credentials=True,allow_methods=["*"],
    allow_headers=["*"])

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(tasks.router,prefix="/api")
app.include_router(auth.router,prefix="/api")

## Templating Jinja2
templates = Jinja2Templates(directory="app/templates")
app.mount("/static",StaticFiles(directory="app/static"),name="static")

## Frontend Pages
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={})

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={})

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html", context={})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html", context={})

## Backend Endpoints
@app.get("/")
def root():
    return {"message": "Welcome to Task Manager API"}

@app.get("/db_test")
def testdb():
    with engine.connect() as connection:
        result = connection.execute(text("select 01"))
        return {"result": result.scalar()}