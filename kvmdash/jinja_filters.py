"""
Custom jinja filters
"""

import time

def format_ts_as_age(s):
    """
    Given an integer timestamp, format it as
    a textual/descriptive age string
    """
    now = int(time.time())
    age = now - s
    # make a human-formatted time string
    age_str = ""
    days    = int( age / 86400 )
    if days > 0:
        age_str = '%id ' % days
    hours   = int( ( age % 86400 ) / 3600 )
    if hours > 0:
        age_str = age_str + ('%ih ' % hours)
    minutes = int( ( age % 3600 ) / 60 )
    if minutes > 0:
        age_str = age_str + ('%im ' % minutes)
    seconds = int( age % 60 )
    age_str = age_str + ('%is' % seconds)
    return age_str
