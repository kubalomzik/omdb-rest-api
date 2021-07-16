import json
import os

import requests

from base import engine, Base
from movie_db import Movie, Comment

omdb_key = os.getenv("OMDB_API_KEY")


class Serialization:

    def _change_object_list_to_dict(self, object_list):
        response = list()
        for object in object_list:
            object_dict = object.__dict__
            del object_dict['_sa_instance_state']
            response.append(object_dict)

        return response

    def _change_object_to_dict(self, object):
        object_dict = object.__dict__
        del object_dict['_sa_instance_state']

        return object_dict


class FindMovie:

    def __init__(self, session):
        self.session = session

    def fetch_movie_by_name(self, movie_name):

        if movie_name is not None:
            url = ("http://www.omdbapi.com/?apikey=%s&t=%s" % (omdb_key, movie_name))
            response = requests.get(url)
            data = json.loads(response.text)
            error = data.get("Error")

            if error is None:
                movie_title = data.get("Title")
                self._save_movie_to_database_if_movie_not_exists(movie_title)

        else:
            data = {"error": "Invalid request"}

        return data

    def _save_movie_to_database(self, movie_title):

        Base.metadata.create_all(engine)
        movie = Movie(movie_title)
        self.session.add(movie)
        self.session.commit()

    def _save_movie_to_database_if_movie_not_exists(self, movie_title):

        if self._check_if_movie_exists(movie_title) is None:
            self._save_movie_to_database(movie_title)

    def _check_if_movie_exists(self, movie_title):

        movie_duplicate = self.session.query(Movie.movie_name).filter_by(movie_name=movie_title).scalar()

        return movie_duplicate


class ShowMovies(Serialization):

    def __init__(self, session):
        self.session = session

    def show_movie_database(self):
        movies = self.session.query(Movie).all()

        return self._change_object_list_to_dict(movies)


class AddComment(Serialization):

    def __init__(self, session):
        self.session = session

    def save_comment_to_database(self, comment, movie_id):
        commented_movie = self._find_movie_by_id(movie_id)
        Base.metadata.create_all(engine)
        comment = Comment(comment, movie_id, commented_movie)
        self.session.add(comment)
        self.session.commit()

    def _find_movie_by_id(self, movie_id):
        commented_movie = self.session.query(Movie.movie_name).filter(Movie.id == movie_id).scalar()

        return commented_movie

    def show_added_comment(self):
        comment = self.session.query(Comment).order_by(Comment.id.desc()).first()

        return self._change_object_to_dict(comment)


class ShowComments(Serialization):

    def __init__(self, session):
        self.session = session

    def show_comment_database(self, movie_id):

        if movie_id is None:
            comments = self.session.query(Comment).all()

        else:
            comments = self._filter_comments_by_id(movie_id)

        return self._change_object_list_to_dict(comments)

    def _filter_comments_by_id(self, movie_id):

        comments = self.session.query(Comment).filter(Comment.movie_id == movie_id).all()

        return comments
