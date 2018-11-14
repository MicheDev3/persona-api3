from sqlalchemy.ext.declarative import declarative_base


class Base(object):
    """
    Model base class some common behaviour needs to be defined
    """


Model = declarative_base(cls=Base)
