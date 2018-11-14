import falcon

from schema import Schema, SchemaError

__all__ = ['ValidatorManager']


class ValidatorManager(object):

    def process_resource(self, req, resp, resource, params):
        data = req.context.get('request') or req.params

        method = req.method.upper()
        validators = getattr(resource, "validators")
        if not validators or method not in validators:
            return

        try:
            req.context['valid_data'] = Schema(validators[method]).validate(data=data)
        except SchemaError as exc:
            raise falcon.HTTPBadRequest(description=exc.code)
