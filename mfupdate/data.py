from .fetcher import (
    MFFetcher,
)


class MFData:
    """資産のデータを含むクラスです"""

    def __init__(
        self,
        fetcher: MFFetcher,
    ) -> None:
        """
        `__init__` は、クラスのインスタンスが作成されるときに呼び出される特別なメソッドです

        :param fetcher: MFWebFetcher オブジェクト
        """
        self.fetcher = fetcher

        self.eq = fetcher.convert_table_to_array("eq")  # pylint: disable=invalid-name
        self.total = fetcher.convert_table_to_array("total")
        self.mgn = fetcher.convert_table_to_array("mgn")
        self.drv = fetcher.convert_table_to_array("drv")
