# re: to use regular expressions
import re

base_url_pattern = re.compile("http(s)?:\/\/(.+)(\.[a-z]+)+")
domain_pattern = re.compile("^(?!(http[s]?:\/\/|mailto:|linkto:))[^#]*$")

def search_pattern(pattern, text):
    result = pattern.search(text)
    # a domain_name should always be matched in the url
    if result != None:
        return result.group(0)
    else:
        raise LookupError("The pattern doesn't match anything in the text!")

def is_under_domain(html):
    return html and domain_pattern.match(html)

def get_base_url(url):
    return search_pattern(base_url_pattern, url)

def is_url(url):
    return base_url_pattern.match(url)

# Parsing HTML
def get_scripts(parser):
    return get_elem(parser, "script", src=True)
def get_images(parser):
    return get_elem(parser, "img", src=True)
def get_stylesheets(parser):
    return get_elem(parser, "link", href=True, rel="stylesheet")
def get_links(parser):
    return get_elem(parser, "a", href=is_under_domain)

# helper method for 3 methods above
def get_elem(parser, elemName, **kwargs):
    attribute = "src"
    if (kwargs.get("href")):
        attribute = "href"

    elements = parser.find_all(elemName, **kwargs)
    return [elem.attrs[attribute] for elem in elements]
