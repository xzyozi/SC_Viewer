"""後方互換用。実装は scraper パッケージへ移動した。

image_guiD_v13.py などの既存 import (from search_img_Thread3 import ...) を壊さないための薄いラッパー。
"""
from scraper.image_scraper import img_webS_srcList, SurDeep_imgthread  # noqa: F401
