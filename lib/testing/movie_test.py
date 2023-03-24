import pytest

from classes.Movie import Movie
from classes.Review import Review
from classes.Viewer import Viewer


class TestMovie:
    '''Movie in movie.py'''

    def test_has_title(self):
        '''has the title passed into __init__.'''
        movie = Movie(title="Avatar: The Way of Water")
        assert movie.title == "Avatar: The Way of Water"

    def test_requires_nonzero_string_title(self):
        '''requires titles to be strings of >0 characters.'''
        movie = Movie("Scarface")
        assert movie.title == "Scarface"

        movie_2 = Movie("")
        assert not hasattr(movie_2, "_title")

        movie_3 = Movie(1)
        assert not hasattr(movie_3, "_title")

        # with pytest.raises(Exception):
        #     Movie(title=1)
        # with pytest.raises(Exception):
        #     Movie(title="")

    def test_has_reviews(self):
        '''contains a reviews() method that returns a list of its reviews.'''
        movie = Movie(title="Scarface")
        movie_2 = Movie("Finding Nemo")
        viewer = Viewer("code-blooded")
        review = Review(viewer, movie, 5)
        review_2 = Review(viewer, movie_2, 5)
        assert review in movie.reviews()
        assert not review_2 in movie.reviews()

    # TODO - NEED TO ADD REVIEWS AND VIEWERS

    def test_has_reviewers(self):
        '''contains a reviewers() method that returns a list of its viewers who left reviews.'''
        movie = Movie(title="Rashomon")
        viewer = Viewer("code-blooded")
        viewer_2 = Viewer("bananas")
        viewer_3 = Viewer("vibing-potatoes")
        Review(viewer, movie, 5)
        Review(viewer_2, movie, 5)
        assert viewer in movie.reviewers()
        assert viewer_2 in movie.reviewers()
        assert not viewer_3 in movie.reviewers()

    def test_calculates_average_rating(self):
        '''has a method "average_rating" that returns the average of self.reviews.'''
        movie = Movie(title="My Neighbor Totoro")
        viewer = Viewer("Apollo")
        Review(viewer, movie, 4)
        Review(viewer, movie, 5)
        Review(viewer, movie, 3)
        assert movie.average_rating() == 4

    def test_shows_highest_rated(self):
        '''has a method "highest_rated" that returns the highest rated movie.'''
        Movie.all = []
        viewer = Viewer("Emiley")
        movie_1 = Movie(title="Avatar: The Way of Water")
        Review(viewer, movie_1, 5)
        Review(viewer, movie_1, 5)
        Review(viewer, movie_1, 5)
        movie_2 = Movie(title="Scarface")
        Review(viewer, movie_2, 4)
        Review(viewer, movie_2, 4)
        Review(viewer, movie_2, 4)
        movie_3 = Movie(title="Rashomon")
        Review(viewer, movie_3, 3)
        Review(viewer, movie_3, 3)
        Review(viewer, movie_3, 3)

        assert Movie.highest_rated().title == "Avatar: The Way of Water"
