"""
TPB search results getter.\n
Use Getter(search: str) and .tltm or .page to read the results.
"""

import bs4
import typing
import requests
import dataclasses
from os import environ
import selenium.webdriver
from os.path import exists
from selenium import webdriver

tltm = typing.TypeVar("tltm")

# call if parameters invalid
class InvalidParameters(ValueError):
    """
    Exception to call if parameters are invalid.
    """

    pass


# call if driver not in PATH
class NoDriver(Exception):
    """
    Exception to call if a valid webdriver isn't found in PATH
    """

    pass


# dataclass for storing link, name, and magnet
@dataclasses.dataclass
class TLTM:
    link: list
    name: list
    magnet: list
    all: list


# the getter
class Getter:

    # conversion from int to sort and category list
    _title = {
        1: "Order by Category",
        2: "Order by Name",
        3: "Order by Date Uploaded",
        5: "Order by Size",
        6: "Order by Seeders",
        7: "Order by Leechers",
        8: "Order by ULed by",
    }
    _cats = ["all", "audio", "video", "apps", "games", "porn", "other"]
    _limit: int = 1
    _d_name: str | None = None

    # tltm: top link, title, magnet. page is the html source.
    page: str
    tltm: tltm = TLTM

    # init with arguments
    def __init__(
        self,
        search: str,
        url: str = "",
        order: int = 6,
        cat: str = "all",
        limit: int = 1,
    ) -> None:
        """
        Getter for TPB.\n
        :param search: str with your search terms
        :param url: optional, default first result on https://proxy-bay.one/
        :param order: optional, default 6
        :param cat: optional, default "all"
        :param limit: optional, default 1
        :return: None
        """
        if url == "":
            self._url: str = self.top_proxy()
        else:
            self._url: str = url
        self._search: str = search
        self._order: int = order
        self._cat: str = cat

        self._limit = limit

        # call request method
        self._api(self._url, self._search, self._order, self._cat)

    # request method
    def _api(self, url: str, search: str, order: int, cat: str) -> None:

        # what driver is installed
        self._what_driver()

        # checks if the parameters are valid
        if type(url) != str:
            raise InvalidParameters(
                'url must be a string. format -> "https://address.extension".'
            )
        elif type(search) != str:
            raise InvalidParameters("search must be a string.")
        elif order not in self._title.keys():
            raise InvalidParameters(
                "order must be an int. format -> 1, 2, 3, 5, 6, 7, 8"
            )
        elif cat not in self._cats:
            raise InvalidParameters(
                "cat must be a string. "
                'format -> "all", "audio", "video", "apps", "games", "porn", "other".'
            )

        # check driver and do getting
        match self._d_name:
            case "geckodriver.exe":
                # setup headless
                options = selenium.webdriver.FirefoxOptions()
                options.headless = True

                # selenium get results and sort
                with webdriver.Firefox(options=options) as driver:
                    driver.get(f"{url}/search.php?q={search}&{cat}=on")
                    sorter = driver.find_element(
                        by="xpath", value=f'//label[@title="{self._title[order]}"]'
                    )
                    sorter.click()

                    # set page attribute
                    self.page = driver.page_source.encode("ascii", "replace").decode(
                        "utf-8"
                    )

            case "chromedriver.exe":
                options = selenium.webdriver.ChromeOptions()
                options.headless = True

                with webdriver.Chrome(options=options) as driver:
                    driver.get(f"{url}/search.php?q={search}&{cat}=on")
                    sorter = driver.find_element(
                        by="xpath", value=f'//label[@title="{self._title[order]}"]'
                    )
                    sorter.click()

                    self.page = driver.page_source.encode("ascii", "replace").decode(
                        "utf-8"
                    )

            case "msedgedriver.exe":
                options = selenium.webdriver.EdgeOptions()
                options.headless = True

                with webdriver.Edge(options=options) as driver:
                    driver.get(f"{url}/search.php?q={search}&{cat}=on")
                    sorter = driver.find_element(
                        by="xpath", value=f'//label[@title="{self._title[order]}"]'
                    )
                    sorter.click()

                    self.page = driver.page_source.encode("ascii", "replace").decode(
                        "utf-8"
                    )

            case "IEDriverServer.exe":
                options = selenium.webdriver.IeOptions()
                options.headless = True

                with webdriver.Ie(options=options) as driver:
                    driver.get(f"{url}/search.php?q={search}&{cat}=on")
                    sorter = driver.find_element(
                        by="xpath", value=f'//label[@title="{self._title[order]}"]'
                    )
                    sorter.click()

                    self.page = driver.page_source.encode("ascii", "replace").decode(
                        "utf-8"
                    )

        # call parser
        self.top_link_title_magnet(url, self.page)

    # parser and tltm setter
    def top_link_title_magnet(self, url: str, source: str) -> tltm:
        """
        Gets the top link, title, and magnet from a TPB results page.\n
        :param url: str with the TPB proxy url
        :param source: html page
        :return: instance of TLTM = [link, name, magnet].
        """

        # parser
        parsed = bs4.BeautifulSoup(source, "html.parser")
        names = parsed.find_all(
            "span", {"class": "list-item item-name item-title"}, limit=self._limit
        )
        links = parsed.find_all(
            "span", {"class": "list-item item-name item-title"}, limit=self._limit
        )
        magnets = parsed.find_all(
            "span", {"class": "item-icons"}, limit=self._limit + 1
        )

        # setter
        link, name, magnet = [], [], []
        for i in range(len(names)):
            name.append(names[i].findNext().getText())
            link.append(url + links[i].findNext().get("href"))
            magnet.append(magnets[i + 1].findNext().get("href"))

        self.tltm = self.tltm(link, name, magnet, list(zip(link, name, magnet)))
        return self.tltm

    # get top proxy url
    def top_proxy(self) -> str:
        url_proxy = "https://proxy-bay.one/"
        proxy_get = requests.request("get", url_proxy).text
        proxy = bs4.BeautifulSoup(proxy_get, "html.parser")

        # get first result and make url; search terms
        self._url = "http://" + proxy.find("a", {"class": "t1"}).text
        return self._url

    # find what driver is installed
    def _what_driver(self):
        envar = environ["PATH"].split(";")
        wd = [
            "chromedriver.exe",
            "msedgedriver.exe",
            "geckodriver.exe",
            "IEDriverServer.exe",
        ]

        for ev in envar:
            for d in wd:
                if exists(ev + "\\" + d):
                    self._d_name = d
                    break
        if self._d_name is None:
            raise NoDriver
