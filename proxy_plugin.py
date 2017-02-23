"""
A ctags plugin for Sublime Text 2/3.
"""

import functools
import codecs
import locale
import sys
import os
import pprint
import re
import string
import threading
import subprocess

from itertools import chain
from operator import itemgetter as iget
from collections import defaultdict, deque

try:
    import sublime
    import sublime_plugin
    from sublime import status_message, error_message

    # hack the system path to prevent the following issue in ST3
    #     ImportError: No module named 'ctags'
    sys.path.append(os.path.dirname(os.path.realpath(__file__)))
except ImportError:  # running tests
    from tests.sublime_fake import sublime
    from tests.sublime_fake import sublime_plugin

    sys.modules['sublime'] = sublime
    sys.modules['sublime_plugin'] = sublime_plugin

import ctags
from ctags import (FILENAME, parse_tag_lines, PATH_ORDER, SYMBOL,
                   TagElements, TagFile)
from helpers.edit import Edit


def get_settings():
    """
    Load settings.

    :returns: dictionary containing settings
    """
    return sublime.load_settings("CTags.sublime-settings")

def get_setting(key, default=None):
    """
    Load individual setting.

    :param key: setting key to get value for
    :param default: default value to return if no value found

    :returns: value for ``key`` if ``key`` exists, else ``default``
    """
    return get_settings().get(key, default)

setting = get_setting

class ProxyNavigateToDeclaration(sublime_plugin.TextCommand):
    """
    Provider for the ``proxy_navigate_to_declaration`` command.

    Command navigates to the definition for a symbol in the open file(s) or
    folder(s).
    """

    def __init__(self, args):
        sublime_plugin.TextCommand.__init__(self, args)

    def is_visible(self):
        return False

    def run(self, edit):
        view = self.view
        language = view.settings().get('syntax')
        if 'Scala' in language:
            view.window().run_command('ensime_go_to_definition')
            return
        else:
            view.window().run_command('navigate_to_definition')
