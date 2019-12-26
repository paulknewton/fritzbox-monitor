from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import super

from future import standard_library

standard_library.install_aliases()
from builtins import object


import fritzconnection


class FritzBox(object):
    """
    Accesses system logs for a FRITZ!Box
    """

    def __init__(self, fc=None, address=None, port=None,
                 user=None, password=None):
        super(FritzBox, self).__init__()
        if fc is None:
            fc = fritzconnection.FritzConnection(
                address=address,
                port=port,
                user=user,
                password=password,
            )
        self.fc = fc

    def get_system_log(self):
        """
        Get the current system log in text format showing device internet events
        :return: system log as a text string
        """
        resp = self.fc.call_action('DeviceInfo', 'GetDeviceLog')
        return resp["NewDeviceLog"]
