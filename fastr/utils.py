from fastapi import Request


def flash(request: Request, error: str):
    """
    Recreate the flash function from Flask. Store error messages in the "flashes" key
    of the session so that all flashed messages can be displayed in a view.

    Parameters
    ----------
    request
        a fastapi request object
    error
        the error message to flash
    """
    request.session["flashes"] = request.session.get("flashes", []) + [error]
