import logging
import os
from functools import lru_cache

import lxml.etree
import lxml.html
import requests

logger = logging.getLogger(__name__)


class MFFetcher:
    headers = {}
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
        self.bs_url = "{url}/bs/portfolio".format(url=url)

    def _login(self):
        r = requests.get(self.url, cookies=self.cookies)
        self.top_html = lxml.html.fromstring(r.text)
        self.token = str(self.top_html.xpath("//meta[@name='csrf-token']/@content")[0])

        logger.debug(f"login token is {self.token}")

        assert self.token is not None

    @lru_cache
    def _get_bs_raw(self):
        r = requests.get(self.bs_url, cookies=self.cookies)
        bs = lxml.html.fromstring(r.text)
        return bs

    def convert_table_to_array(self, map_table_name):
        try:
            eq = self._get_bs_raw().xpath(self.map_table[map_table_name])[0]
            return [
                [col.text_content().strip() for col in row]
                for row in eq.findall(".//tr")
            ]
        except:
            return

    def _set_update(self):
        """更新対象を抽出し、更新を実施する"""
        link = self.top_html.xpath("//*[text()='更新']/@href")
        link = list(map(lambda x: self.url + x, link))  # urlを付与
        list(map(self._post_reload, link))

    def _post_reload(self, url: str):
        """連携先からデータを取得するリクエストを行う

        Args:
            url (str): 更新するための絶対URL
        """

        r = requests.post(
            url,
            cookies=self.cookies,
            headers={"X-Requested-With": "XMLHttpRequest", "X-CSRF-Token": self.token},
        )
        assert r.status_code == 200

    def get_token(self):
        pass
