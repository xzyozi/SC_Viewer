"""HTTP 取得とHTMLパース。GUI に依存しない。

- User-Agent を指定した Session を共有する
- タイムアウトとステータス確認を必ず行う
- 連続取得用に robots.txt の確認関数を提供する
"""
import threading
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests
from lxml import html

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)
DEFAULT_TIMEOUT = 10  # 秒

_session = requests.Session()
_session.headers.update({"User-Agent": USER_AGENT})

_robots_cache = {}
_robots_lock = threading.Lock()


def fetch_tree(url, timeout=DEFAULT_TIMEOUT):
    """url を取得し、lxml の要素ツリーを返す。4xx/5xx は HTTPError を送出する。"""
    response = _session.get(url, timeout=timeout)
    response.raise_for_status()
    return html.fromstring(response.content)


def is_allowed_by_robots(url, timeout=DEFAULT_TIMEOUT):
    """robots.txt で url の取得が許可されているか。robots.txt を取得できない場合は許可とみなす。"""
    parts = urlparse(url)
    origin = f"{parts.scheme}://{parts.netloc}"

    with _robots_lock:
        parser = _robots_cache.get(origin)

    if parser is None:
        parser = RobotFileParser()
        try:
            response = _session.get(f"{origin}/robots.txt", timeout=timeout)
            if response.status_code == 200:
                parser.parse(response.text.splitlines())
            else:
                parser.allow_all = True
        except requests.RequestException:
            parser.allow_all = True
        with _robots_lock:
            _robots_cache[origin] = parser

    return parser.can_fetch(USER_AGENT, url)
