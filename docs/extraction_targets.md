# モジュール切り出し対象一覧

ブランチ: `refactor-extract-modules`
方針: コメントは残す。再利用できる処理を、GUI に依存しないモジュールへ分割する。

## 1. 対象ファイル

| ファイル                                        | 行数 | 判定             | 内容                                                                                       |
| ----------------------------------------------- | ---- | ---------------- | ------------------------------------------------------------------------------------------ |
| `image_guiD_v13.py`                             | 931  | 切り出し対象(主) | GUI、CSV 入出力、画像表示、自動保存が 1 ファイルに混在。                                   |
| `search_img_Thread3.py`                         | 446  | 切り出し対象(主) | スクレイピング関数群。GUI 非依存だが、同じ処理が関数ごとに重複している。                   |
| `dateBase.py`                                   | 51   | 切り出し対象(小) | CSV を SQLite へ取り込む。`read_csv_file` は未使用で、処理はモジュール直下に書かれている。 |
| `image_guiD_v2.py`                              | 932  | 対象外(整理候補) | v13 とは import 行のみ差異あり。旧版として扱い、切り出し後に削除するか確認する。           |
| `setup_easy.py`                                 | 24   | 対象外           | cx_Freeze のビルド設定。                                                                   |
| `build/`, `__pycache__/`                        | -    | 対象外           | 生成物。追跡されているので、別途 `.gitignore` 対応を検討する。                             |
| `save/df_saveURL_V2.csv`, `sc/artist_url_4.csv` | -    | 対象外           | データ。パス定数を設定モジュールへ集約する。                                               |

## 2. 切り出し候補(処理単位)

### image_guiD_v13.py

| 現在の場所                                                | 候補モジュール                   | 切り出す内容                                                                                                                                   |
| --------------------------------------------------------- | -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| L21-L69                                                   | `storage/saved_list.py`          | 保存済み一覧 CSV の読み込み、列ごとの分解(`listBox_*Col`)。初期 CSV 生成。                                                                     |
| L75-L83                                                   | `storage/artist_list.py`         | `sc/artist_url_4.csv` の読み込み。                                                                                                             |
| L113-L128 `url_change`                                    | `storage/artist_list.py`         | アーティスト名から URL リストを返す。グローバル `box` への依存を引数化する。                                                                   |
| L505 付近 (while 内の `error_img` 読み込み)               | `storage/saved_list.py`          | 保存済みの `error_image` 文字列(`a` 区切り)と整数リストの相互変換。                                                                            |
| 自動保存部                                                | `core/url_normalize.py`          | 保存名の生成(`https://`、`www.`、`.com` の除去)。                                                                                              |
| 自動保存部 / 保存処理                                     | `storage/saved_list.py`          | CSV への行追記。`error_img` の文字列化が 2 か所で重複している。                                                                                |
| 削除処理 (`pd.read_csv` と `drop`)                        | `storage/saved_list.py`          | 行の削除。                                                                                                                                     |
| 描画処理 (`requests.get` から `resize`)                   | `core/image_loader.py`           | 画像の取得、サイズ判定(幅 150 以下、アスペクト比の範囲外は例外)、リサイズ後のサイズ計算、PNG バイト列化。GUI 更新(`image_elem.update`)は残す。 |
| while 内のカウント処理                                    | `core/viewer_state.py`           | `count`、`back_scroll`、`timeout`、スキップ判定、ループ判定を持つ状態クラス。PySimpleGUI に依存させない。                                      |
| `window_made`, `window_viewer_made`, テーマとフォント定数 | `gui/windows.py`, `gui/theme.py` | レイアウト定義。                                                                                                                               |
| 「コピー」「貼り付け」イベント処理                        | `gui/clipboard.py`               | メインウィンドウと viewer の 2 か所で重複している(対象 element のみ違う)。                                                                     |
| `browser = webbrowser.get(...)` と `-web-` 処理           | `core/browser.py`                | Chrome 固定のパスを設定化し、失敗時は既定ブラウザへフォールバックする。                                                                        |
| メインのイベントループ                                    | `app.py`                         | 組み立てと起動のみ。                                                                                                                           |

### search_img_Thread3.py

| 現在の場所                                                                                                           | 候補モジュール           | 切り出す内容                                                             |
| -------------------------------------------------------------------------------------------------------------------- | ------------------------ | ------------------------------------------------------------------------ |
| `img_web_surfaceList`, `img_webS_srcList`, `deepHTML_img` などに繰り返し出る相対パス補正 (`//`、`/`、`http`、その他) | `scraper/url_resolve.py` | 単一関数 `resolve_img_url(src, base_url)`。現状 9 か所で同じ分岐を持つ。 |
| 各関数の `requests.get` と `html.fromstring`                                                                         | `scraper/fetch.py`       | HTML 取得とパース。タイムアウトと待機時間(`time.sleep(1)`)を引数化する。 |
| 各関数の xpath 取得ロジック                                                                                          | `scraper/extractors.py`  | `//img/@src`、`a/img/@src` などを戦略として分ける。                      |
| `SurDeep_imgthread`                                                                                                  | `scraper/threaded.py`    | スレッド並列実行と結果の統合、重複除去(`dict.fromkeys`)。                |
| `IMG_STYLE`, `D_HIERARCHY`                                                                                           | `scraper/constants.py`   | 定数。                                                                   |

### dateBase.py

| 現在の場所                   | 候補モジュール             | 切り出す内容                                                                                                     |
| ---------------------------- | -------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| モジュール直下の SQLite 処理 | `storage/sqlite_import.py` | 関数化し、`if __name__ == "__main__":` で起動する。テーブル名の `your_table_name` は仮名のため、命名を確認する。 |

## 3. GUI と処理が重複している箇所(両方を切り出す)

| 重複内容                                       | 該当箇所                                    | 切り出し先               |
| ---------------------------------------------- | ------------------------------------------- | ------------------------ |
| `error_img` を `a` 区切り文字列に変換する処理  | 自動保存、手動保存(2 か所)                  | `storage/saved_list.py`  |
| 一覧 CSV の再読込と `listBox_*Col` の再構築    | 起動時、後処理(2 か所)                      | `storage/saved_list.py`  |
| 画像 URL の相対パス補正                        | `search_img_Thread3.py` 内で複数回          | `scraper/url_resolve.py` |
| クリップボードのコピー処理                     | メインウィンドウと viewer                   | `gui/clipboard.py`       |
| 画面遷移 `window.close()` から `window_made()` | viewer 内の RETURN とエラー画像過多(3 か所) | `gui/` 内のヘルパー      |
| 画像の取得とリサイズ                           | GUI 内のみ                                  | `core/image_loader.py`   |

## 4. 切り出し時の確認事項

- v13 の現行動作を維持するため、リファクタ前にキャラクタリゼーションテストを用意する。対象は URL 補正、`error_img` の変換、リサイズ計算、保存名の生成。
- リサイズ処理の `aspect_ratio >= 0.909 or aspect_ratio <= 1.1` は常に真になる。この挙動を維持するか修正するかは、切り出し時に判断する。
- `-del-` の処理は、`window` や `g` といったグローバル状態に依存している。切り出す際に状態の持ち方を決める必要がある。
- `image_guiD_v2.py` の扱い(削除するか、残すか)。
