from sqlalchemy import Column, String, Integer, ForeignKey

from base import Base


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    movie_name = Column(String)

    def __init__(self, movie_name):
        self.movie_name = movie_name


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    comment = Column(String)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    commented_movie = Column(String, ForeignKey('movies.movie_name'))

    def __init__(self, comment, movie_id, commented_movie):
        self.comment = comment
        self.movie_id = movie_id
        self.commented_movie = commented_movie
