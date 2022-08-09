class MFData:
    def __init__(self, fetcher) -> None:
        self.fetcher = fetcher
        fetcher._login()
        fetcher._set_update()

        self.eq = fetcher.convert_table_to_array("eq")
        self.total = fetcher.convert_table_to_array("total")
        self.mgn = fetcher.convert_table_to_array("mgn")
        self.drv = fetcher.convert_table_to_array("drv")
