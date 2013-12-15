"""
File-based storage
"""

from config import FILESTORAGE_DIR
import os
import re
import anyjson

class FileStorage():
    """
    Store hosts and guests on the filesystem
    """

    _base_path = None

    def __init__(self):
        """
        base_path - base abs FS path to storage dir
        """
        self._base_path = FILESTORAGE_DIR

    def list_hosts(self):
        """
        Return a list of all KVM host names.
        """
        ret = []
        file_re = re.compile(r'host_(.+).json')
        for f in os.listdir(self._base_path):
            p = os.path.join(self._base_path, f)
            if not os.path.isfile(p):
                continue
            m = file_re.match(f)
            if m is None:
                continue
            ret.append(m.group(1))
        return ret

    def get_host(self, name):
        """
        Return the hash of information about a host.

        Return None if not found.
        """
        fname = "host_%s.json" % name
        path = os.path.join(self._base_path, fname)
        if not os.path.exists(path):
            return None
        if not os.path.isfile(path):
            return None
        ret = None
        raw = ""
        with open(path, 'r') as fh:
            raw = fh.read()
        ret = anyjson.deserialize(raw)
        return ret

    def get_all_hosts(self):
        """
        Return a dict of all KVM host information,
        hostname -> dict of data
        """
        ret = {}
        file_re = re.compile(r'host_(.+).json')
        for f in os.listdir(self._base_path):
            p = os.path.join(self._base_path, f)
            if not os.path.isfile(p):
                continue
            m = file_re.match(f)
            if m is None:
                continue
            foo = None
            raw = None
            with open(p, 'r') as fh:
                raw = fh.read()
                foo = anyjson.deserialize(raw)
            ret[m.group(1)] = foo
        return ret

    def list_guests(self):
        """
        Return a list of all KVM guest names.
        """
        ret = []
        file_re = re.compile(r'guest_(.+).json')
        for f in os.listdir(self._base_path):
            p = os.path.join(self._base_path, f)
            if not os.path.isfile(p):
                continue
            m = file_re.match(f)
            if m is None:
                continue
            ret.append(m.group(1))
        return ret

    def get_guest(self, domname):
        """
        Return the hash of information about a specific guest,
        by libvirt domain name

        Return None if not found.
        """
        fname = "guest_%s.json" % name
        path = os.path.join(self._base_path, fname)
        if not os.path.exists(path):
            return None
        if not os.path.isfile(path):
            return None
        ret = None
        raw = ""
        with open(path, 'r') as fh:
            raw = fh.read()
        ret = anyjson.deserialize(raw)
        return ret

    def get_all_guests(self):
        """
        Return a dict of all KVM guest information,
        libvirt domain name -> dict of data
        """
        ret = {}
        file_re = re.compile(r'guest_(.+).json')
        for f in os.listdir(self._base_path):
            p = os.path.join(self._base_path, f)
            if not os.path.isfile(p):
                continue
            m = file_re.match(f)
            if m is None:
                continue
            foo = None
            with open(p, 'r') as fh:
                raw = fh.read()
            foo = anyjson.deserialize(raw)
            ret[m.group(1)] = foo
        return ret
