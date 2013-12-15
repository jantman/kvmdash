from flask import request, jsonify
from kvmdash import kvmdash
from config import STORAGE_CLASS, MAX_UPLOAD_LEN
from storage import get_storage_api
import anyjson

@kvmdash.route('/clientapi/v1/host/byname/<hostname>', methods=['GET', 'PUT'])
def clientapi_host(hostname):
    """
    client GET or PUT host data by hostname
    """
    c = get_storage_api(STORAGE_CLASS)
    stor = c()

    if request.method == 'GET':
        data = stor.get_host(hostname)
        if data is None:
            abort(404)
        return jsonify(data) # implicit 200
    elif request.method == 'PUT':
        if request.content_length > MAX_UPLOAD_LEN:
            abort(413)
        if not request.json or not 'name' in request.json:
            abort(400)
        result = stor.store_host(hostname, request.json)
        if not result:
            abort(500)
        return jsonify( request.json ), 201
    abort(405) # method not allowed
