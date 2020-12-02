"""
Unit test
"""
import pytest
from wechaty_plugin_contrib.daily_plugin import DailyPluginOptions


def test_plugin():
    options = DailyPluginOptions(name='daily-plugin')
    assert options is not None
