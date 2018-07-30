import logging
import xml.etree.ElementTree as XmlEtree
from contextlib import contextmanager
from urllib.parse import urljoin

import requests

logger = logging.getLogger(__name__)


class HttpClient(object):

    GET, POST, PUT, DELETE, HEAD, OPTIONS = 'GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'

    def __init__(self, host='', base_url='', single_session=False, **kwargs):
        self.url = urljoin(host, base_url)
        self.single_session = single_session
        self.kwargs = kwargs
        self._session = None

    @property
    def session(self):
        if self.single_session:
            if self._session is None:
                self._session = requests.session()
            return self._session
        else:
            return requests.session()

    @contextmanager
    def session_ctx(self):
        yield self.session
        if not self.single_session:
            self.session.close()

    def request(self, method, url, params=None, headers=None, data=None, json=None, xml_to_tree=False,
                expected_code=None, **kwargs):
        full_url = urljoin(self.url, url)
        self.kwargs.update({'params': params, 'headers': headers, 'data': data, 'json': json})
        self.kwargs.update(kwargs)
        logger.info('Making {} request:\n        URL: {}\n        PARAMS: {}\n        HEADERS: {}\n        BODY: {}'
                    '\n        JSON: {}'.format(method, full_url, self.kwargs['params'], self.kwargs['headers'],
                                                self.kwargs['data'], self.kwargs['json']))
        with self.session_ctx() as s:
            resp = s.request(method, full_url, **self.kwargs)
            logger.info('Request executed in {} sec. Response code {}'.format(resp.elapsed, resp.status_code))
            logger.debug(resp.text)

            if expected_code is not None and resp.status_code != expected_code:
                message = 'Response code is {} but {} was expected'.format(resp.status_code, expected_code)
                logger.error(message)
                logger.debug('Response: {}'.format(resp.text))
                raise UnexpectedStatusCode(resp.status_code, message)

            if xml_to_tree:
                return XmlEtree.parse(resp.text)

            return resp

    def get(self, url, params=None, headers=None, data=None, json=None, **kwargs):
        kwargs.update({'params': params, 'headers': headers, 'data': data, 'json': json})
        return self.request(self.GET, url, **kwargs)

    def post(self, url, params=None, headers=None, data=None, json=None, **kwargs):
        kwargs.update({'params': params, 'headers': headers, 'data': data, 'json': json})
        return self.request(self.POST, url, **kwargs)

    def put(self, url, params=None, headers=None, data=None, json=None, **kwargs):
        kwargs.update({'params': params, 'headers': headers, 'data': data, 'json': json})
        return self.request(self.PUT, url, **kwargs)

    def delete(self, url, params=None, headers=None, data=None, json=None, **kwargs):
        kwargs.update({'params': params, 'headers': headers, 'data': data, 'json': json})
        return self.request(self.DELETE, url, **kwargs)

    def head(self, url, params=None, headers=None, data=None, json=None, **kwargs):
        kwargs.update({'params': params, 'headers': headers, 'data': data, 'json': json})
        return self.request(self.HEAD, url, **kwargs)

    def options(self, url, params=None, headers=None, data=None, json=None, **kwargs):
        kwargs.update({'params': params, 'headers': headers, 'data': data, 'json': json})
        return self.request(self.OPTIONS, url, **kwargs)

    def close(self):
        if self._session is not None:
            self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class UnexpectedStatusCode(Exception):

    def __init__(self, status_code, *args, **kwargs):
        self.status_code = status_code
        super().__init__(*args, **kwargs)
