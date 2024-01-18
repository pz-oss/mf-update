import os

import gspread
from retry import retry

from google.oauth2.service_account import (
    Credentials,
)

SA_FILE = os.environ["MF_SA_FILE"]
SPREADSHEET_KEY = os.environ["MF_SPREADSHEET_KEY"]


class GSpreadsheetService:
    """リストのリストを使用して Google スプレッドシートを簡単に更新できる gspread ライブラリのラッパーです。"""

    @retry()
    def __init__(
        self,
    ) -> None:
        # お決まりの文句
        # 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        # ダウンロードしたjsonファイル名をクレデンシャル変数に設定。
        credentials = Credentials.from_service_account_file(
            SA_FILE,
            scopes=scope,
        )

        # OAuth2の資格情報を使用してGoogle APIにログイン。
        self.gclient = gspread.authorize(credentials)

    def worksheet(self, name) -> gspread.Worksheet:
        """
        スプレッドシートを開き、ワークシートを返します。

        :param name: 開きたいワークシートの名前。
        :return: ワークシート オブジェクト。
        """
        # スプレッドシートIDを変数に格納する。
        # スプレッドシート（ブック）を開く
        workbook = self.gclient.open_by_key(SPREADSHEET_KEY)

        # シートの一覧を取得する。（リスト形式）
        worksheets = workbook.worksheets()

        if name in [i.title for i in worksheets]:
            # シートを開く
            return workbook.worksheet(name)

        return workbook.add_worksheet(
            name,
            rows=100,
            cols=20,
        )

    @retry()
    def update(
        self,
        name,
        row,
        col,
        values,
        clear=False,
        **kwargs,
    ):
        """
        リストのリストを受け取り、それを Google スプレッドシートに書き込みます

        :param name: ワークシートの名前。
        :param row: 書き込みを開始する行番号。
        :param col: 書き込みを開始する列番号。
        :param values: リストのリスト。それぞれがスプレッドシートの行を表します。
        :param clear: True の場合、更新前にシートをクリアします。, defaults to False (optional)
        :return: リストのリスト。
        """
        cell1 = gspread.utils.rowcol_to_a1(row, col)
        cell2 = gspread.utils.rowcol_to_a1(
            row + len(values),
            col + len(values[0]),
        )
        sheet = self.worksheet(name)
        if clear:
            sheet.clear()
        return sheet.update(
            f"{cell1}:{cell2}",
            values,
            **kwargs,
        )
