class Review:
    all = []

    def __init__(self, viewer, movie, rating):
        if isinstance(rating, int or float):
            self.viewer = viewer
            self.movie = movie
            self.rating = rating
        else:
            raise Exception('rating is not valid')
        Review.get_all_reviews(self)

    @classmethod
    def get_all_reviews(cls, review):
        cls.all.append(review)


    # rating property goes here!
    def get_rating(self):
        return self._rating

    def set_rating(self, rating):
        if isinstance(rating, int) and (1<=rating<=5): #Review in review.py requires ratings to be between 1 and 5, inclusive. - Exception: rating is not valid
            self._rating = rating
        else:
            raise Exception('rating must be a number between 1 and 5.')

    rating = property(get_rating, set_rating)

    # viewer property goes here!
    def get_viewer(self):
        return self._viewer
    def set_viewer(self,viewer):
        from classes.Viewer import Viewer
        if isinstance(viewer, Viewer):
            self._viewer = viewer
        else:
            raise Exception('this is not a valid instance')
    viewer = property(get_viewer, set_viewer)

    # movie property goes here!
    def get_movie(self):
        return self._movie
    def set_movie(self, movie):
        from classes.Movie import Movie
        if isinstance(movie,Movie):
            self._movie = movie
        else:
            raise Exception('this is not a valid instance')
    movie = property(get_movie, set_movie)

