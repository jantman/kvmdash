#!/usr/bin/env python

from kvmdash import kvmdash

if __name__ == "__main__":
    kvmdash.debug = True
    kvmdash.run(host='0.0.0.0')
