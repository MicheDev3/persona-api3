import ujson
import falcon
import logging

from schema import Optional
from src.models.persona import Persona
from src.api.common.utils import to_dict


__all__ = ['People', 'Search']


class People(object):
    validators = {'DELETE': {'username': str},
                  'GET': {'offset': str, Optional('limit', default="20"): str}}

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def on_get(self, req, resp):
        output = {}
        valid_data = req.context['valid_data']
        offset = int(valid_data['offset'])
        limit = offset + int(valid_data['limit'])
        personas = self.session.query(Persona).slice(
            offset, limit
        ).all()
        if personas:
            output = [to_dict(persona) for persona in personas]
        resp.body = ujson.dumps(output, ensure_ascii=False)
        self.logger.info('{0} {1} {2} {3}'.format(
            req.method, req.relative_uri, resp.status[:3], output)
        )

        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp):
        output = "No user found"
        valid_data = req.context['valid_data']
        deleted = self.session.query(Persona).filter(
            Persona.username == valid_data['username']
        ).delete()
        if deleted:
            output = "%s user(s) with %s equals to %s deleted" %\
                     (deleted, "username", valid_data['username'])
        resp.body = ujson.dumps(output, ensure_ascii=False)
        self.logger.info('{0} {1} {2} {3}'.format(
            req.method, req.relative_uri, resp.status[:3], output)
        )

        resp.status = falcon.HTTP_202


class Search(object):
    validators = {'GET': {'username': str}}

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def on_get(self, req, resp):
        output = {}
        valid_data = req.context['valid_data']
        personas = self.session.query(Persona).filter(
            Persona.username == valid_data['username']
        ).all()
        if personas:
            output = [to_dict(persona) for persona in personas]
        resp.body = ujson.dumps(output, ensure_ascii=False)
        self.logger.info('{0} {1} {2} {3}'.format(
            req.method, req.relative_uri, resp.status[:3], output)
        )

        resp.status = falcon.HTTP_200
