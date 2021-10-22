"""Main file to execute the runner."""
import os

from controllers.pagescrapper import AgencyParser, InvestmentParser, browser_open_and_download_page, ItDashboardParserMixin
from controllers.aggreagator import merge_data_to_xls
from multiprocessing.pool import Pool
from functools import partial
from distutils.util import strtobool


def get_path():
    output = os.environ.get("RESULTS_PATH", "output").strip('/')
    path = f"{os.getcwd()}/{output}"
    return path


def run():
    """
    Default runner for parsing data
    """
    path = get_path()

    agency_data = AgencyParser(
        parent_xpath="//div[@id='agency-tiles-container']//div[@class='tuck-5']/div[@class='row top-gutter-20']",
        results_path=path,
    )
    investment_data = InvestmentParser(
        agency_title="Department of Commerce",
        parent_xpath="//div[@id='agency-tiles-container']//div[@class='tuck-5']/div[@class='row top-gutter-20']",
        results_path=path,

    )
    enabled_multiporcessing = strtobool(
        os.environ.get("ENABLED_MULTIPROSSING", 'false'))
    download_and_open = partial(browser_open_and_download_page, path)
    if enabled_multiporcessing:
        with Pool(2) as p:
            p.map(download_and_open, investment_data.links)
    else:
        for item in investment_data.links:
            download_and_open(item)

    merge_data_to_xls("agency", path, agency_data.data, investment_data.data)


if __name__ == "__main__":
    run()
