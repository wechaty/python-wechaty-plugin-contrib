"""exception in wechaty-plugin-contrib"""
from typing import Any


class WechatyPluginError(Exception):
    """ Wechaty puppet error """

    def __init__(self, message: str, code: Any = None, params: Any = None) -> None:
        super().__init__(message, code, params)

        self.message = message
        self.code = code
        self.params = params

    def __str__(self) -> str:
        return repr(self)


class WechatyPluginConfigurationError(WechatyPluginError):
    """ Raises when configuration out of expected case """
