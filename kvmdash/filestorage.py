"""
File-based storage
"""

from config import FILESTORAGE_DIR
import os
import re

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
