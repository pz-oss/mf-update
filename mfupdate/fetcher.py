import logging
import os
from functools import lru_cache

import lxml.etree
import lxml.html
import requests

logger = logging.getLogger(__name__)


class MFFetcher:
    """MFからデータを取得し、リストのリストに変換します"""

    headers = {"User-Agent": 'Mozilla/5.0'}
    cookies = {"_moneybook_session": os.environ.get("MF_SESSION")}
    token = None
    map_table = {
        # 資産の内訳
        "total": '//section[contains(@class,"bs-total-assets")]//table',
        # 現物株式
        "eq": '//section[@id="portfolio_det_eq"]//table[contains(@class,"table-eq")]',
        # 株式信用
        "mgn": '//section[@id="portfolio_det_mgn"]//table[contains(@class,"table-mgn")]',
        # 先物・オプション
        "drv": '//section[@id="portfolio_det_drv"]//table[contains(@class,"table-drv")]',
    }

    def __init__(self, url):
        self.url = url
        self.bs_url = f"{url}/bs/portfolio"
        self._login()

    def _login(self):
        """
        > ログインページに GET リクエストを送信し、HTML を解析し、CSRF トークンを抽出します
        """
        response = requests.get(self.url, cookies=self.cookies, headers=self.headers)
        self.top_html = lxml.html.fromstring(response.text)
        self.token = str(self.top_html.xpath("//meta[@name='csrf-token']/@content")[0])

        logger.debug("login token is %s", self.token)

        assert self.token is not None

    @lru_cache
    def _get_bs_raw(self):
        """
        URL を受け取り、その URL にリクエストを送信し、レスポンスを BeautifulSoup オブジェクトとして返します。
        :return: ページ上のすべてのリンクのリスト。
        """
        response = requests.get(self.bs_url, cookies=self.cookies)
        element = lxml.html.fromstring(response.text)
        return element

    def convert_table_to_array(self, map_table_name):
        """
        この関数はテーブル名を入力として取り、テーブルの内容の 2D 配列を返します

        :param map_table_name: 配列に変換するテーブルの名前。
        """
        try:
            table = self._get_bs_raw().xpath(self.map_table[map_table_name])[0]
            return [
                [self._clean_text(col.text_content()) for col in row]
                for row in table.findall(".//tr")
            ]
        except IndexError:
            return [[]]

    def _clean_text(self, text):
        """
        この関数はテキストを入力として受け取り、カンマや単位（円）を取り除き、数値を返します。
        :param text: 数値を含むテキスト。
        """
        try:
            return float(text.replace(",", "").replace("円", ""))
        except ValueError:
            return text.strip()

    def update(self):
        """更新対象を抽出し、更新を実施する"""
        link = self.top_html.xpath("//*[text()='更新']/@href")
        link = list(map(lambda x: self.url + x, link))  # urlを付与
        assert len(link) > 0
        list(map(self._post_reload, link))

    def _post_reload(self, url: str):
        """連携先からデータを取得するリクエストを行う

        Args:
            url (str): 更新するための絶対URL
        """

        response = requests.post(
            url,
            cookies=self.cookies,
            headers=dict(self.headers,**{"X-Requested-With": "XMLHttpRequest", "X-CSRF-Token": self.token}),
        )
        assert response.status_code == 200
