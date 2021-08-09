"""
Unit test
"""
from wechaty_plugin_contrib import DailyPluginOptions


def test_plugin():
    options = DailyPluginOptions(name='daily-plugin')
    assert options is not None
