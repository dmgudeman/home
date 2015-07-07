# -----------------------------------------------------------------------------
# Name:        crawler.py
# Purpose:     a simple web crawler
#
# Author:      David Gudeman
# Date:        July 4, 2015
# -----------------------------------------------------------------------------
"""
implement a simple web crawler

Usage: crawler.py seed_url
seed: absolute url - the crawler will use it as the initial web address
"""


import urllib.request
import urllib.parse
import urllib.error
import urllib.robotparser
import re
import sys
import textwrap

MAX_URLS = 10

# DO NOT CHANGE ok_to_crawl!!!
def ok_to_crawl(absolute_url):
    """
    check if it is OK to crawl the specified absolute url

    We are implementing polite crawling by checking the robots.txt file
    for all urls except the ones using the file scheme (these are urls
    on the local host and they are all OK to crawl.)
    We also use this function to skip over mailto: links and javascript: links.
    Parameter:
    absolute_url (string):  this is an absolute url that we would like to crawl
    Returns:
    boolean:  True if the scheme is file (it is a local webpage)
              True if we successfully read the corresponding robots.txt
                   file and determined that user-agent * is allowed to crawl
              False if it is a mailto: link or a javascript: link
                   if user-agent * is not allowed to crawl it or
                   if it is NOT an absolute url.
    """
    if absolute_url.lower().startswith('mailto:'):
        return False
    if absolute_url.lower().startswith('javascript:'):
        return False
    link_obj=urllib.parse.urlparse(absolute_url)
    if link_obj.scheme.lower().startswith('file'):
        return True
    # check if the url given as input is an absolute url
    if not link_obj.scheme or not link_obj.hostname:
        print('Not a valid absolute url: ', absolute_url)
        return False
    #construct the robots.txt url from the scheme and host name
    else:
        robot_url= link_obj.scheme+'://'+link_obj.hostname + '/robots.txt'
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robot_url)
        try:
            rp.read()
        except:
            print ("Error accessing robot file: ", robot_url)
            return False
        else:
            return rp.can_fetch("*", absolute_url)


# DO NOT CHANGE crawl!!!
def crawl(seed_url):
    """
    start with the seed_url and crawl up to 10 urls

    Parameter:
    seed_url (string) - this is the first url we'll visit.
    Returns:
    set of strings - set of all the urls we have visited.
    """
    urls_tocrawl = {seed_url}  # initialize our set of urls to crawl
    urls_visited = set()  # initialize our set of urls visited
    while urls_tocrawl and len(urls_visited) < MAX_URLS:
        current_url= urls_tocrawl.pop() # just get any url from the set
        if current_url not in urls_visited: # check if we have crawled it
            page = get_page(current_url)
            if page:
                more_urls = extract_links(current_url, page) # get the links
                urls_tocrawl = urls_tocrawl | more_urls # add them
                urls_visited.add(current_url)
    return urls_visited

#------------Do not change anything above this line----------------------------

def get_page(url):
    # TO DO:
    # get_page takes an absolute url as input parameter
    # and returns a string that contains the web page pointed to by that url.
    # Assume the web page uses utf-8 encoding.
    # If there is an error opening the url or decoding the content,
    # print a message identifying the url and the error and
    # return an empty string.
    # Use the with construct to open the url.
    empty_string = ''
    try:
        with urllib.request.urlopen(url) as url_file:
            page = url_file.read()
            decoded_page = page.decode('utf-8')
    except urllib.error.URLError as url_err:
        print('ERROR OPENING url: \n', url, url_err)
        return empty_string
    except UnicodeDecodeError as decode_err:
        print('ERROR DECODING url, could be utf-8 issue: \n', url, decode_err )
        return empty_string

    return decoded_page

def extract_links(base_url, page):
    """
    extract the links contained in the page at the base_url
    Parameters:
    base_url (string): the url we are currently crawling - web address
    page(string):  the content of that url - html
    Returns:
    A set of absolute urls (set of strings) - These are all the urls extracted
        from the current url and converted to absolute urls.

    """

    url_list = []               # initialize list to catch urls
    href_url = r'(<a\s*href\s*=\s*")(\S*)("\S|"\s)'  # url search pattern
    pat_list = re.findall(href_url, page)
    for member in pat_list:
        joined_url = urllib.parse.urljoin(base_url, member[1])  # joins to base
        get_ok = ok_to_crawl(joined_url)  # check putative crawlee site for ok
        if get_ok:
            url_list.append(joined_url)  # if ok then add qualified url to list
    url_set = set(url_list)              # convert list to set

    return url_set

def write_file(crawl_path):
    """
    writes up to ten url to a text file

    if there is no file, it makes a file and writes up to ten urls to file
    in the working directory
    :param crawl_path:
    :return: appends up to ten urls to a text file
    """
    counter = 0
    with open('crawled.txt', 'a', encoding='utf-8') as url_file:
        for url in crawl_path:
            if counter <= 10:
                url_file.write(url + '\n')
                counter += 1

def main():
    if len(sys.argv) > 2:
        sys.exit('Error, too many arguments. Only provide seed url')
    try:
        seed_url = sys.argv[1]          # collect seed url from command line
        print("webcrawler working......")
        crawl_path = crawl(seed_url)
        write_file(crawl_path)

    except IndexError:
        print("Usage:", sys.argv[0], 'seed url')
        sys.exit()


if __name__ == '__main__':
    main()