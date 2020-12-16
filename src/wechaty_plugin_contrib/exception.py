"""exception in wechaty-plugin-contrib"""


class WechatyPluginError(Exception):
    """ Wechaty puppet error """

    def __init__(self, message, code=None, params=None):
        super().__init__(message, code, params)

        self.message = message
        self.code = code
        self.params = params

    def __str__(self):
        return repr(self)


class WechatyPluginConfigurationError(WechatyPluginError):
    """ Raises when configuration out of expected case """
