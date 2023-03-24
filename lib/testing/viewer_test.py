import pytest

from classes.Movie import Movie
from classes.Viewer import Viewer
from classes.Review import Review


class TestViewer:
    '''Viewer in viewer.py'''

    def test_has_username(self):
        '''has the username passed into __init__.'''
        viewer = Viewer(username="gustave_the_cat")
        assert viewer.username == "gustave_the_cat"

    def test_requires_username_between_6_and_16_characters(self):
        '''requires titles to be strings between 6 and 16 characters, inclusive.'''
        viewer = Viewer("code-blooded")
        viewer_2 = Viewer(123)
        viewer_3 = Viewer('abcde')
        assert hasattr(viewer, "_username")
        assert not hasattr(viewer_2, "_username")
        assert not hasattr(viewer_3, "_username")
        assert viewer.username == "code-blooded"
        # with pytest.raises(Exception):
        #     Viewer(username="abcde")
        # with pytest.raises(Exception):
        #     Viewer(username=123456)

    def test_has_reviews(self):
        '''has a method reviews() that returns a list of reviews for the viewer.'''
        viewer = Viewer(username="fabio_the_hmstr")
        viewer_2 = Viewer(username="Apollo")
        movie = Movie("Finding Nemo")
        review_1 = Review(viewer, movie, 5)
        review_2 = Review(viewer, movie, 5)
        review_3 = Review(viewer_2, movie, 5)
        assert review_1 in viewer.reviews()
        assert review_2 in viewer.reviews()
        assert not review_3 in viewer.reviews()
        assert isinstance(viewer.reviews(), list)

    def test_has_reviewed_movies(self):
        '''has a method reviewed_movies() that returns a list of reviewed movies.'''
        viewer = Viewer(username="Apollo")
        movie = Movie("Finding Nemo")
        movie_2 = Movie("Airbuddies")
        review = Review(viewer, movie_2, 5)
        assert movie_2 in viewer.reviewed_movies()
        assert not movie in viewer.reviewed_movies()
        assert isinstance(viewer.reviewed_movies(), list)

    def test_checks_if_reviewed_movie(self):
        '''has a method "movie_reviewed()" that checks if a movie has been reviewed or not.'''
        viewer = Viewer(username="lucky_the_cat")
        movie_1 = Movie("No Country for Old Men")
        review = Review(viewer, movie_1, 4)
        assert viewer.movie_reviewed(movie_1)
        movie_2 = Movie("The Secret Life of Pets")
        assert not viewer.movie_reviewed(movie_2)

    def test_reviews_movie(self):
        '''Creates a review for a movie.'''
        viewer = Viewer(username="luckier_the_cat")
        movie = Movie("The Bourne Identity")
        viewer.rate_movie(movie, 3)
        assert movie in viewer.reviewed_movies()
        assert viewer.reviews()[0].rating == 3
        viewer.rate_movie(movie, 4)
        assert len(viewer.reviewed_movies()) == 2
        assert viewer.reviews()[1].rating == 4
