__author__ = 'yoshi.miyamoto'
import logging
logger = logging.getLogger('access_log')


class LogRequestParams(object):

    def process_request(self, request):
        http = request.POST if request.POST else request.GET
        logger.info("PATH: {path}, HttpRequest: {http}".
                    format(path=request.path, http=http))
        return None
