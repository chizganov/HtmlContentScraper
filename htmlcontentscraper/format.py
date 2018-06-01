import abc
import bs4


class ArticleFormatStrategyAbstract(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def format(self, title, summary_node):
        """Required method"""


class SimpleTxtFormatStrategy(ArticleFormatStrategyAbstract):

    def format(self, title, summary_node):
        '''
        Get text from summary node (node that contains all the necessary text) and format it as:
        - string length not greater than 80;
        - link format: [tag text|href];
        - the block text is separated by with double new-line char.

        :type title: str
        :param title: article titile
        :type summary_node: bs4.element.Tag
        :param summary_node: bs4 node, root of subtree that contains all the text
        :rtype: str
        :return: format string
        '''
        if not isinstance(summary_node, bs4.Tag):
            return None

        text = ""
        max_str_len = 80
        str_len = 0
        # Is last tag wes inline
        prev_inline = False
        for string in summary_node.strings:
            tag = string.parent
            string = str.strip(string)
            # Replace new-line with space in text
            string = string.replace("\n", " ")
            if string == "":
                continue
            elif tag.name == "a":
                string = "[" + string + "|" + tag["href"] + "]"
                prev_inline = True
            elif tag.name == "p" or tag.name == "div":
                # If last tag was inline, block tag continues -> new-line redundant
                if not prev_inline:
                    text += "\n\n"
                    str_len = 0
                prev_inline = False
            else:
                string = " " + string + " "
                prev_inline = True

            # Handle line length restriction
            if str_len + len(string) > max_str_len:
                word_list = string.split(" ")
                for word in word_list:
                    if str_len + len(word) + 1 > max_str_len:
                        text += "\n"
                        str_len = 0
                    else:
                        text += " "
                    text += word
                    str_len += len(word) + 1
            else:
                text += string

        if not title:
            return text
        else:
            return title + text
