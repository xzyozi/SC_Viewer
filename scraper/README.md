# scraper

Web ページから画像 URL を集めるモジュール。GUI(PySimpleGUI)には依存しない。

## 構成

| ファイル | 内容 |
| --- | --- |
| `__init__.py` | 公開関数 `img_webS_srcList`、`SurDeep_imgthread` を再公開する。 |
| `image_scraper.py` | 画像 URL の抽出関数群。 |
| `http_client.py` | ページ取得とパース(`fetch_tree`)、robots.txt の確認(`is_allowed_by_robots`)。 |
| `url_resolve.py` | URL の絶対化(`resolve_img_url`)、画像拡張子の判定(`is_image_url`)、拡張子の定数 `IMG_STYLE`。 |

プロジェクト直下の `search_img_Thread3.py` は、このパッケージを呼ぶだけの後方互換ラッパー。`from search_img_Thread3 import ...` はそのまま動く。

## 使い方

```python
from scraper import SurDeep_imgthread, img_webS_srcList

# 1ページから画像 URL を集める(5種類の抽出を並列実行して統合)
urls = SurDeep_imgthread("https://example.com/page/")

# 複数ページ(ページ間は1秒待機)
urls = img_webS_srcList(["https://example.com/a/", "https://example.com/b/"])
```

## 関数

| 関数 | 抽出対象(XPath) |
| --- | --- |
| `SurDeep_imgthread(url)` | 下記5関数を並列実行して結果を統合する。ページ取得は1回だけ。 |
| `img_web_surfaceList(url, tree=None)` | `//img/@src` |
| `img_web_AHREFsrc(url, tree=None)` | `//a/@href` のうち画像拡張子のもの |
| `img_web_Aimgsrc(url, tree=None)` | `//a/img/@src` |
| `web_P_imgsrc(url, tree=None)` | `//p/img/@src` |
| `detaSlider(url, tree=None)` | `//img/@data-src` |
| `img_webS_srcList(urls)` | 複数 URL に対する `//img/@src` と `a/img/@src` |
| `deepHTML_img(url)` | リンク先ページを取得して画像を探す。現在は未使用。 |

`tree` を渡すと取得を省略できる。省略した場合は関数が自分で取得する。

## 動作の仕様

- 相対 URL は `urllib.parse.urljoin` で絶対化する。
- 画像拡張子は `jpg`、`jpeg`、`png`、`gif`、`webp`。クエリと大文字小文字は無視する。
- HTTP はタイムアウト10秒。User-Agent を指定し、4xx/5xx は `requests.HTTPError` を送出する。
- `deepHTML_img` は robots.txt を確認し、リンク先ごとに1秒待機する。
- 結果は重複を除き、出現順を保つ。

## 既知の制限

- `deepHTML_img` の XPath `/img/@src` は、どのページでも何も取得できない。
- `SurDeep_imgthread` の5つのスレッドは、同じ lxml ツリーを読み取り専用で共有する。
- 自動テストはない。
