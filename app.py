import json

from flask import Flask, request

from base import Session
from movie_service import FindMovie, ShowMovies, AddComment, ShowComments

app = Flask(__name__)
app.config.from_pyfile('settings.py')


@app.route('/')
def index():
    return "OMDb API"


@app.route('/movies', methods=['POST', 'GET'])
def find_movie():
    session = None
    movie = None

    try:
        session = Session()
        movie_service = FindMovie(session)
        movie_name = request.args.get('movie_name')
        movie = movie_service.fetch_movie_by_name(movie_name)
    except:
        session.rollback()
    finally:
        session.close()

    return movie


@app.route('/movies/database', methods=['GET'])
def show_movies():
    session = None
    movies = None

    try:
        session = Session()
        movie_service = ShowMovies(session)
        movies = movie_service.show_movie_database()
    except:
        session.rollback()
    finally:
        session.close()

    return json.dumps(movies)


@app.route('/comments', methods=['POST', 'GET'])
def add_comment():
    session = None
    added_comment = None

    try:
        session = Session()
        movie_service = AddComment(session)
        comment = request.args.get('comment')
        movie_id = request.args.get('movie_id')
        movie_service.save_comment_to_database(comment, movie_id)
        added_comment = movie_service.show_added_comment()
    except:
        session.rollback()
    finally:
        session.close()

    return json.dumps(added_comment)


@app.route('/comments/database', methods=['GET'])
def show_comments():
    session = None
    comments = None

    try:
        session = Session()
        movie_service = ShowComments(session)
        movie_id = request.args.get('movie_id')
        comments = movie_service.show_comment_database(movie_id)
    except:
        session.rollback()
    finally:
        session.close()

    return json.dumps(comments)


if __name__ == '__main__':
    app.run(debug=True)
