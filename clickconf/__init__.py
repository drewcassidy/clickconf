import sys
from abc import abstractmethod

import click
import tomlkit
from os import PathLike
from typing import Type, Any, Union, Optional, MutableMapping, MutableSequence, TypeVar, Generic, Tuple, overload


class ConfigFile(MutableMapping):
    def __init__(self, label: str, path: PathLike, priority: int = 0, readonly: bool = False):
        self.label: str = label
        self.path: PathLike = path
        self.priority = 0
        self.readonly: bool = readonly
        self.doc: tomlkit.TOMLDocument = tomlkit.document()

    @property
    def loaded(self):
        return self.doc is not None

    def load(self):
        self.doc = tomlkit.load(self.path)  # TODO: THIS NEEDS A FILE POINTER

    def save(self):
        if not self.readonly:
            tomlkit.dump(self.doc, self.path)

    def insert(self, index, value) -> None:
        self.doc.insert(index, value)

    def __getitem__(self, item):
        return self.doc.__getitem__(item)

    def __setitem__(self, key, value):
        self.doc.__setitem__(key, value)

    def __delitem__(self, key):
        del self.doc[key]

    def __len__(self):
        return self.doc.__len__()

    def __iter__(self):
        return self.doc.__iter__()


class Config:
    def __init__(self):
        self._files = []

    def _sort(self):
        self._files.sort(key=lambda f: f.priority)

    def add_file(self, *args, **kwargs):
        self._files.append(ConfigFile(*args, **kwargs))
        self._sort()

    def load(self):
        for file in self._files:
            file.load()


class ConfigNode:
    def __init__(self, path: Union[str, Tuple]):
        self.path = path


class ConfigArray(ConfigNode, MutableSequence):
    def __init__(self, path: Union[str, Tuple]):
        super(ConfigNode).__init__(self, path)

    def __getitem__(self, index: int) -> _T:
        pass

    def insert(self, index: int, value) -> None:
        pass
