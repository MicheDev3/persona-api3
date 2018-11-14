from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from src import settings

__all__ = ['SessionManager']


class SessionManager(object):

    def __init__(self):
        self.session = self.create_session()

    @staticmethod
    def create_session():
        engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
        session_factory = sessionmaker(bind=engine)
        return scoped_session(session_factory)

    def process_resource(self, req, resp, resource, params):
        resource.session = self.session()

    def process_response(self, req, resp, resource, req_succeeded):
        if hasattr(resource, 'session'):
            if req_succeeded:
                resource.session.commit()
            self.session.remove()
