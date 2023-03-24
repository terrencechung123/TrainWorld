# from classes.Review import Review


class Viewer:

    def __init__(self, username):
        if isinstance(username, str):
            self.username = username

    def get_viewer(self):
        return self._username

    def set_viewer(self, username):
        if isinstance(username, str) and (5 < len(username) < 17): #Review in review.py requires ratings to be between 1 and 5, inclusive. - Exception: rating is not valid
            self._username = username


    def reviews(self):
        from classes.Review import Review
        reviews_list =[]
        for review in Review.all:
            if review.viewer == self:
                reviews_list.append(review)
        return reviews_list


    def reviewed_movies(self):
        viewers_who_reviewed = []
        for review in self.reviews():
            if not review.movie in viewers_who_reviewed:
                viewers_who_reviewed.append(review.movie)
        return viewers_who_reviewed

    def movie_reviewed(self, movie):
        return len(movie.reviews())

    def rate_movie(self, movie, rating):
        from classes.Review import Review
        rate_review = Review(self, movie, rating)
