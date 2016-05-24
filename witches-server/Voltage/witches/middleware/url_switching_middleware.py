from Voltage.witch_config import get_environment
from witches import const
from witches.master import is_versions_larger_than_prod
from witches.models import Environment
from witches.utils.custom_exceptions import NoValueFoundError, TooManyValueFoundError
from witches.utils.util import get_properties, throw_error_in_json_response
import logging
logger = logging.getLogger(__name__)

__author__ = 'yoshi.miyamoto'

"""
this class handle supporting 2 different API versions by looking up api_version in database.
build version and device name are needed for this process.
this also checks to see if the version is latest for every call
"""


class URLSwitchingMiddleware(object):
    def process_request(self, request):
        ENVIRONMENT = get_environment('Env', 'environment')
        #  all other environment uses current api
        if ENVIRONMENT == 'Prod':
            other = 'URLSwitchingMiddleware process request'
            try:
                path_info = request.META['PATH_INFO']
                if const.admintool in path_info:   # usage of const needs to be reconsidered. it's not used as a part of url
                    return None                    # paths so once path name changes, this const needs to be changed
                else:
                    build_version, device = self.get_version_device_info_from_request(request)
                    is_current_api = self.is_current_api_version(build_version, device)

                if is_current_api:
                    user_api_version = const.current_api_vers
                else:
                    user_api_version = const.historical_api_vers
                    # return self.handle_unsupported_version(device, build_version, other)
            except Exception as e:
                return throw_error_in_json_response(e, other)
        else:
            user_api_version = const.current_api_vers

        request.urlconf = 'Voltage.urls_' + user_api_version
        return None

    # """
    # "handle_unsupported_version" won't be used for the sprint 5 yet. we need more discussion on how to handle
    # force update for each server call.
    # this simply returns success status with a flag to indicate the build version is not latest.
    # Client side needs to be able to handle the response otherwise all server calls made from old build
    # will be treated as success call without updating database.
    # """
    # def handle_unsupported_version(self, device, build_version, other):
    #     try:
    #         prod = self.get_prod_environment(device)
    #     except Exception as e:
    #         return throw_error_in_json_response(e, other)
    #
    #     new_version = self.is_new_version(prod.build_version, build_version)
    #     if not new_version:
    #         res_obj = {'status': 'success', 'base_url': prod.base_url, 'latest': False,
    #                    'metrics': prod.metrics, 'obb_path': prod.obb_path}
    #         urls_json = json.dumps(res_obj, default=date_handler)
    #         return HttpResponse(urls_json, content_type='application/json')
    #     else:
    #         error = get_properties(err_type="Error", err_code="ERR0089")
    #         return throw_error_in_json_response(error, other)

    def get_version_device_info_from_request(self, request):
        build_version = request.POST.get('build')
        device = request.POST.get('device')
        if not build_version:
            build_version = request.GET.get('build')
            if not build_version:
                error = get_properties(err_type="Error", err_code="ERR0083")
                raise NoValueFoundError(error)
        if not device:
            device = request.GET.get('device')
            if not device:
                error = get_properties(err_type="Error", err_code="ERR0084")
                raise NoValueFoundError(error)
        return build_version, device

    def is_current_api_version(self, build_version, device):
        user_environment = Environment.objects.filter(build_version=build_version, device=device, delete_flag=False)
        if len(user_environment) == 1:
            return user_environment[0].current_api
        elif len(user_environment) == 0:
            return False
        else:
            error = get_properties(err_type="Error", err_code="ERR0086")
            raise TooManyValueFoundError(error)

    def get_prod_environment(self, device):
        prod = Environment.objects.filter(device=device, description='prod', delete_flag=False)
        if len(prod) == 1:
            return prod[0]
        elif len(prod) == 0:
            error = get_properties(err_type="Error", err_code="ERR0087")
            raise NoValueFoundError(error)
        else:
            error = get_properties(err_type="Error", err_code="ERR0088")
            raise TooManyValueFoundError(error)

    def is_new_version(self, prod_version, client_version):
            client_build_version = client_version.split("_")
            version = client_build_version[0].split(".")
            prod_build_version = prod_version.split(".")
            new_version = is_versions_larger_than_prod(version, prod_build_version)
            return new_version
