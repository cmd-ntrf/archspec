# Copyright 2019-2020 Lawrence Livermore National Security, LLC and other
# Archspec Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Global objects with the content of the microarchitecture
JSON file and its schema
"""
import json
import os.path

import urllib.request

try:
    from collections.abc import MutableMapping  # novm
except ImportError:
    from collections import MutableMapping


class LazyDictionary(MutableMapping):
    """Lazy dictionary that gets constructed on first access to any object key

    Args:
        factory (callable): factory function to construct the dictionary
    """

    def __init__(self, factory, *args, **kwargs):
        self.factory = factory
        self.args = args
        self.kwargs = kwargs
        self._data = None

    @property
    def data(self):
        """Returns the lazily constructed dictionary"""
        if self._data is None:
            self._data = self.factory(*self.args, **self.kwargs)
        return self._data

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)


def _load_json_file(json_file):
    def _factory():
        with urllib.request.urlopen('https://raw.githubusercontent.com/archspec/archspec-json/v0.1.2/cpu/' + json_file) as response:
            return json.loads(response.read())
    return _factory

#: In memory representation of the data in microarchitectures.json,
#: loaded on first access
TARGETS_JSON = LazyDictionary(_load_json_file("microarchitectures.json"))

#: JSON schema for microarchitectures.json, loaded on first access
SCHEMA = LazyDictionary(_load_json_file("microarchitectures_schema.json"))
