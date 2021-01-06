import os
import re
import sys
import urllib
from urllib import urlencode

import random
import cookielib
import urllib2
import urlparse
import xbmc
import xbmcgui
import xbmcplugin
from urlparse import parse_qsl
import xbmcplugin, xbmcaddon, xbmcgui, xbmc

_url = sys.argv[0]
_handle = int(sys.argv[1])

addon = xbmcaddon.Addon()

addon_path = addon.getAddonInfo('path')

__addonname__ = addon.getAddonInfo('id')

__datapath__ = xbmc.translatePath('special://profile/addon_data/' + __addonname__)

avatar = xbmc.translatePath('special://profile/addon_data/' + __addonname__ + '/icon.png')

args = urlparse.parse_qs(sys.argv[2][1:])

VIDEOS = {"Favorites": [{'name': "Futurama",
                         'thumb': addon_path + "/thumb/thumb_futurama.jpg",
                         'video': "",
                         'genre': 'TV Shows'
                         }]
          }


def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def get_categories():
    return VIDEOS.iterkeys()


def get_videos(category):
    return VIDEOS[category]


def getusersearch():
    kb = xbmc.Keyboard('default', 'heading')
    kb.setDefault('')
    kb.setHeading('Enter The Name For A Cartoon')
    kb.setHiddenInput(False)
    kb.doModal()
    if (kb.isConfirmed()):
        search_term = kb.getText()
        return (search_term)
    else:
        return
        mode = args.get('mode', None)


def show_get(url):
    get_show(url)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def search_show():
    show_name = getusersearch()
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    html = opener.open("https://www.toonova.net/toon/search?key=" + show_name).read()
    links = re.findall('<a href="(.*?)"><img src="', html)
    photos = re.findall('"><img src="(.*?)" width="120" height="168" alt="', html)
    names = re.findall('">(.*?)</a></h3>', html)
    for row in range(len(photos)):
        list_item = xbmcgui.ListItem(label=names[row])
        list_item.setArt({
            'thumb': photos[row],
            'icon': photos[row],
            'fanart': addon_path + "/fanart.jpg"})
        list_item.setInfo('video', {'title': names[row],
                                    'genre': names[row],
                                    'mediatype': 'video'})
        url = get_url(action='get_show', category=links[row])
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def list_categories():
    xbmcplugin.setPluginCategory(_handle, 'Commercials')
    xbmcplugin.setContent(_handle, 'videos')
    categories = [['Favorites', 'listing_favorites', '/icon_fav.png'], ['Search', 'search', '/icon_search.png'],['Random Shuffle Loop','shfl_loop','']]
    for category in categories:
        list_item = xbmcgui.ListItem(label=category[0])
        list_item.setArt({
            'thumb': addon_path + category[2],
            'icon': addon_path + category[2],
            'fanart': addon_path + "/fanart.jpg"})
        list_item.setInfo('video', {'title': category[0],
                                    'genre': category[0],
                                    'mediatype': 'video'})

        url = get_url(action=category[1])
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def get_episode(category):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    html = opener.open(category).read()
    link = re.findall('</span></div><div><iframe src="(.*?)"', html)[0]
    html = opener.open(link).read()
    link = re.findall('file: "(.*?)"', html)[0]
    liz = xbmcgui.ListItem("", iconImage="", thumbnailImage="");
    liz.setInfo(type="Video", infoLabels={"Title": "Show"})
    xbmc.Player().play(link, liz, False)

def shfl_loop():
    links = ['Simpsons', "Bob's Burger", "American Dad", "South Park", "King Of The Hill", "Archer", "Family Guy"]
    while True:
        random.shuffle(links)
        name = links[0].replace(' ','+')
        search_link = "https://www.toonova.net/toon/search?key=" + name
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        html = opener.open(search_link).read()
        show_links = re.findall('<h3><a href="(.*?)">',html)
        random.shuffle(show_links)
        html = opener.open(show_links[0]).read()
        episode_link = re.findall('&nbsp;&nbsp;<a href="(.*?)">', html)
        random.shuffle(episode_link)
        with open("file.txt", "w") as file_new:
            file_new.write(episode_link[0])
        file_new.close()
        get_episode(episode_link[0])
        from time import sleep
        sleep(1200)

def get_show(url1):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    html = opener.open(url1).read()
    link = re.findall('&nbsp;&nbsp;<a href="(.*?)">', html)
    links = []
    for row in range(1, len(link) - 1):
        links.append(link[-row])
    name = re.findall('">(.*?)</a>', html)
    names = []
    for row in range(1, len(name)):
        if "episode " in name[-row].lower():
            names.append(name[-row])
    for row in range(len(links)):
        list_item = xbmcgui.ListItem(label=names[row])
        list_item.setInfo('video', {'title': names[row],
                                    'genre': names[row],
                                    'mediatype': 'video'})
        list_item.setArt(
            {'thumb': "", 'icon': "", 'fanart': addon_path + "/fanart.jpg"})
        list_item.setProperty('IsPlayable', 'true')
        url = get_url(action='episode', category=links[row])
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    if "?page" in url1:
        list_item = xbmcgui.ListItem(label="Next Page")
        list_item.setInfo('video', {'title': "Next Page",
                                    'genre': "",
                                    'mediatype': 'video'})
        list_item.setArt(
            {'thumb': addon_path + "/icon.png", 'icon': addon_path + "/icon.png", 'fanart': addon_path + "/fanart.jpg"})
        list_item.setProperty('IsPlayable', 'true')
        url2 = url1 + "11"
        url2 = re.findall("page=(.*?)11", url2)[0]
        url1 = url1.replace(str(url2), "")
        if not url2:
            categ = url1.replace("?page=", "")
        else:
            categ = url1 + str(int(url2) - 1)
        url = get_url(action='show', category=categ)
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
        xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(_handle)


