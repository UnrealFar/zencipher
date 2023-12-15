import os
import fastapi
from fastapi import Depends, Request, Header
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from starlette import status
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
from mongo import create_user, get_user
from utils import encrypt, decrypt, check_password
from uvicorn import run

from typing import Union, Optional

app = fastapi.FastAPI(
    title="ZenCipher",
)
app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ["SECRET_KEY"]
) #type: ignore
app.mount("/static", StaticFiles(directory="static"), name="static")
app.title = "ZenCipher"
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(
    request: Request,
):
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": app.title, "username":request.session.get("username")}
    )


@app.get(
    "/login",
)
async def login_page(request: Request, err: Optional[str] = None):
    return templates.TemplateResponse(
        "login.html", {
            "request": request, "err": err}
    )


@app.post("/_login", response_class=HTMLResponse)
async def _login(request: Request):
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")
    acc = await get_user(username=username.lower())
    if not acc:
        return RedirectResponse(url="/login?err=User not found",
                                status_code=status.HTTP_302_FOUND)
    if check_password(password, acc.password):
        request.session["password"] = acc.password
        request.session["username"] = acc.username
        return RedirectResponse(url="/",status_code=status.HTTP_302_FOUND)
    else:
        return RedirectResponse(url="/login?err=Wrong password",status_code=status.HTTP_302_FOUND)


@app.get("/register", response_class=HTMLResponse)
async def register(request: Request, err: Optional[str] = None):
    return templates.TemplateResponse(
        "register.html",
        {
            "request": request,
            "title": app.title,
            "err": err,
        },
    )


@app.post("/_register", response_class=HTMLResponse)
async def _register(request: Request):
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")
    email = form_data.get("email")
    acc = await get_user(username=username)
    if acc:
        return RedirectResponse(
            url="/register?err=User with that username already exists",status_code=status.HTTP_302_FOUND
        )
    acc = await create_user(username, password, email)
    return RedirectResponse(url="/login",status_code=status.HTTP_302_FOUND)


@app.get("/logout")
async def logout(request: Request):
    request.session.pop("username",None)
    request.session.pop("password",None)
    return RedirectResponse(url="/login")


@app.get("/passwords", response_class=HTMLResponse)
async def passwords(
    request: Request,
):
    username = request.session.get("username")
    password = request.session.get("password")
    user = await get_user(username = username, password = password)
    if not user:
        return RedirectResponse(url="/login")
    passwords = await user.passwords()
    return templates.TemplateResponse(
        "passwords.html",
        {
            "request": request,
            "title": app.title,
            "passwords": passwords,
            "len": passwords,
        },
    )


# API Routes below
# TODO: Move the API routes into a new file.


class _Acc(BaseModel):
    username: str
    password: str
    email: str


@app.post("/api/v1/create_account")
async def create_account(acc: _Acc):
    user = await create_user(acc.username, acc.password, acc.email)
    return {
        "message": "Make sure to store the key somewhere safe",
        "data": {"key": user.key},
    }


class _Pass(BaseModel):
    title: str
    username: str
    password: str
    note: Union[str, None] = None


@app.post("/api/v1/new_password")
async def new_password(
    request: Request,
    back: Optional[str] = None,
    x_username: Optional[str] = Header(None),
    x_password: Optional[str] = Header(None),
    content_type: str = Header()
):
    username = x_username or request.session.get("username")
    password = x_password or request.session.get("password")
    if password is None:
        return {"message": "No authorization token provided"}
    user = await get_user(username=username,password=password)
    if user is None:
        return {"message": "Invalid authorization token"}
    if content_type == "application/json":
        pa = await request.json()
    elif content_type.startswith("multipart/form-data"):
        pa = await request.form()
    else:
        print(content_type)
        return {"message": "Invalid content type"}
    p = await user.new_password(pa['title'], pa['username'], pa['password'], pa['note'])
    if back:
        return RedirectResponse(
            url=back, status_code=status.HTTP_302_FOUND
        )
    return {"message": "Password details successfully created!"}


@app.get("/api/v1/all_passwords")
async def all_passwords(
    x_authorization=Header(),
):
    if x_authorization is None:
        return {"message": "No authorization token provided"}
    user = await get_user(key=x_authorization)
    if user is None:
        return {"message": "Invalid authorization token"}
    return {
        "message": "Successfully retrieved all passwords",
        "data": await user.passwords(),
    }


run(app, host="0.0.0.0", port=8080)
