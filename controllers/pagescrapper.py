"""File contains controllers for page that gonna be parsed."""

from dataclasses import dataclass
import os
import time
from typing import Optional

import pandas as pd

from RPA.Browser.Selenium import Selenium
from selectorlib import Extractor


def browser_open_and_download_page(path, page_url):
    """Default opener for page."""
    preferences = {
        "download.default_directory": f"{path}",
        "plugins.always_open_pdf_externally": True,
        "download.directory_upgrade": True,
        "download.prompt_for_download": False,
    }
    browser = Selenium()
    browser.open_chrome_browser(
        page_url, preferences=preferences)
    try:
        xpath = "//div[@id='business-case-pdf']//a"
        browser.wait_until_element_is_enabled(xpath, 20)
        browser.click_element_when_visible(xpath)
        time.sleep(15)
        browser.close_window()
    except:
        browser.close_window()


@dataclass
class BaseWebParser:
    """Base class for parsing the data from web-page."""
    parent_xpath: str
    results_path: Optional[str]

    def __post_init__(self):
        self.create_results_folder()
        self.browser = self.get_browser()

    def get_browser(self):
        """Initial setup for the browser driver."""
        return Selenium()

    def browser_open_page(self, page_url):
        """Default opener for page."""
        preferences = {
            "download.default_directory": self.results_path,
            "plugins.always_open_pdf_externally": True,
            "download.directory_upgrade": True,
            "download.prompt_for_download": False,
        }
        self.browser.open_chrome_browser(
            page_url, preferences=preferences)

    def create_results_folder(self):
        """Try to folder where the results will be stored."""
        try:
            os.makedirs(os.path.dirname(self.results_path), exist_ok=True)
        except OSError as e:
            # TODO: Move to cool logger.
            print("Something wrong with creation folder: ", e)

    def parse_page(self, page, selector):
        """Parse page using selectorlib and config with selectors."""
        extractor = Extractor.from_yaml_file(selector)
        return extractor.extract(page)


class ItDashboardParserMixin:

    def open_main_page(self):
        """Open main page."""
        self.browser.open_chrome_browser("https://itdashboard.gov/")

    def open_dive_in(self):
        """Find and click button."""

        xpath = "//a[@href='#home-dive-in']"
        self.browser.wait_until_element_is_enabled(xpath)
        self.browser.click_element_when_visible(xpath)
        self.browser.wait_until_element_is_enabled(
            "//div[@id='agency-tiles-container']//a[.='view']", 50)
        return self.browser.get_source()


class AgencyParser(BaseWebParser, ItDashboardParserMixin):
    """Page parser for https://itdashboard.gov."""
    selector_config_path = f"{os.getcwd()}/selector_configs/agency.yml"

    def __post_init__(self):
        super().__post_init__()
        self.open_main_page()
        page = self.open_dive_in()
        data = self.parse_page(page, self.selector_config_path)
        self.data = pd.DataFrame(data.get('results', []))


@dataclass
class InvestmentParser(BaseWebParser, ItDashboardParserMixin):
    """Parser for detail page for agency."""
    agency_title: str
    selector_config_path = f"{os.getcwd()}/selector_configs/table.yml"

    def __post_init__(self):
        super().__post_init__()
        self.open_main_page()
        self.open_dive_in()
        self.open_agency_page()
        page = self.open_all_selected_table()
        initial_data = self.parse_page(page, self.selector_config_path)
        data = self.serialize_data(initial_data)
        self.data = pd.DataFrame(
            data, columns=['UII', "Bureau", "Investment Title", "Total", "Type", "Cio Rating", "Number of project"])
        self.links = self.get_links(initial_data.get('hrefs'))

    def open_agency_page(self):
        xpath = f"{self.parent_xpath}//span[.='{self.agency_title}']/../../..//a[.='view']"
        self.browser.wait_until_element_is_enabled(xpath)
        self.browser.click_element_when_visible(xpath)

    def open_all_selected_table(self):
        xpath = "//select[@name='investments-table-object_length']"
        self.browser.wait_until_element_is_enabled(xpath, 15)
        self.browser.select_from_list_by_value(xpath, "-1")
        xpath = "//a[@class = 'paginate_button next disabled']"
        self.browser.wait_until_element_is_enabled(xpath, 45)
        xpath = "//table[@id = 'investments-table-object']//tbody"
        return self.browser.get_source()

    def get_pdf_base_url(self, current_location):
        agency_id = current_location.split("/")[-1]
        return f"https://itdashboard.gov/drupal/summary/{agency_id}/"

    def get_links(self, uiis):
        base_url = self.get_pdf_base_url(self.browser.get_location())
        links = [f"{base_url}{x}" for x in uiis]
        return links

    def serialize_data(self, data):
        import numpy as np
        values = data.get("results", {}).get("values", [])
        data_massives = np.array_split(values, len(values)/7)
        return data_massives
