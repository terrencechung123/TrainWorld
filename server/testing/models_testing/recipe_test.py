import pytest
from sqlalchemy.exc import IntegrityError

from app import app
from models import db, Train

class TestTrain:
    '''User in models.py'''

    def test_has_attributes(self):
        '''has attributes title, instructions, and minutes_to_complete.'''
        
        with app.app_context():

            Train.query.delete()
            db.session.commit()

            train = Train(
                    title="Delicious Shed Ham",
                    instructions="""Or kind rest bred with am shed then. In""" + \
                        """ raptures building an bringing be. Elderly is detract""" + \
                        """ tedious assured private so to visited. Do travelling""" + \
                        """ companions contrasted it. Mistress strongly remember""" + \
                        """ up to. Ham him compass you proceed calling detract.""" + \
                        """ Better of always missed we person mr. September""" + \
                        """ smallness northward situation few her certainty""" + \
                        """ something.""",
                    minutes_to_complete=60,
                    )

            db.session.add(train)
            db.session.commit()

            new_train = Train.query.filter(Train.title == "Delicious Shed Ham").first()

            assert new_train.title == "Delicious Shed Ham"
            assert new_train.instructions == """Or kind rest bred with am shed then. In""" + \
                    """ raptures building an bringing be. Elderly is detract""" + \
                    """ tedious assured private so to visited. Do travelling""" + \
                    """ companions contrasted it. Mistress strongly remember""" + \
                    """ up to. Ham him compass you proceed calling detract.""" + \
                    """ Better of always missed we person mr. September""" + \
                    """ smallness northward situation few her certainty""" + \
                    """ something."""
            assert new_train.minutes_to_complete == 60

    def test_requires_title(self):
        '''requires each record to have a title.'''

        with app.app_context():

            Train.query.delete()
            db.session.commit()

            train = Train()
            
            with pytest.raises(IntegrityError):
                db.session.add(train)
                db.session.commit()

    def test_requires_50_plus_char_instructions(self):
        with app.app_context():

            Train.query.delete()
            db.session.commit()

            train = Train(
                title="Generic Ham",
                instructions="idk lol")

            with pytest.raises(IntegrityError):
                db.session.add(train)
                db.session.commit()

