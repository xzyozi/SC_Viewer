"""画像URLの正規化。GUI に依存しない。"""
from urllib.parse import urljoin


def resolve_img_url(base_url, src):
    """src (相対/絶対/プロトコル相対) を base_url 基準の絶対URLに変換する。

    urljoin は `//host/x`、`/x`、`./x`、`../x`、クエリ付きを標準仕様どおりに扱う。
    """
    return urljoin(base_url, src.strip())
