import os

import gspread
from google.oauth2.service_account import Credentials

SA_FILE = os.environ["MF_SA_FILE"]
SPREADSHEET_KEY = os.environ["MF_SPREADSHEET_KEY"]


class GSpreadsheetService:
    def __init__(self) -> None:
        # お決まりの文句
        # 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        # ダウンロードしたjsonファイル名をクレデンシャル変数に設定。
        credentials = Credentials.from_service_account_file(SA_FILE, scopes=scope)

        # OAuth2の資格情報を使用してGoogle APIにログイン。
        self.gc = gspread.authorize(credentials)

    def worksheet(self, name) -> gspread.Worksheet:
        # スプレッドシートIDを変数に格納する。
        # スプレッドシート（ブック）を開く
        workbook = self.gc.open_by_key(SPREADSHEET_KEY)

        # シートの一覧を取得する。（リスト形式）
        worksheets = workbook.worksheets()

        if name in [i.title for i in worksheets]:
            # シートを開く
            return workbook.worksheet(name)
        else:
            return workbook.add_worksheet(name, rows=100, cols=20)

    def update(self, name, row, col, values, clear=False, **kwargs):
        a = gspread.utils.rowcol_to_a1(row, col)
        b = gspread.utils.rowcol_to_a1(row + len(values), col + len(values[0]))
        sheet = self.worksheet(name)
        if clear:
            sheet.clear()
        return sheet.update(f"{a}:{b}", values, **kwargs)


# GSpreadsheetService().worksheet('mfupdate_total')
