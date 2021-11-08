from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from fastr.db.database import get_db
from fastr.db import crud, schemas, models


router = APIRouter(tags=["blog"])
templates = Jinja2Templates(directory=str("fastr/templates"))


# https://github.com/tiangolo/fastapi/issues/1039#issuecomment-591661667
class RequiresLoginException(Exception):
    """
    Used in conjunction with login_required to ensure user is logged in before
    accessing certain views.

    Workaround suggested in a GitHub comment here:
    https://github.com/tiangolo/fastapi/issues/1039#issuecomment-591661667
    """
    pass


def login_required(request: Request):
    """Ensure a user is logged in."""
    if not request.session.get("user"):
        raise RequiresLoginException


@router.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    """Show all the posts, most recent first."""
    posts = crud.get_posts(db)
    return templates.TemplateResponse(
        "blog/index.html", {"request": request, "posts": posts}
    )


@router.get(
    "/create", dependencies=[Depends(login_required)], response_class=HTMLResponse
)
def create_page(request: Request):
    """Create post page."""
    return templates.TemplateResponse("blog/create.html", {"request": request})


@router.post(
    "/create", dependencies=[Depends(login_required)], response_class=HTMLResponse
)
def create_post(
    request: Request,
    title: str = Form(...),
    body: str = Form(""),
    db: Session = Depends(get_db),
):
    """
    Create a new post for the current user.

    Note: title is specified as a required field, so FastAPI's input validation will
    make sure it is populated. No need for an explicit check that it is not None or "".
    """
    post = schemas.Post(title=title, body=body)
    crud.create_post(db=db, create_data=post, user_id=request.session["user"]["id"])
    return RedirectResponse("/", status_code=302)


@router.get(
    "/{id}/update", dependencies=[Depends(login_required)], response_class=HTMLResponse
)
def update_page(request: Request, id: int, db: Session = Depends(get_db)):
    """Update post page."""
    post = get_and_validate_post(id=id, db=db, request=request)
    return templates.TemplateResponse(
        "blog/update.html", {"request": request, "post": post}
    )


@router.post(
    "/{id}/update", dependencies=[Depends(login_required)], response_class=HTMLResponse
)
def update_post(
    request: Request,
    id: int,
    title: str = Form(...),
    body: str = Form(""),
    db: Session = Depends(get_db),
):
    """
    Update an existing post that was created by the logged in user.

    Note: title is specified as a required field, so FastAPI's input validation will
    make sure it is populated. No need for an explicit check that it is not None or "".
    """
    get_and_validate_post(id=id, db=db, request=request)

    update_data = schemas.PostUpdate(id=id, title=title, body=body)
    crud.update_post(db, update_data)
    return RedirectResponse("/", status_code=302)


@router.post(
    "/{id}/delete", dependencies=[Depends(login_required)], response_class=HTMLResponse
)
def delete_post(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
):
    """Delete a post that was created by the logged in user."""
    get_and_validate_post(id=id, db=db, request=request)
    crud.delete_post(db, post_id=id)
    return RedirectResponse("/", status_code=302)


def get_and_validate_post(
    id: int,
    db: Session,
    request: Request,
    check_author: bool = True,
) -> models.Post:
    """
    Retrieve a post by id. Validate that it exists and was created by the logged in
    user.

    Parameters
    ----------
    id
        id of post we were looking for
    db
        database from get_db
    request
        API request
    check_author
        require the current user to be the author

    Returns
    -------
    The post data

    Raises
    ------
    404
        if a post with the given id doesn't exist
    403
        if the current user isn't the author
    """
    post = crud.get_post_by_id(db, id)
    if post is None:
        raise HTTPException(404, f"Post id {id} doesn't exist.")

    user = schemas.LoggedInUser(**request.session.get("user", {}))
    if check_author and post.author_id != user.id:
        raise HTTPException(
            403,
            f"Post {id} was not posted by currently logged in user ({user.username}).",
        )

    return post
