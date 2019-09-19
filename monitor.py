from fritzconnection import fritzconnection


class FritzMonitor():
    """
    Accesses system logs for a FRITZ!Box
    """

    def __init__(self, fc=None, address=None, port=None,
                 user=None, password=None):
        super(FritzMonitor, self).__init__()
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
