# Fastr

Recreate the [Flask tutorial](https://flask.palletsprojects.com/en/2.0.x/tutorial/index.html) in FastAPI.

The app is named Fastr.
It is a simple web app that allows user to register, log in, and create posts on a simple page.
It creates and accesses a local SQLite database.

![Example homepage for Fastr app](img/fastr_homepage.png?raw=true)

The Fastr app has all the functionality of the Flaskr app created in the Flask tutorial and a full suite of unit tests.
The only piece of the Flask tutorial that is not currently implemented is the packaging piece (from the "Make the Project Installable" section of the Flask tutorial).

For additional commentary on this FastAPI implementation vs. the original Flask app, see the post on Towards Data Science [here](https://towardsdatascience.com/using-fastapi-to-recreate-the-flask-tutorial-ee19ab135eed) (or use [this link](https://medium.com/@djcunningham0/ee19ab135eed?source=friends_link&sk=eb20704515eeca89b601b67043e75008) if you hit a paywall with the first one).

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
Please ensure that all tests pass and new tests are written for any new functionality before submitting a PR.
