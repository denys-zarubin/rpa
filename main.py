"""Main file to execute the runner."""
import os

from controllers.pagescrapper import AgencyParser, InvestmentParser, browser_open_page, ItDashboardParserMixin
from controllers.aggreagator import merge_data_to_xls
from multiprocessing.pool import Pool


def x(a):
    return a


def run():
    """
    Default runner for parsing data
    """

    output = os.environ.get("RESULTS_PATH", "output").strip('/')
    path = f"{os.getcwd()}/{output}"

    # agency_data = AgencyParser(
    #     parent_xpath="//div[@id='agency-tiles-container']//div[@class='tuck-5']/div[@class='row top-gutter-20']",
    #     results_path=path,
    # )
    investment_data = InvestmentParser(
        agency_title="Department of Commerce",
        parent_xpath="//div[@id='agency-tiles-container']//div[@class='tuck-5']/div[@class='row top-gutter-20']",
        results_path=path,

    )
    with Pool(10) as p:

        p.map(ItDashboardParserMixin().browser_open_page, investment_data.links)

    # merge_data_to_xls(agency_data, investment_data)


if __name__ == "__main__":
    run()
