"""Serve GET responses from a per-target snapshot of the mirrored site.

A target opts in by defining SNAPSHOT_KEY in its config.py and shipping a
database.sqlite next to it, holding a `pages` table that some other process
populates. When a target has not opted in, every request falls through to the
network untouched.
"""
import os
import sqlite3

import requests

from config_default import *
from config_global import *

from flask import g, current_app

from .urlutil import clean_and_sort_url

try:
    from config import *
except:  # coverage: exclude
    print('There is no specific config for this domain')
    raise

try:
    SNAPSHOT_KEY
except NameError:  # the target did not opt into the snapshot cache
    SNAPSHOT_KEY = None

CURRENT_DIR = os.path.dirname(__file__)

DB_NAME = 'database.sqlite'
DB_PATH = os.path.join(os.path.dirname(CURRENT_DIR), 'target_domains', target_domain, DB_NAME)

SELECT_PAGE = (
    'SELECT res_body, res_mime, snapshot FROM pages '
    'WHERE site = ? AND req_path LIKE ? AND snapshot = ? '
    'ORDER BY rowid DESC LIMIT 1'
)


def snapshot_cache_enabled():
    return SNAPSHOT_KEY is not None and os.path.isfile(DB_PATH)


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def _build_response(url, res_body, res_mime, snapshot):
    """Rebuild a requests.Response from a stored row.

    The caller treats the result exactly like a live response, so it needs the
    body, the mime and an originating request to be present.
    """
    response = requests.Response()
    response._content = res_body.encode() if isinstance(res_body, str) else res_body
    response.status_code = 200
    response.headers['Content-Type'] = res_mime
    response.headers['x-zmirror-cache'] = snapshot
    response.request = requests.Request(method='GET', url=url, headers={})
    response.url = url
    return response


def cache_request(send_request):
    def wrapper(url, **kwargs):
        if kwargs.get('method', 'GET') != 'GET' or not snapshot_cache_enabled():
            return send_request(url, **kwargs)

        try:
            cur = get_db().cursor()
            cur.execute(SELECT_PAGE, (
                target_domain,
                '%' + clean_and_sort_url(url),
                current_app.config[SNAPSHOT_KEY],
            ))
            result = cur.fetchone()
            if result:
                return _build_response(url, *result)
        except (sqlite3.Error, KeyError):
            # A missing table, an unreadable file or a snapshot that the target
            # has not recorded yet: fall back to the network rather than fail.
            pass

        return send_request(url, **kwargs)

    return wrapper
