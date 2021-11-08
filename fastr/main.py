from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from fastr import auth, blog
from fastr.db import models
from fastr.db.database import engine
from fastr.config import Settings


# create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

settings = Settings()
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

app.mount("/static", StaticFiles(directory="fastr/static"), name="static")
app.include_router(auth.router)
app.include_router(blog.router)


@app.get("/hello", response_class=HTMLResponse)
async def hello() -> str:
    """A simple page that says hello"""
    return "Hello, World!"


@app.exception_handler(blog.RequiresLoginException)
def exception_handler(request: Request, exc: blog.RequiresLoginException) -> Response:
    """
    Redirect to login screen if someone tries to access a view that requires login.

    Workaround suggested in a GitHub comment here:
    https://github.com/tiangolo/fastapi/issues/1039#issuecomment-591661667
    """
    return RedirectResponse(url="/auth/login", status_code=302)
