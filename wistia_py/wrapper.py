import calendar
import copy
from datetime import datetime, timedelta
import logging

import requests


log = logging.getLogger('wistia_py')


def utcnow():
    return datetime.utcnow()


def to_timestamp(date):
    return calendar.timegm(date.timetuple())


class WistiaAPI:
    """Simple wrapper class for Wistia API, using requests

    This makes requests to Wistia easier. In the future, it may be nice
    to auto validate certain required parameters, such as access, project_id.

    :param user: Your Wistia user, see https://wistia.com/support/developers/data-api#authentication
    :param api_password: Your Wistia api password, available in your account
    :param expiry_delta: How far in the future to expire this token, passed straight to timedelta, e.g. {'hours': 12}
    :type user: string
    :type api_password: string
    :type expiry_delta: dict
    :return: a python object

    :Example:

    wistia = WistiaAPI(user, api_password)
    # TODO: add more info here

    .. todo:: Add more example info
    """

    API_BASE_URL = 'https://api.wistia.com/v1/'
    # This is only used for expiring tokens for now
    # https://wistia.com/support/developers/v2-api-change-summary-08172016
    API_BASE_URL_V2 = 'https://api.wistia.com/v2/'
    EXPIRY_DELTA = dict(hours=12)

    def __init__(self, api_password, user='api', expiry_delta=None):
        self.user = user
        self.api_password = api_password
        self.expiry_delta = expiry_delta or self.EXPIRY_DELTA

    def call(self, rel_path, data=None, method='GET'):
        """Handles making HTTP request. Returns parsed JSON.

        Requests will be sent to:
        BASE_API_PATH/rel_path

        Parameters for queries are sent in the request body.

        :param rel_path: relative path to API endpoint, e.g. /medias.json
        :param data: python dictionary of parameters
        :type rel_path: string, excluding the beginning '/'
        :type data: python dictionary
        :type method: a valid HTTP method, e.g. 'GET', 'POST'
        :returns: python dictionary representing JSON response
        """
        response = requests.request(
            method,
            self.build_url(rel_path),
            data=data)

        return response.json()

    def build_url(self, rel_path):
        """
        Build a URL for queries. For query requests, parameters are sent in the
        query string and not in the POST.
        """
        if 'expiring_token' in rel_path:
            base = self.API_BASE_URL_V2
        else:
            base = self.API_BASE_URL

        return '{0}{1}?api_password={2}'.format(
            base, rel_path, self.api_password)

    def get_expiring_token(self, required_params=None, expires_at=None):
        """Request an expiring token, optionally require params

        See https://wistia.com/support/developers/uploader#using-expiring-tokens

        :returns: string, representing the expiring token value
        """
        data = []
        required_params = required_params or []
        if required_params:
            for key, value in required_params:
                data.append(('required_params[{0}]'.format(key), value))

        if expires_at is None:
            expires_at = to_timestamp(
                utcnow() +
                timedelta(**self.expiry_delta))

        json_response = self.call('expiring_token', data=data, method='POST')
        return json_response['data']['id']

    def get_upload_expiring_token(self, project_id,
                                  required_params=None, expires_at=None):
        """Wrapper for get_expiring_token for use with the uploader.

        :param project_id: project_id to upload into
        :type project_id: string, id of the project
        :returns: string, representing the expiring token value
        """
        required_params = (copy.deepcopy(required_params) if required_params
                           else [])
        required_params.append(('project_id', project_id))
        return self.get_expiring_token(required_params=required_params,
                                       expires_at=expires_at)

    def project_create(self, name, **parameters):
        """Create a Wistia project.

        For examples of other parameters you can pass, see:
        https://wistia.com/support/developers/data-api#projects_create

        By default, projects are public. Control where they can be embedded
        with expiring tokens and domain restriction. More info:
        * https://wistia.com/support/account/setup#domain-restrictions
        * https://wistia.com/support/developers/uploader#using-expiring-tokens
        """
        # Use safe defaults
        parameters.setdefault('anonymousCanUpload', False)
        parameters.setdefault('anonymousCanDownload', False)
        parameters.setdefault('public', True)
        data = dict(name=name, **parameters)

        return self.call('projects.json', data=data, method='POST')

    def medias_update(self, hashed_id, **parameters):
        """Update media object.

        For examples of other parameters you can pass, see:
        https://wistia.com/support/developers/data-api#medias_update
        """
        return self.call('medias/{0}.json'.format(hashed_id),
                         data=parameters, method='PUT')

    def medias_delete(self, hashed_id, **parameters):
        """Delete media object.

        For examples of other parameters you can pass, see:
        https://wistia.com/support/developers/data-api#medias_delete
        """
        return self.call('medias/{0}.json'.format(hashed_id), method='DELETE')
