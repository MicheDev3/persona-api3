import base64
import datetime
import hashlib
import hmac

import falcon

from src import settings

__all__ = ['AuthManager']


class AuthManager(object):

    @staticmethod
    def get_signature():
        """
        :return: signature to be matched against the request
        """
        # using a date plus a salt in order to create the raw string
        raw = datetime.date.today().strftime('%d/%m/%Y') + u"#persona#api#"
        digest = hmac.new(
            bytes(settings.SECRET_KEY, 'utf-8'), raw.encode('utf-8'), hashlib.sha256
        ).digest()
        return base64.b64encode(digest).decode()

    def process_request(self, req, resp):
        token = req.get_header('Authorization')

        if not token or token != self.get_signature():
            raise falcon.HTTPUnauthorized(
                "You don\'t have the permission to access the requested resource."
                "It is either read-protected or not readable by the server."
            )
