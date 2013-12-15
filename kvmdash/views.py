from flask import render_template
from kvmdash import kvmdash
from config import STORAGE_CLASS, AGE_THRESHOLD_SEC
from storage import get_storage_api
from util import calculate_host_resources
from jinja_filters import format_ts_as_age
import time

#url_for('static', filename='favicon.ico')

@kvmdash.route('/')
@kvmdash.route('/index')
@kvmdash.route('/index.html')
@kvmdash.route('/index.htm')
def index():
    """
    main index page
    """
    kvmdash.jinja_env.filters['formatage'] = format_ts_as_age
    c = get_storage_api(STORAGE_CLASS)
    stor = c()
    raw_hosts = stor.get_all_hosts()
    guests = stor.get_all_guests()
    hosts = calculate_host_resources(raw_hosts, guests)
    return render_template("index.html",
                           title = 'kvmdash',
                           now = int(time.time()),
                           age_threshold = AGE_THRESHOLD_SEC,
                           hosts = hosts,
                           guests = guests)
