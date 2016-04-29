import scraper
import sys
import urllib
import urlparse
import xbmcplugin
import xbmcgui
import xbmc

addon_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
page = args.get("page", [None])[0]


def build_url(query):
    return addon_url + '?' + urllib.urlencode(query)


def get_videos():
    videos = scraper.list_videos()
    for video in videos:
        url = build_url({"page": "resolve", "url": video["url"]})
        li = xbmcgui.ListItem(video["label"], iconImage="DefaultVideo.png")
        xbmcplugin.addDirectoryItem(handle=addon_handle,
                                    url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)


if page is None:
    scraper.login(xbmcplugin.getSetting(addon_handle, 'username'), xbmcplugin.getSetting(addon_handle, 'password'))
    get_videos()
elif page == "resolve":
    xbmc.Player().play(scraper.resolve_url(args.get("url")[0]))
