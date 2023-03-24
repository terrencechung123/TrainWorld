from classes.Review import Review


class Movie:
    def __init__(self, title):
        self.title = title

    def get_title(self):
        return self._title

    def set_title(self, title):
        if 0 < len(title): #Movie in movie.py requires titles to be strings of >0 characters.
            self._title = title
        else:
            raise Exception('name is not valid.')
    title = property(get_title, set_title)


    # title property goes here

    def reviews(self):
        from classes.Review import Review
        reviews_list = []
        for review in Review.all:
            if review.movie == self:
                reviews_list.append(review)
        return reviews_list

    def reviewers(self):
        reviewers_reviewed= []
        for review in self.reviews():
            if not review.viewer in reviewers_reviewed:
                reviewers_reviewed.append(review)
        return reviewers_reviewed

    def average_rating(self):
        reviews = self.reviews()
        rating = [review.rating for review in reviews]
        num_reviews = len(reviews)
        sum_price = sum(rating)
        return sum_price / num_reviews

# @classmethod
# def highest_rated(cls):
#     pass