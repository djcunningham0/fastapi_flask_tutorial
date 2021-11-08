# Fastr

Recreate the [Flask tutorial](https://flask.palletsprojects.com/en/2.0.x/tutorial/index.html) in FastAPI.
A simple web app that allows user to register, log in, and create posts on a simple page.

## How to run the app

First clone this repository.
Then install the requirements (preferably in a virtual environment):
```
pip install -r requirements.txt
```

From the root directory, use the following command to run the app with uvicorn:
```
uvicorn fastr.main:app --reload
```

(omit the `--reload` argument if you don't want the app to refresh when changes are made to the code)

## Contributing

If you have suggestions for better ways to implement any of the functionality using FastAPI, feel free to open an issue and/or submit a pull request.
Code should be simple and beginner-friendly.