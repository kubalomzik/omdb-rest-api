# OMDb REST API

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This project is a REST API based on [OMDb API](https://www.omdbapi.com/) web service.

## Technologies
* Python 3.9
* Flask 2.0.1
* SQLAlchemy 1.4.21
* SQLite 3.31.1

## Setup
The project requires software mentioned in [Technologies](#technologies). Generate your own free API Key from OMDb here: [API Key](http://www.omdbapi.com/apikey.aspx).
Two additonal files containing environment variables should be located in the project's folder:

**.env**
```
OMDB_API_KEY=your_key
```

**.flaskenv**
```
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True
```
