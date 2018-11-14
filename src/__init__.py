import falcon
import logging

from src import settings

__all__ = ['falcon', 'settings', 'custom_error_handler']

# setting up logging
# TODO find an other way (it seems using dictConfig, instead of basicConfig, does not works)
logging.basicConfig(format='%(levelname)s [%(name)s]: %(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=settings.LOG_LEVEL)

logger = logging.getLogger("waitress")


def custom_error_handler(ex, req, resp, params):
    # handling as normal 500 for normal exceptions
    if not isinstance(ex, falcon.HTTPError):
        logger.exception('{0} {1} {2}'.format(req.method, req.relative_uri, 500))
        raise falcon.HTTPInternalServerError()

    # handling the falcon.HTTPError
    status = ex.status[:3]
    if status <= "500":
        logger.warning('{0} {1} {2}'.format(req.method, req.relative_uri, status))
    else:
        logger.exception('{0} {1} {2}'.format(req.method, req.relative_uri, status))
    raise ex