def list_videos(category):
    allow = True
    xbmcplugin.setPluginCategory(_handle, category)
    xbmcplugin.setContent(_handle, 'videos')
    shows = []
    if "Rick And Morty" == category:
        file = open(addon_path + "/links/rick_and_morty.txt", "r").read().split()
        file_screenshots = open(addon_path + "/links/rick_and_morty_screenshots.txt", "r").read().split()
        for row in range(0, 41):
            show = []
            show.append(file[row])
            show.append("Rick And Morty Episode " + str(int(row + 1)))
            show.append(file_screenshots[row])
            shows.append(show)
    if "Bob's Burger" == category:
        allow = False
        get_show("http://www.toonova.net/bobs-burgers?page=4")
        xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(_handle)
    if "American Dad" == category:
        allow = False
        for row in range(1, 16):
            if row == 14:
                pass
            else:
                get_show("http://www.toonova.net/american-dad-season-" + str(row))
        xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(_handle)
    if "Simpsons (Seasons 1-15)" == category:
        allow = False
        get_show("http://www.toonova.net/the-simpsons?page=3")
        for row in range(7, 16):
            get_show("https://www.toonova.net/the-simpsons-season-" + str(row))
        xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(_handle)
    if "Simpsons (Seasons 15-Present)" == category:
        allow = False
        for row in range(15, 32):
            get_show("https://www.toonova.net/the-simpsons-season-" + str(row))
        xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(_handle)
    if "South Park" == category:
        allow = False
        for row in range(1, 24):
            get_show("http://www.toonova.net/south-park-season-" + str(row))
        xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(_handle)
    if "King Of The Hill" == category:
        allow = False
        get_show("http://www.toonova.net/king-of-the-hill?page=6")
        xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(_handle)
    if "Archer" == category:
        allow = False
        get_show("http://www.toonova.net/archer?page=3")
        xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(_handle)
    if "Family Guy" == category:
        allow = False
        for row in range(1,19):
            get_show("https://www.toonova.net/family-guy-season-"+ str(row))
        xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(_handle)
    if allow:
        for show in shows:
            list_item = xbmcgui.ListItem(label='')
            list_item.setInfo('video', {'title': show[1],
                                        'genre': show[1],
                                        'mediatype': 'video'})
            list_item.setArt(
                {'thumb': show[2], 'icon': show[2], 'fanart': addon_path + "/fanart.jpg"})
            list_item.setProperty('IsPlayable', 'true')
            url = show[0]
            is_folder = False
            xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
        xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(_handle)


def Favorites():
    categories = ['Simpsons (Seasons 1-15)', "Rick And Morty", "Bob's Burger", "American Dad",
                  "Simpsons (Seasons 15-Present)", "South Park", "King Of The Hill", "Archer", "Family Guy"]
    thumbs = ["/thumb/thumb_simpsons.jpg", "/thumb/ram_thumb.jpg", "/thumb/bobs_burger_thumb.jpg",
              "/thumb/american_dad_thumb.jpg", "/thumb/thumb_simpsons2.jpg", "/thumb/south_park_thumb.jpg",
              "/thumb/koth_thumb.jpg", "/thumb/archer_thumb.jpg","/thumb/family_guy_thumb.jpg"]
    x = 0
    for category in categories:
        list_item = xbmcgui.ListItem(label=category)
        list_item.setArt({
            'thumb': addon_path + thumbs[x],
            'icon': addon_path + thumbs[x],
            'fanart': addon_path + "/fanart.jpg"})
        list_item.setInfo('video', {'title': category,
                                    'genre': category,
                                    'mediatype': 'video'})
        url = get_url(action='listing', category=category)
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
        x += 1
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def play_video(path):
    play_item = xbmcgui.ListItem(path=path)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'listing':
            list_videos(params['category'])
        elif params['action'] == 'play':
            play_video(params['video'])
        elif params['action'] == 'listing_favorites':
            Favorites()
        elif params['action'] == 'episode':
            get_episode(params['category'])
        elif params['action'] == 'show':
            get_show(params['category'])
        elif params['action'] == 'search':
            search_show()
        elif params['action'] == 'get_show':
            show_get(params['category'])
        elif params['action'] == 'shfl_loop':
            shfl_loop()
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        list_categories()


if __name__ == '__main__':
    router(sys.argv[2][1:])
