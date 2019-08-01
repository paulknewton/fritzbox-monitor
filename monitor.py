from fritzconnection import fritzconnection


class FritzMonitor():
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
        resp = self.fc.call_action('DeviceInfo', 'GetDeviceLog')
        return resp["NewDeviceLog"]