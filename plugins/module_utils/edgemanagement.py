# -*- coding: utf-8 -*-

# (c) 2022, Adam Miller (admiller@redhat.com)
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from __future__ import absolute_import, division, print_function

__metaclass__ = type
from ansible.module_utils.connection import Connection
import ansible.module_utils.six.moves.urllib as url_lib

INVENTORY_API_HOSTS = '/api/inventory/v1/hosts'

EDGE_API_DEVICES = '/api/edge/v1/devices'
EDGE_API_DEVICESVIEW = '/api/edge/v1/devices/devicesview'
EDGE_API_GROUPS = '/api/edge/v1/device-groups'
EDGE_API_IMAGES = '/api/edge/v1/images'
EDGE_API_IMAGESETS = '/api/edge/v1/image-sets'
EDGE_API_THIRDPARTYREPO = '/api/edge/v1/thirdpartyrepo'
EDGE_API_UPDATES = "/api/edge/v1/updates"


class ConsoleDotRequest(object):
    def __init__(self, module, headers=None):

        self.module = module
        self.connection = Connection(self.module._socket_path)

    def _httpapi_error_handle(self, method, path, data=None):
        # FIXME - make use of handle_httperror(self, exception) where applicable
        #   https://docs.ansible.com/ansible/latest/network/dev_guide/developing_plugins_network.html#developing-plugins-httpapi

        code, response = self.connection.send_request(method, path, data=data)

        # if code == 500:
        if code not in [200, 201]:
            self.module.fail_json(msg=f"[{method}] Error-{code}: {response}")

        return response

    def get_groups(self, name: str = ''):
        valid_url_name = url_lib.parse.quote(name)
        return self.get(f'{EDGE_API_GROUPS}?name={valid_url_name}')

    def find_group(self, group_data, name: str = ''):
        if group_data['data'] is None:
            return []
        return [
            group for group in group_data['data'] if group['DeviceGroup']['Name'] == name
        ]

    def get_edge_system(self, system_id):
        api_request = '%s?uuid=%s' % (EDGE_API_DEVICESVIEW, system_id)
        response = self.get(api_request)
        return response['data']['devices'][0]

    def get(self, path, **kwargs):
        return self._httpapi_error_handle("GET", path, **kwargs)

    def put(self, path, **kwargs):
        return self._httpapi_error_handle("PUT", path, **kwargs)

    def post(self, path, **kwargs):
        return self._httpapi_error_handle("POST", path, **kwargs)

    def patch(self, path, **kwargs):
        return self._httpapi_error_handle("PATCH", path, **kwargs)

    def delete(self, path, **kwargs):
        return self._httpapi_error_handle("DELETE", path, **kwargs)
