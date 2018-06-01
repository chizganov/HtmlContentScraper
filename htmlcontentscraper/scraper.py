from bs4 import BeautifulSoup
from bs4 import NavigableString
import abc
import requests
import format
import sys


class ArticleHtmlScraper:

    def __init__(self, scraper_strategy, format_strategy):
        self.summary_node = scraper_strategy.extract_article()
        self.title = scraper_strategy.extract_title()
        self.text = format_strategy.format(self.title, self.summary_node)

    def get_text(self):
        return self.text


class ScrapingStrategyAbstract(object):

    __metaclass__ = abc.ABCMeta

    def extract_article(self):
        """Required method"""

    def extract_title(self):
        """Required method"""


class EconScrapingStrategy(ScrapingStrategyAbstract):

    # Big-nodes definition (text tags)
    big_nodes = ['p', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'em', 'b', 'i', 'td', 'font']
    # Noise tags that contains unnecessary information
    noise_nodes = ["script", "style", "button", "figcaption"]

    def __init__(self, url):
        try:
            self.html_page = requests.get(url, timeout=5).content
            self.soup = BeautifulSoup(self.html_page, 'html.parser')
            self.title = None
            self.title = self.extract_title()
        except requests.ConnectionError as e:
            print("Connection Error. Make sure you are connected to Internet.")
            print(str(e))
            sys.exit()
        except requests.Timeout as e:
            print("Timeout Error")
            print(str(e))
            sys.exit()
        except requests.RequestException as e:
            print("Request error")
            print(e)
            sys.exit()
        except KeyboardInterrupt:
            print("Someone closed the program")
            sys.exit()

    def extract_article(self):
        '''
        Extract information from html using ECON algorithm.
        Delete noise from html-tree.

        :rtype: bs4.element.Tag
        :return: summary node (node that contains all necessary text)
        '''
        root = self.soup.find("body")
        if not root:
            return None

        # One set of nodes that satisfies the conditions is called as text-node-set:
        # 1) The nodes in the set are all big-nodes,
        # and they are at the same level in the DOM tree and they are adjacent;
        # 2) The nodes in the set together wrap a part of or entire content of news or noise.
        text_node_sets = []

        for node in root.descendants:
            if node is None:
                continue
            if node.parent.name == "set":
                # Set tag already contains text_node_set
                continue
            if node.name in self.noise_nodes:
                # Clear noise nodes like <script>
                node.clear()
            if self.__is_big_node(node):
                node_set = self.__joint_para(node)
                if node_set is not None:
                    text_node_sets.append(node_set)

        if not text_node_sets:
            return None
        # Find snippet_node
        # Snippet node is one node from the text_node_set that wraps the longest text-para
        snippet_set_node = text_node_sets[0]
        for node_set in text_node_sets:
            if len(node_set.text) > len(snippet_set_node.text):
                snippet_set_node = node_set

        # Backtracking while punc_num difference not 0
        # and the text length difference is small between tree levels (some websites has small noises).
        summary_node = snippet_set_node
        while EconScrapingStrategy.__punc_num(summary_node.parent.text) - EconScrapingStrategy.__punc_num(
                summary_node.text) != 0 or len(summary_node.parent.text) - len(
                summary_node.text) < 10:
            summary_node = summary_node.parent
            if summary_node.name == "body":
                break

            # clean tree from noise
            par_classes = summary_node.get("class")
            for child_node in summary_node.parent.children:
                if not child_node.find("set"):
                    child_node.clear()
                if isinstance(child_node, NavigableString):
                    continue
                # Often a web-site article has the same paragraph style (class set)
                if child_node.get("class") != par_classes:
                    child_node.clear()

        return summary_node

    def extract_title(self):
        """
        Extract article title from website and store it in self.title attribute.

        :rtype: str
        :return: title of the article if exists, None otherwise
        """
        if self.title is not None:
            return self.title
        # As stub just return first h1 tag text as title
        h1 = self.soup.find("h1", recursive=True)
        if h1 is not None:
            return h1.text

        return None

    def __joint_para(self, big_node):
        """
        The algorithm of Joint-para merges short pieces of text in text-node-set.
        Some noise may be embedded within some subtrees.

        :type big_node: bs4.element.Tag
        :param big_node: father of the text node
        :rtype: bs4.element.Tag
        :return: set-node that contains text-node-set
        """
        text_node_set = []

        # Traverse direct siblings and add them to the text_node_set if they big-node
        sibling = big_node
        while True:
            sibling = sibling.previous_sibling
            if isinstance(sibling, type(big_node)) and self.__is_big_node(sibling):
                text_node_set.append(sibling)
            else:
                break
        text_node_set.append(big_node)
        sibling = big_node
        while True:
            sibling = sibling.next_sibling
            if isinstance(sibling, type(big_node)) and self.__is_big_node(sibling):
                text_node_set.append(sibling)
            else:
                break
        # Wrap the text-node-set in set-node
        text_node_set_wrapper = self.__wrap_text_node_set(text_node_set)

        return text_node_set_wrapper

    def __is_big_node(self, node):
        if self.big_nodes.__contains__(node.name):
            return True

        return False

    @staticmethod
    def __punc_num(text):
        return text.count(".") + text.count(",") + text.count("，") + text.count("。")

    def __wrap_text_node_set(self, text_node_set):
        wrapper = self.soup.new_tag("set")
        for node in text_node_set:
            node.wrap(wrapper)

        return wrapper


class EconHtmlScraper(ArticleHtmlScraper):

    def __init__(self, url):
        super().__init__(EconScrapingStrategy(url), format.SimpleTxtFormatStrategy())
