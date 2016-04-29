from bs4 import BeautifulSoup
import urllib2
import urllib
import re
import cookielib
import os
import xbmcplugin
import sys

MAIN_URL = "https://www.tytnetwork.com/annual-archives/2015-archives/"
NAME_REGEX = re.compile(r"(?<=turks-)\w+-[0-9]+-[0-9]+")
LOGIN_URL = "https://www.tytnetwork.com/wp-login.php?wpe-login=tyt"
COOKIE_FILE = "./cookies.txt"

addon_handle = int(sys.argv[1])


def setup_cookies():
    cj = cookielib.MozillaCookieJar(COOKIE_FILE)
    if os.access(COOKIE_FILE, os.F_OK):
        cj.load(ignore_discard=True)
        opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=0),
                                      urllib2.HTTPSHandler(debuglevel=0),
                                      urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
    return cj


def login(username, password):
    cj = setup_cookies()
    data = urllib.urlencode({
        "log": username,
        "pwd": password,
        "wp-submit": "Log In",
        "rememberme": "forever",
        "redirect_to": "https://www.tytnetwork.com/login/",
        "wppb_login": "true",
        "wppb_form_location": "page",
        "wppb_request_url": "https://www.tytnetwork.com/login/",
        "wppb_lostpassword_url": "/lost-password/",
        "wppb_redirect_priority": "",
        "wppb_referer_url": ""
    })

    req = urllib2.Request("https://www.tytnetwork.com/login/",
                          headers={'User-Agent': "Mozilla/5.0"})
    cj.extract_cookies(urllib2.urlopen(req), req)
    req = urllib2.Request(LOGIN_URL, data, headers={"user-agent": "Mozilla/5.0"})
    cj.extract_cookies(urllib2.urlopen(req), req)
    cj.save()


def resolve_url(url):
    setup_cookies()
    req = urllib2.Request(url, headers={'User-Agent': "Chrome"})
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    return soup.find("source").get('src')


def list_videos():
    req = urllib2.Request(MAIN_URL, headers={'User-Agent': "Chrome"})
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    links = soup.findAll('a', class_="arc-vid-watch")
    return [{
        'url': link.get('href'),
        'label': NAME_REGEX.search(link.get('href')).group(0)
        .replace('-', ' ').capitalize() + ' - ' + link.string
    } for link in links if link.string is not None
        and link.get('href') is not None
        and NAME_REGEX.search(link.get('href')) is not None]
