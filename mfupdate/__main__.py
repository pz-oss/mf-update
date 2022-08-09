import logging
import os

from lib.gspreadsheet import GSpreadsheetService
from mfupdate.data import MFData
from mfupdate.fetcher import MFFetcher

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


if __name__ == "__main__":

    logging.info("start fetcher")
    fetcher = MFFetcher(url=os.environ["MF_BASE_URL"])
    data = MFData(fetcher)

    logger.debug(data.total)
    GSpreadsheetService().update("mfupdate_total", 1, 1, data.total)

    logger.debug(data.eq)
    GSpreadsheetService().update("mfupdate_eq", 1, 1, data.eq)
    # logger.debug(data.mgn)
    # logger.debug(data.drv)
    # h2c.table_to_list()
