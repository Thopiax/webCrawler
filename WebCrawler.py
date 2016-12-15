#!/usr/local/bin/python3

# sys: to load command line arguments
import sys
# json: to output the results
import json
# requests: to connect to the servers
import requests
# bs4: to parse the HTML
from bs4 import BeautifulSoup
# webCrawlerUtil: all regular expression matching functions
import WebCrawlerUtil as Util
# urllib: handle urls 
from urllib.parse import urljoin
# robotexclusionruleparser: handle robots.txt
from robotexclusionrulesparser import RobotExclusionRulesParser
# pdb: debug
import pdb

from collections import OrderedDict

USER_AGENT  = '*'
MAX_VISIT_COUNT = 100

class CrawlerController(object):

    def __init__(self, url):
        self.pages_visited = []
        url = urljoin(url, "/")
        # initialize the url and the pages to visit
        self.pages_to_visit = set([url])
        self.visit_count = 0
        # get robot.txt permissions
        self.robot_handler = self.__get_robot_handler(url)

    @staticmethod
    def __get_robot_handler(url):
        rp = RobotExclusionRulesParser()
        if Util.is_url(url):
            # get the original base url
            base_url = Util.get_base_url(url)
            page = requests.get(urljoin(base_url, 'robots.txt'))
            rp.fetch(urljoin(base_url, 'robots.txt'))
        return rp

    def can_visit(self, url):
        # can visit the url if:
        #   - the robots.txt allows it
        #   - haven't visited it yet
        return self.robot_handler.is_allowed(USER_AGENT, url) and url not in self.pages_visited

    def add_to_visit(self, urls):
        # add all the pages we can visit to 
        self.pages_to_visit.update(filter(self.can_visit, urls))

    def collect(self):
        # set up results variable
        result = []
        while self.pages_to_visit and self.visit_count < MAX_VISIT_COUNT:
            # get a url from the pages to be visited
            url = self.pages_to_visit.pop()
            crawler = Crawler(url)
            result.append(crawler.get_static_assets())
            self.pages_visited.append(url) 
            self.add_to_visit(crawler.get_links())

            self.visit_count += 1

        if (self.visit_count == MAX_VISIT_COUNT):
            print("Ended due to exceeded visit count")

        return result


class Crawler(object):
    
    def __init__(self, url):
        self.url = url
        self.parser = None

    def __load_parsed_HTML(self):
        # isolate web connections and requests to only this method
        if not self.parser:
            try:
                # get the requests from the url
                page = requests.get(self.url)
            except requests.exceptions.ConnectionError as e:
                print("The page {} does not seem to exist".format(self.url))
                raise e
            except requests.exceptions.MissingSchema as e:
                print("The given url is not well defined.")
                raise e
            else:
                # parse the html file
                self.parser = BeautifulSoup(page.content, "html.parser")


    def get_static_assets(self):
        result = OrderedDict()

        self.__load_parsed_HTML()

        result['url'] = self.url
        # get all assets in the page
        image_elements  = self.get_asset(Util.get_images)
        script_elements = self.get_asset(Util.get_scripts)
        css_elements    = self.get_asset(Util.get_stylesheets)
        # add them to the result
        result['assets'] = (image_elements + script_elements + css_elements)

        return result

    def get_links(self):
        # get links in page
        return self.get_asset(Util.get_links)

    def get_asset(self, asset_func):
        # collect the locations with the given function (e.g. '../../web')
        # add the url to the locations 
        return [urljoin(self.url, x) for x in asset_func(self.parser)]

def main():

    urls = []
    results = []

    # check for stin parameters
    if len(sys.argv) < 2:
        raise AttributeError("Need at least one url to parse")
    # store the given urls
    urls = sys.argv[1:]

    for website in urls:
        # create an instance of the crawler
        cc = CrawlerController(website)
        results += cc.collect()

    # print the results as a JSON to the stdout
    print(json.dumps(results, indent=4))

if __name__ == '__main__':
    main()