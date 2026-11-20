"""画像URLの正規化。GUI に依存しない。"""
from urllib.parse import urljoin, urlparse

IMG_STYLE = ['jpg', 'png', 'gif', 'jpeg', 'webp']  # 画像として扱う拡張子(ドットなし・小文字)


def resolve_img_url(base_url, src):
    """src (相対/絶対/プロトコル相対) を base_url 基準の絶対URLに変換する。

    urljoin は `//host/x`、`/x`、`./x`、`../x`、クエリ付きを標準仕様どおりに扱う。
    """
    return urljoin(base_url, src.strip())


def is_image_url(url):
    """URL のパス部分の拡張子で画像か判定する。クエリ・フラグメントと大文字小文字は無視する。"""
    path = urlparse(url).path.lower()
    return path.endswith(tuple(f".{ext}" for ext in IMG_STYLE))
