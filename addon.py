# -*- coding: utf-8 -*-
import os, sys, ssl, time, datetime, json, re
from kodiswift import Plugin, ListItem, xbmc, xbmcgui, xbmcvfs, xbmcaddon, xbmcplugin, xbmcmixin
from resources.lib import getoauth, TUMBLRAUTH, TumblrRestClient, tumblrsearch
from collections import namedtuple

try:
    from xbmcutil import viewModes
except:
    pass
tclient = TumblrRestClient
viewmode = 20
APIOK = False
plugin = Plugin(name="TumblrV", addon_id="plugin.video.tumblrv", plugin_file="addon.py", info_type="episodes")
__addondir__ = xbmc.translatePath(plugin.addon.getAddonInfo('path'))
__resdir__ = os.path.join(__addondir__, 'resources')
__imgdir__ = os.path.join(__resdir__, 'images')
__imgsearch__ = os.path.join(__imgdir__, 'search.png')
__imgnext__ = os.path.join(__imgdir__, 'next.png')
__imgtumblr__ = os.path.join(__imgdir__, 'tumblr.png')
tagpath = os.path.join(xbmc.translatePath('special://profile/addon_data/'), 'plugin.video.tumblrv', 'tagslist.json')
weekdelta = datetime.timedelta(days=7)
updatedelta = datetime.timedelta(minutes=10)
import web_pdb


def doDebug():
    return bool(plugin.get_setting(key='debugon', converter=bool))


def _json_object_hook(d):
    f = {}
    for k,v in enumerate(d):
        keyname = k.replace("_", "-")
        f.update({keyname: v})
    return namedtuple('tumblr', f.keys(), rename=True)(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)

def makeitem(name=None, img=None, path='blogposts', playable=False, **kwargs):
    #if doDebug():
    xitem = None
    try:
        if not path.startswith('plugin://'):
            itempath = plugin.url_for(endpoint=path, items=kwargs)
        else:
            itempath = path
        lbl2 = kwargs.get("label2", itempath.partition('plugin.video.tumblrv/')[-1])
        if img is None:
            img = "https://api.tumblr.com/v2/blog/{0}/avatar/64".format(name)
        xitem = ListItem(label=name, label2=lbl2, icon=img, thumbnail=img, path=itempath)
        xitem.playable = playable
        xitem.poster = img
        #litem = {'label': name, 'thumbnail': img, 'icon': img, 'is_playable': playable, 'path': itempath)}
        if path == 'blogposts':
            img = "https://api.tumblr.com/v2/blog/{0}/avatar/64".format(name)
        elif plugin.request.path.find('following/') != -1 or plugin.request.path.find('liked/') != -1 or plugin.request.path.find('dashboard/') != -1:
            blogname = kwargs.get('blogname', name)
            ctxaction = "RunPlugin({0})".format(plugin.url_for(endpoint=blogposts, blogname=blogname))
            cname = "[COLOR green]GOTO:[/COLOR] {0}".format(blogname)
            citem = (cname, ctxaction,)
            ctxlist.append(citem)
            vidurl = kwargs.get("vidurl", None)
            if vidurl is not None:
                pathdl = plugin.url_for(endpoint=download, urlvideo=vidurl)
                citem = ('Download', 'RunPlugin({0})'.format(pathdl),)
                ctxlist.append(citem)
            vidid = kwargs.get('id', None)
            if vidid is not None:
                pathaddlike = plugin.url_for(endpoint=addlike, id=vidid)
                citem = ('Like', 'RunPlugin({0})'.format(pathaddlike),)
                ctxlist.append(citem)
        xitem.add_context_menu_items(items=ctxlist, replace_items=False)
    except Exception as ex:
        outmsg = "Error: {0}\n{1}\n{2}\n".format(str(ex), str(ex.message), str(ex.args))
        plugin.notify(msg=outmsg, delay=10000)
        print outmsg
    return xitem


@plugin.route('/')
def index():
    # setview_list()
    litems = []
    itemdashvids = {}
    itemliked = {}
    itemfollowing = {}
    itemtagbrowse = {}
    itemtagged = {}
    itemsearch = {}
    tstamp = str(time.mktime((datetime.datetime.now() - weekdelta).timetuple())).split('.', 1)[0]
    info = {"name": "Not logged in", "likes": 1, "following": 1}
    tinfo = namedtuple("tumblr_info", field_names=info.keys())(*info.values())
    try:
        userinforesp = tclient.info()
        if isinstance(userinforesp, dict):
            info = userinforesp.get("user", {})
            tinfo = namedtuple('tumblr_info', info.keys(), rename=True)(*info.values())
    except:
        plugin.notify("ERROR: Tumblr needs this addon to be authorized.")
    try:
        lbldash = "[B]{0}[/B]'s Dashboard".format(tinfo.name)
        lblfol = "Following: {0}".format(str(tinfo.following))
        lbllike = "Liked: {0}".format(str(tinfo.likes))
        itemdash = ListItem(label=lbldash, icon=__imgtumblr__, path=plugin.url_for(dashboard, offset=0))
        itemfollowing = ListItem(label=lblfol, path=plugin.url_for(blogs_following, offset=0))
        itemliked = ListItem(label=lbllike, path=plugin.url_for(liked, offset=0))
        litems.append(itemdash)
        litems.append(itemfollowing)
        litems.append(itemliked)
        #itemargs = {'offset': 0, 'lastid':0}
        #itemdashvids = makeitem(name='Dashboard Videos', img=__imgtumblr__,  path='dashboard', kwargs=itemargs)
        #itemargs = {'offset':0}
        #itemliked = makeitem(name='Liked Videos', path='liked', kwargs=itemargs)
        #itemfollowing = makeitem(name='Following', path='blogs_following', kwargs=itemargs)
        #itemargs = {'timestamp': str(tstamp)}
        #itemtagbrowse = makeitem(name='Browse Tags', path='taglist', kwargs=itemargs) #dict(timestamp=str(tstamp)))
        #itemargs.update({'tagname': 0})
        #litems.append(itemdash)
        #litems.append(itemfollowing)
        #litems.append(itemliked)
        #litems.append(itemtagbrowse)
    except Exception as ex:
        outmsg = "{0}".format(str(ex))
        plugin.notify(msg=outmsg, delay=7000)
        print outmsg
    return litems


def indexold():
    # curid, previd = get_postids()
    # dashoffset = int(curid)-int(previd) * -1
    itemdashvids = {
        'label': 'Dashboard Videos',
        'thumbnail': __imgtumblr__,
        'path': plugin.url_for(endpoint=dashboard, offset=0, lastid=0),
        'is_playable': False}
    itemliked = {
        'label': 'Liked Videos',
        'thumbnail': __imgtumblr__,
        'path': plugin.url_for(endpoint=liked, offset=0),
        'is_playable': False}
    itemfollowing = {
        'label': 'Following',
        'thumbnail': __imgtumblr__,
        'path': plugin.url_for(endpoint=blogs_following, offset=0),
        'is_playable': False}
    itemtagbrowse = {
        'label': 'Browse Tags',
        'thumbnail': __imgtumblr__,
        'path': plugin.url_for(endpoint=taglist, timestamp=str(tstamp)),
        'is_playable': False}
    itemtagged = {
        'label': 'Search Tags',
        'thumbnail': __imgtumblr__,
        'path': plugin.url_for(endpoint=tags, tagname='0', timestamp=str(tstamp)),
        'is_playable': False}
    itemsearch = {
        'label': 'Search Tumblr',
        'thumbnail': __imgsearch__,
        'path': plugin.url_for(endpoint=search),
        'is_playable': False}


@plugin.route('/setup')
def setup():
    litems = []
    itemappkey = {
        'label': "Consumer KEY: {0}".format(TUMBLRAUTH['consumer_key']),
        'path': plugin.keyboard(default=TUMBLRAUTH['consumer_key'], heading=TUMBLRAUTH['consumer_key'])}
    itemappsecret = {
        'label': "Consumer SECRET: {0}".format(TUMBLRAUTH['consumer_secret']),
        'path': plugin.keyboard(default=TUMBLRAUTH['consumer_secret'], heading=TUMBLRAUTH['consumer_secret'])
    }
    itemurl = {
        'label': 'Visit: https://api.tumblr.com/console/calls/user/info\nenter Key and Secret from this screen',
        'path': plugin.url_for(endpoint=setup)
    }
    litems.append(itemurl)
    litems.append(itemappkey)
    litems.append(itemappsecret)
    return litems


@plugin.route('/setup/get')
def setup_get():
    token = plugin.keyboard(heading="OAUTH TOKEN")
    secret = plugin.keyboard(heading="OAUTH SECRET")
    plugin.set_setting('oauth_token', token)
    plugin.set_setting('oauth_secret', secret)
    TUMBLRAUTH['oauth_secret'] = secret
    TUMBLRAUTH['oauth_token'] = token
    try:
        client = TumblrRestClient(**TUMBLRAUTH)
        APIOK = True
    except:
        plugin.notify("Problem with the Tumblr OAUTH details", "Tumblr Login Failed")


@plugin.route('/liked/<offset>')
def liked(offset=0):
    # setview_thumb()
    likes = {}
    alltags = []
    litems = []
    listlikes = []
    strpage = str(((int(offset) + 20) / 20))
    nextitem = ListItem(label="Next Page -> #{0}".format(int(strpage) + 1), label2="Liked Videos", icon=__imgnext__,
                        thumbnail=__imgnext__, path=plugin.url_for(liked, offset=int(20 + int(offset))))
    nextitem.set_art({'poster': __imgnext__, 'thumbnail': __imgnext__, 'fanart': __imgnext__})
    nextitem.is_folder = True
    # litems = [nextitem]
    results = tclient.likes(limit=20, offset=int(offset))
    if results is not None:
        if results.get('liked_posts', '') is not None:
            listlikes = results.get('liked_posts', '')
        else:
            listlikes = results.get(results.keys()[-1])
    for item in listlikes:
        if item.get('type', '') == 'video':
            b = {}
            b.update(item)
            lbl = ""
            lbl2 = ""
            img = item.get('thumbnail_url', item.get('image_permalink', item.get('image_permalink', "")))
            alltags.extend(item.get('tags', []))
            if img == '':
                img = __imgtumblr__
            try:
                if len(b.get('slug', '')) > 0:
                    lbl = b.get('slug', '')
                elif len(b.get('title', '')) > 0:
                    lbl = b.get('title', '')
                elif len(b.get('caption', '')) > 0:
                    lbl = Strip(b.get('caption', ''))
                elif len(b.get('summary', '')) > 0:
                    lbl = b.get('summary', '')
                elif len(b.get('source_title', '')) > 0:
                    lbl = b.get('source_title', '')
                else:
                    lbl = b.get('short_url', '')
                if len(item.get('summary', '')) > 0:
                    lbl2 = item.get('summary', '')
                else:
                    lbl2 = item.get('blog_name', "") + " / " + item.get('source_title', '') + "(" + item.get(
                        'slug_name', '') + ")"
            except:
                lbl = b.get(b.keys()[0], "")
                lbl2 = b.get(b.keys()[-1], "")
            vidurl = item.get('video_url', "")
            if vidurl is not None and len(vidurl) > 10:
                litem = ListItem(label=lbl, label2=lbl2, icon=img, thumbnail=img, path=vidurl)
                litem.playable = True
                litem.is_folder = False
                if item.get('date', '') is not None:
                    rdate = str(item.get('date', '')).split(' ', 1)[0].strip()
                litem.set_info(info_type='video', info_labels={'Date': rdate})
                litem.set_art({'poster': img, 'thumbnail': img, 'fanart': img})
                pathdl = plugin.url_for(endpoint=download, urlvideo=vidurl)
                litem.add_context_menu_items([('Download', 'RunPlugin({0})'.format(pathdl)), ])
                litems.append(litem)
    savetags(alltags)
    litems.append(nextitem)
    return litems


@plugin.route('/taglist/<timestamp>')
def taglist(timestamp=0):
    # setview_list()
    if not os.path.exists(tagpath):
        json.dump([], fp=open(tagpath, mode='w'))
    litems = []
    alltags = json.load(open(tagpath))
    for tag in alltags:
        turl = plugin.url_for(tags, tagname=tag, timestamp=str(timestamp))
        li = ListItem(label=tag, label2=tag, icon=__imgtumblr__, thumbnail=__imgtumblr__, path=turl)
        li.is_folder = True
        litems.append(li)
    return litems


def setview_list():
    plugin.notify(
        msg="{0} View: {1} / L{2} / T{3}".format(str(plugin.request.path), str(plugin.get_setting('viewmode')),
                                                 str(plugin.get_setting('viewmodelist')),
                                                 str(plugin.get_setting('viewmodethumb'))))
    try:
        if int(plugin.get_setting('viewmodelist')) == 0:
            viewselector = viewModes.Selector(20)
            viewmode = viewselector.currentMode
            plugin.set_setting('viewmodelist', viewmode)
    except:
        plugin.set_setting('viewmodelist', 20)
    plugin.notify(
        msg="{0} View: {1} / L{2} / T{3}".format(str(plugin.request.path), str(plugin.get_setting('viewmode')),
                                                 str(plugin.get_setting('viewmodelist')),
                                                 str(plugin.get_setting('viewmodethumb'))))


def setview_thumb():
    plugin.notify(
        msg="{0} View: {1} / L{2} / T{3}".format(str(plugin.request.path), str(plugin.get_setting('viewmode')),
                                                 str(plugin.get_setting('viewmodelist')),
                                                 str(plugin.get_setting('viewmodethumb'))))
    try:
        if int(plugin.get_setting('viewmodethumb')) == 0:
            viewselector = viewModes.Selector(500)
            viewmode = viewselector.currentMode
            plugin.set_setting('viewmodethumb', viewmode)
    except:
        plugin.set_setting('viewmodethumb', 500)
    plugin.notify(
        msg="{0} View: {1} / L{2} / T{3}".format(str(plugin.request.path), str(plugin.get_setting('viewmode')),
                                                 str(plugin.get_setting('viewmodelist')),
                                                 str(plugin.get_setting('viewmodethumb'))))


@plugin.route('/tags/<tagname>/<timestamp>')
def tags(tagname='', timestamp=0):
    atags = {}
    taglist = []
    litems = []
    if tagname == '0':
        tagname = plugin.keyboard(plugin.get_setting('lastsearch'), 'Search for tags')
        plugin.set_setting('lastsearch', tagname)
    nextstamp = time.mktime((datetime.datetime.fromtimestamp(float(timestamp)) - weekdelta).timetuple())
    nstamp = str(nextstamp).split('.', 1)[0]
    nextitem = ListItem(label="Next -> {0}".format(time.ctime(nextstamp)), label2="Tagged Videos", icon=__imgnext__,
                        thumbnail=__imgnext__, path=plugin.url_for(tags, tagname=tagname, timestamp=nstamp))
    nextitem.set_art({'poster': __imgnext__, 'thumbnail': __imgnext__, 'fanart': __imgnext__})
    nextitem.is_folder = True
    # litems = [nextitem]
    if tagname is not None and len(tagname) > 0:
        results = tclient.tagged(tagname, filter='text')  # ), before=float(timestamp))
        if results is not None:
            for res in results:
                if res.get('type', '') == 'video': taglist.append(res)
        for item in taglist:
            b = {}
            b.update(item)
            lbl = ""
            lbl2 = ""
            img = __imgtumblr__
            if 'thumb' in str(item.keys()[:]):
                if item.get('thumbnail_url', '') is not None:
                    img = item.get('thumbnail_url', '')  # .replace('https', 'http') #item.get('thumbnail_url','')
            elif 'image' in str(item.keys()[:]):
                if item.get('image_permalink', ""):
                    img = item.get('image_permalink', "")
            try:
                plugin.log.debug(msg=item.get('thumbnail_url', ''))
                if len(b.get('slug', '')) > 0:
                    lbl = b.get('slug', '')
                elif len(b.get('title', '')) > 0:
                    lbl = b.get('title', '')
                elif len(b.get('caption', '')) > 0:
                    lbl = Strip(b.get('caption', ''))
                elif len(b.get('summary', '')) > 0:
                    lbl = b.get('summary', '')
                elif len(b.get('source_title', '')) > 0:
                    lbl = b.get('source_title', '')
                else:
                    lbl = b.get('short_url', '')
                if len(item.get('summary', '')) > 0:
                    lbl2 = item.get('summary', '')
                else:
                    lbl2 = item.get('blog_name', "") + " / " + item.get('source_title', '') + "(" + item.get(
                        'slug_name', '') + ")"
            except:
                lbl = b.get(b.keys()[0], "")
                lbl2 = b.get(b.keys()[-1], "")
            vidurl = item.get('video_url', "")
            if vidurl is not None and len(vidurl) > 10:
                litem = ListItem(label=lbl, label2=lbl2, icon=img, thumbnail=img, path=vidurl)
                litem.playable = True
                litem.is_folder = False
                if item.get('date', '') is not None:
                    rdate = str(item.get('date', '')).split(' ', 1)[0].strip()
                litem.set_info(info_type='video', info_labels={'Date': rdate})
                litem.set_art({'poster': img, 'thumbnail': img, 'fanart': img})
                litems.append(litem)
    litems = [nextitem]
    return litems


def dashboard_items(results=[]):
    alltags = []
    litems = []
    for item in results:
        b = {}
        b.update(item)
        vidid = b.get('id', 0)
        ctxlist = []
        lbl = ""
        lbl2 = ""
        vidurl = item.get('video_url', '')
        if vidid != 0:
            pathaddlike = plugin.url_for(endpoint=addlike, id=vidid)
            citemlike = ('Like', 'RunPlugin({0})'.format(pathaddlike),)
            ctxlist.append(citemlike)
        pathtoblog = plugin.url_for(blogposts, blogname=b.get('blog_name', ''), offset=0)
        citemblog = ('View Blog', 'RunPlugin({0})'.format(pathtoblog),)
        ctxlist.append(citemblog)
        pathdl = plugin.url_for(endpoint=download, urlvideo=vidurl)
        citemdl = ('Download', 'RunPlugin({0})'.format(pathdl),)
        ctxlist.append(citemdl)
        img = item.get('thumbnail_url', item.get('image_permalink', __imgtumblr__))
        alltags.extend(item.get('tags', []))
        lbl = b.get('summary', b.get('source_title', b.get('short_url', b.get('title', b.get('blog_name', b.get('source_title', b.get('caption','')))))))
        lbl2 = b.get('blog_name', '') + " " + str(vidid) + " " + b.get('short_url', '')
        from urllib import quote_plus
        if vidurl.find('.mp4') == -1 and len(vidurl) > 0:
            vidurl = "plugin://plugin.video.hubgay/playtumblr/" + quote_plus(vidurl)
        else:
            vidurl = "plugin://plugin.video.hubgay/playmovie/" + quote_plus(b.get('short_url', b.get('source_url', '')))
        litem =  ListItem(label=lbl, label2=lbl2, icon=img, thumbnail=img, path=vidurl)
        litem.playable = True
        litem.is_folder = False
        postdate = item.get('date', datetime.datetime.fromtimestamp(item.get('timestamp', None)).isoformat(sep=' ').rpartition(':')[0])
        if postdate is not None:
            lbl2 += postdate
        else:
            postdate = datetime.datetime.fromtimestamp(item.get('timestamp', 1500000000)).isoformat(sep=' ').rpartition(':')[0]
        postdate = postdate.split(' ', 1)[0]
        litem.set_info(info_type='video', info_labels={'Date': postdate})
        litem.set_art({'poster': img, 'thumbnail': img, 'fanart': img})
        litem.add_context_menu_items(ctxlist)
        litems.append(litem)
    return litems, alltags


def dashboard_getitems(startoffset):
    offset = int(startoffset)
    item = {}
    litems = []
    postslist = []
    for offnum in range(offset, offset+60, 20):
        results = tclient.dashboard(offset=offnum, type='video').get("posts", [])
        if len(results) > 0:
            postslist, alltags = dashboard_items(results)
            savetags(alltags)
            litems.extend(postslist)
    return litems


def get_lastid():
    lastid = 0
    lastid = plugin.get_setting('lastid', int)
    if lastid == 0:
        lastid = 150000000000
    if lastid is None or lastid < 1000000:
        lastid = 150000000000
    return lastid


def get_postids(ForceUpdate=False):
    lastid = get_lastid()
    latestid = lastid
    if shouldUpdate() or ForceUpdate:
        results = tclient.dashboard(limit=1, type='video')
        apost = None
        posts = results.get('posts', None)
        if posts is None:
            posts = results.get('posts', results.get(results.keys()[-1], []))
        if not isinstance(posts, list):
            apost = posts.get(posts.keys()[-1], None)
        else:
            if len(posts) > 0:
                apost = posts.pop()
            else:
                apost = None
        if apost is not None:
            latestid = apost.get('id', lastid)
        if latestid != lastid:
            tstampnow = float(str(time.mktime((datetime.datetime.now()).timetuple())).split('.', 1)[0])
            plugin.set_setting('newid', latestid)
            plugin.set_setting('idupdate', str(tstampnow))
    else:
        latestid = plugin.get_setting('newid')
    return (latestid, lastid)


def shouldUpdate(checkDashboardId=True, checkFollowing=False):
    needsupdate = False
    needupdate = False
    lastup = None
    try:
        if checkFollowing:
            blogpath = tagpath.replace("tagslist.json", "following.json")
            if not os.path.exists(blogpath):
                return True
            lastupdated = plugin.get_setting('lastupdate', converter=str)
        else:
            lastupdated = plugin.get_setting('idupdate', converter=str)
        tstampnow = float(str(time.mktime((datetime.datetime.now()).timetuple())).split('.', 1)[0])
        if tstampnow - float(lastupdated) > 600:
            needsupdate = True
    except Exception as ex:
        errmsg = "**Failed to check whether an update is required. Update requested for**\n  Dashboard Posts: {0} Posts from Followed Blogs: {1}\n** {2} **".format(str(repr(checkDashboardId)), str(repr(checkDashboardId)), str(repr(ex)))
        plugin.log.error(msg=errmsg)
        needsupdate = True
    return True


@plugin.route('/dashboard/<offset>')
def dashboard(offset=0):
    # setview_thumb()
    likes = {}
    listlikes = []
    litems = []
    alltags = []
    nextoff = int(60 + int(offset))
    strpage = str(nextoff / 60)
    pathnext = plugin.url_for(dashboard, offset=nextoff)
    nextitem = ListItem(label="[B]Page #{0}[/B] ->".format(str(int(strpage) + 1)), label2=pathnext, icon=__imgnext__,thumbnail=__imgnext__, path=pathnext)
    nextitem.set_art({'poster': __imgnext__, 'thumbnail': __imgnext__, 'fanart': __imgnext__})
    nextitem.is_folder = True
    litems = [nextitem]
    litems.append(dashboard_getitems(offset))
    return litems


def dashboard_old(listlikes, alltags, litems):
    for item in listlikes:
        if item.get('type', '') == 'video':
            b = item
            img = item.get("thumbnail_url", __imgtumblr__)
            img2 = item.get("image_permalink", __imgtumblr__)
            alltags.extend(item.get('tags', []))
            try:
                if len(b.get('slug', '')) > 0:
                    lbl = b.get('slug', '')
                elif len(b.get('title', '')) > 0:
                    lbl = b.get('title', '')
                elif len(b.get('caption', '')) > 0:
                    lbl = Strip(b.get('caption', ''))
                elif len(b.get('summary', '')) > 0:
                    lbl = b.get('summary', '')
                elif len(b.get('source_title', '')) > 0:
                    lbl = b.get('source_title', '')
                else:
                    lbl = b.get('short_url', '')
                if len(item.get('summary', '')) > 0:
                    lbl2 = item.get('summary', '')
                else:
                    lbl2 = item.get('blog_name', '') + " / " + item.get('source_title', '') + "(" + item.get(
                        'slug_name', '') + ")"
            except:
                lbl = b.get('blog_name', '')
                lbl2 = b.get('short_url', '')
            vidurl = item.get('video_url', '')
            img = item.get('thumbnail_url',
                           item.get('image_permalink', item.get('image_permalink', __imgtumblr__))).replace('https:',
                                                                                                            'http:')
            img2 = item.get('image_permalink',
                            item.get('thumbnail_url', item.get('thumbnail_url', __imgtumblr__))).replace('https:',
                                                                                                         'http:')
            if vidurl is not None and len(vidurl) > 10:
                if len(b.get('caption', '')) > 0:
                    lbl = Strip(b.get('caption', ''))
                litem = ListItem(label=lbl, label2=lbl2, icon=img2, thumbnail=img, path=vidurl)
                litem.playable = True
                litem.is_folder = False
                if item.get('date', '') is not None:
                    rdate = str(item.get('date', '')).split(' ', 1)[0].strip()
                litem.set_info(info_type='video', info_labels={'Date': rdate})
                litem.set_art({'poster': img2, 'thumbnail': img, 'fanart': img2})
                pathdl = plugin.url_for(endpoint=download, urlvideo=vidurl)
                pathaddlike = plugin.url_for(endpoint=addlike, id=item.get('id', ''))
                litem.add_context_menu_items(
                    [('Download', 'RunPlugin({0})'.format(pathdl)), ('Like', 'RunPlugin({0})'.format(pathaddlike)),
                     ('Show Image', 'ShowPicture({0})'.format(img)), ])
                litems.append(litem)
    item = listlikes[-1]
    plugin.set_setting('lastid', str(item.get('id', lastid)))
    savetags(alltags)
    # litems.append(nextitem)
    return litems


@plugin.route('/addlike/<id>')
def addlike(id=0):
    try:
        tclient.like(None, id)
        plugin.notify(msg="LIKED: {0}".format(str(id)))
    except:
        plugin.notify(msg="Failed to add like: {0}".format(str(id)))


@plugin.route('/download/<urlvideo>')
def download(urlvideo):
    try:
        from YDStreamExtractor import getVideoInfo
        from YDStreamExtractor import handleDownload
        info = getVideoInfo(urlvideo, resolve_redirects=True)
        dlpath = plugin.get_setting('downloadpath')
        if not os.path.exists(dlpath):
            dlpath = xbmc.translatePath("home://")
        handleDownload(info, bg=True, path=dlpath)
    except:
        plugin.notify(urlvideo, "Download Failed")


def refresh_following():
    # blogpath = tagpath.replace("tagslist.json", "following.json")
    # needsupdate = False
    # if not os.path.exists(blogpath):
    #    needsupdate = True
    # lastupdated = plugin.get_setting('lastupdate')
    # tstamp = str(time.mktime((datetime.datetime.now() - updatedelta).timetuple())).split('.', 1)[0]
    # tstampnow = float(str(time.mktime((datetime.datetime.now()).timetuple())).split('.', 1)[0])
    # if tstampnow - float(lastupdated) > 600:
    #    needsupdate = True
    if not shouldUpdate(checkFollowing=True):
        allblogs = []
        allblogs_temp = []
        allblogs_temp = json.load(fp=open(tagpath.replace("tagslist.json", "following.json"), mode='r'))
        for blog in allblogs:
            newblog = dict(blog)
            newblog['description'] = Strip(blog['description'])
            allblogs.append(newblog)
        return allblogs
    from operator import itemgetter
    litems = []
    allblogs = []
    blogs = []
    offset = 0
    total = 0
    resp = tclient.following(offset=0, limit=20)  # tclient.dashboard(type='videos')
    results = resp.get('blogs', {})
    total = len(results)  # int(results.get('total_blogs', 0))
    for offset in range(0, total, 20):
        resp = tclient.following(offset=offset, limit=20)
        # results = resp.get('response', {})
        blogs = resp.get('blogs', [])  # results.get('blogs', [])
        blogs.sort(key=itemgetter('updated'), reverse=True)
        for item in blogs:
            allblogs.append(item)
    allblogs.sort(key=itemgetter('updated'), reverse=True)
    save_following(allblogs)
    plugin.set_setting('lastupdate', str(time.mktime((datetime.datetime.now()).timetuple())).split('.', 1)[0])
    return allblogs


def get_following():
    allfollowedblogs = []
    if doDebug():
        web_pdb.set_trace()
        with web_pdb.catch_post_mortem():
            allfollowedblogs = refresh_following()
            save_following(allblogs=allfollowedblogs)
            return allfollowedblogs
    else:
        allfollowedblogs = refresh_following()
        save_following(allblogs=allfollowedblogs)
        return allfollowedblogs


def save_following(allblogs=[]):
    blogpath = tagpath.replace("tagslist.json", "following.json")
    outlist = []
    for blog in allblogs:
        newblog = {}
        newblog.update(blog)
        newblog['thumb'] = u'http://api.tumblr.com/v2/blog/{0}/avatar/64'.format(blog.get('name', 'tumblr'))
        newblog['description'] = Strip(blog.get('description', ''))
        outlist.append(newblog)
    json.dump(outlist, fp=open(blogpath, mode='w'))


def following_list(offset=0, max=0):
    litems = []
    blogs = []
    offset = 0
    total = 0
    resp = tclient.following(offset=offset)  # tclient.dashboard(type='videos')
    blogs = resp.get('blogs', [])
    if max == 0:
        total = len(blogs)
        if total > 250: total = 250
    else:
        total = 20 + max
    offend = offset + 20
    if offend > len(blogs):
        offend = len(blogs)
    results = get_following()
    start = 0
    end = len(results)
    if len(results) > offset:
        start = offset
    if offend < len(results):
        end = offend
    else:
        end = len(results)
    blogres = results[start:end]
    try:
        for blog in blogres:
            assert isinstance(blog, dict)
            updatetext = datetime.datetime.fromtimestamp(blog.get('updated'), 0).isoformat()
            #updatetext = "[B]{0}:{1}[/B] [I]{2}/{3}[/I]".format(updatedate.time().hour, updatedate.time().minute, updatedate.day, updatedate.month)
            blogname = blog.get('name', '')
            thumb = "https://api.tumblr.com/v2/blog/{0}/avatar/64".format(blogname)
            description = blog.get('description', '').partition('\n')[0]
            if len(description) > len(blogname) * 2:
                splitidx = description.find('.')
                if splitidx != -1:
                    if splitidx < len(blogname):
                        splitidx + 10
                else:
                    splitidx = description.find(',')
                    if splitidx == -1:
                        splitidx = len(blogname) + 10
                if splitidx < len(blogname):
                    splitidx = len(blogname)
                about = str(description[0:splitidx]).strip() + '..'
            else:
                about = description.strip()
                if about.find('>') != -1:
                    about = about.partition('>')[-1].strip()
            about = "{0}".format(about)
            if thumb == '':
                thumb = "https://api.tumblr.com/v2/blog/{0}/avatar/64".format(blog.get('name', __imgtumblr__))
                #if thumbn.get('avatar_url', None):
                #    thumb = thumbn.get('avatar_url', __imgtumblr__)
                #else:
                #    thumb = __imgtumblr__
            newitem = {'name': blogname, 'thumb': thumb, 'updated': updatetext, 'description': about}
            litems.append(newitem)
        return litems
    except Exception as ex:
        print str(repr(ex))
        litems = results
    return litems


@plugin.route('/blogsfollowing/<offset>')
def blogs_following(offset=0):
    blogs = {}
    litems = []
    blogres = []
    listblogs = []
    litems = []
    name = ''
    updated = ''
    url = ''
    desc = ''
    strpage = str(((int(offset) + 20) / 20))
    nextitem = ListItem(label="Next Page -> #{0}".format(int(strpage) + 1), label2="More", icon=__imgnext__,
                        thumbnail=__imgnext__, path=plugin.url_for(blogs_following, offset=int(20 + int(offset))))
    nextitem.set_art({'poster': __imgnext__, 'thumbnail': __imgnext__, 'fanart': __imgnext__})
    nextitem.is_folder = True
    litems = [nextitem]
    results = following_list(offset=offset, max=20)  # max not working right now, max=50)
    for b in results:
        thumb = 'https://api.tumblr.com/v2/blog/{0}/avatar/64'.format(name) #__imgtumblr__
        try:
            thumbd = {}
            name = b.get(u'name', '')
            title = b.get(u'title', '')
            desc = Strip(b.get(u'description', ''))
            url = b.get(u'url', "http://{0}.tumblr.com".format(name))
            updated = b.get(u'updated', 0)
            updatetext = datetime.datetime.fromtimestamp(updated)#.isoformat()
            thumb = 'https://api.tumblr.com/v2/blog/{0}/avatar/64'.format(name)
            iurl = plugin.url_for(endpoint=blogposts, blogname=name, offset=0)
            lbl = "[COLOR yellow][B]{0}[/B][/COLOR] ({2}:{3} {4}/{5})\n[I]{1}[/I]".format(name, title.encode('latin-1', 'ignore'), updatetext.hour, updatetext.minute, updatetext.day, updatetext.month)
            lbl2 = title + "\n" + desc.encode('latin-1', 'ignore')
            litem = ListItem(label=lbl, label2=lbl2, icon=thumb, thumbnail=thumb, path=iurl)
            litem.set_art({'poster': thumb, 'thumbnail': thumb, 'fanart': thumb})
            litem.is_folder = True
            litem.playable = False
            litems.append(litem)
        except:
            pass
    return litems


@plugin.route('/blogposts/<blogname>/<offset>')
def blogposts(blogname, offset=0):
    listposts = []
    lbl = ''
    lbl2 = ''
    vidurl = ''
    results = []
    alltags = []
    litems = []
    if blogname.find('.') != -1:
        shortname = blogname.split('.', 1)[-1]
        if shortname.find('.') != -1:
            blogname = shortname.lsplit('.')[0]
    strpage = str((20 + int(offset)) / 20)
    nextitem = ListItem(label="Next Page -> #{0}".format(strpage), label2=blogname, icon=__imgnext__,
                        thumbnail=__imgnext__,
                        path=plugin.url_for(blogposts, blogname=blogname, offset=int(20 + int(offset))))
    nextitem.set_art({'poster': __imgnext__, 'thumbnail': __imgnext__, 'fanart': __imgnext__})
    nextitem.is_folder = True
    # litems = [nextitem]
    results = tclient.posts(blogname=blogname, limit=20, offset=int(offset), type='video')
    if results is not None:
        if len(results.get('posts', '')) > 1:
            results = results.get('posts', '')
        for post in results:
            lbl2 = post.get('blog_name', '')
            lbl = post.get('slug', '').replace('-', ' ')
            img = post.get('thumbnail_url', post.get('image_permalink', __imgtumblr__))
            img2 = post.get('image_permalink', post.get('thumbnail_url', __imgtumblr__))
            alltags.extend(post.get('tags', []))
            try:
                if post.get('slug', '') is not None:
                    lbl = post.get('slug', '').replace('-', ' ')
                if len(post.get('caption', '')) > 0:
                    lbl = Strip(post.get('caption', ''))
                elif len(post.get('summary', '')) > 0:
                    lbl = post.get('summary', '')
                elif len(post.get('source_title', '')) > 0:
                    lbl = post.get('source_title', '')
                else:
                    lbl = post.get('short_url', '')
                if post.get('video_url', '') is not None:
                    vidurl = post.get('video_url', '')
            except:
                plugin.notify(str(repr(post)))
            litem = ListItem(label=lbl, label2=lbl2, icon=img2, thumbnail=img, path=vidurl)
            litem.playable = True
            litem.is_folder = False
            if len(post.get('date', '')) > 0:
                rdate = str(post.get('date', '')).split(' ', 1)[0].strip()
            litem.set_info(info_type='video', info_labels={'Date': rdate, 'Duration': post.get('duration', '')})
            litem.set_art({'poster': img2, 'thumbnail': img, 'fanart': img2})
            pathdl = plugin.url_for(endpoint=download, urlvideo=vidurl)
            pathaddlike = plugin.url_for(endpoint=addlike, id=post.get('id', ''))
            litem.add_context_menu_items(
                [('Download', 'RunPlugin({0})'.format(pathdl)), ('Like', 'RunPlugin({0})'.format(pathaddlike)), ])
            litems.append(litem)
    else:
        litems = []
        backurl = ''
        if offset == 0:
            backurl = plugin.url_for(endpoint=blogs_following, offset=0)
        else:
            backurl = plugin.url_for(blogposts, blogname=blogname, offset=(int(offset) - 20))
        nextitem = ListItem(label="No Results - GO BACK".format(strpage), label2=blogname, icon=__imgtumblr__,
                            thumbnail=__imgtumblr__, path=backurl)
        nextitem.set_art({'poster': __imgtumblr__, 'thumbnail': __imgtumblr__, 'fanart': __imgtumblr__})
        nextitem.is_folder = True
        litems = [nextitem]
    savetags(alltags)
    litems.append(nextitem)
    return litems


@plugin.route('/posts/<blogname>/<offset>')
def posts(blogname, offset=0):
    postdata = tclient.posts(blogname=blogname, type='text', filter='video', offset=offset)
    postdata = postdata.get('response', {})
    postdata = postdata.get('posts', {"posts": [{"__type__": "Post"}]})
    listdata = json2obj(postdata)
    assert isinstance(listdata, namedtuple)


@plugin.route('/search')
def search():
    # plugin.log.debug(TUMBLRAUTH)
    # client = TumblrRestClient(**TUMBLRAUTH)
    # info = client.info()
    litems = []
    searchtxt = ''
    searchquery = ''
    offsetnum = 0
    searchtxt = plugin.get_setting('lastsearch')
    searchtxt = plugin.keyboard(searchtxt, 'Search All Sites', False)
    searchquery = searchtxt.replace(' ', '+')
    plugin.set_setting(key='lastsearch', val=searchtxt)
    results = following_list(offset=offsetnum)
    listmatch = []
    max = 20
    # if len(results) < 20:
    #    max = len(results) - 1
    for blog in results:
        name = blog.get('name', '')
        posts = tclient.posts(name, type='video')
        for post in posts.get('posts', []):
            for k, v in post.items():
                try:
                    if searchquery.lower() in str(v.encode('latin-1', 'ignore')).lower():
                        listmatch.append(post)
                        break
                except:
                    pass
    plugin.notify(msg="Matches: {0}".format(str(len(listmatch))))
    alltags = []
    for post in listmatch:
        lbl2 = post.get('blog_name', '')
        lbl = post.get('slug', '').replace('-', ' ')
        img = post.get('thumbnail_url', post.get('image_permalink', __imgtumblr__))
        img2 = post.get('image_permalink', post.get('thumbnail_url', __imgtumblr__))
        alltags.extend(post.get('tags', []))
        try:
            if post.get('slug', '') is not None:
                lbl = post.get('slug', '').replace('-', ' ')
            if len(post.get('caption', '')) > 0:
                lbl = Strip(post.get('caption', ''))
            elif len(post.get('summary', '')) > 0:
                lbl = post.get('summary', '')
            elif len(post.get('source_title', '')) > 0:
                lbl = post.get('source_title', '')
            else:
                lbl = post.get('short_url', '')
            if post.get('video_url', '') is not None:
                vidurl = post.get('video_url', '')
        except:
            plugin.notify(str(repr(post)))
        litem = ListItem(label=lbl, label2=lbl2, icon=img2, thumbnail=img, path=vidurl)
        litem.playable = True
        litem.is_folder = False
        if len(post.get('date', '')) > 0:
            rdate = str(post.get('date', '')).split(' ', 1)[0].strip()
        litem.set_info(info_type='video', info_labels={'Date': rdate, 'Duration': post.get('duration', '')})
        litem.set_art({'poster': img2, 'thumbnail': img, 'fanart': img2})
        pathdl = plugin.url_for(endpoint=download, urlvideo=vidurl)
        pathaddlike = plugin.url_for(endpoint=addlike, id=post.get('id', ''))
        litem.add_context_menu_items(
            [('Download', 'RunPlugin({0})'.format(pathdl)), ('Like', 'RunPlugin({0})'.format(pathaddlike)), ])
        litems.append(litem)
    savetags(alltags)
    return litems


def savetags(taglist=[]):
    if not os.path.exists(tagpath):
        json.dump([], fp=open(tagpath, mode='w'))
    taglist.extend(json.load(open(tagpath, mode='r')))
    alltags = sorted(set(taglist))
    json.dump(alltags, fp=open(tagpath, mode='w'))


def Strip(text):
    notagre = re.compile(r'<.+?>')
    return notagre.sub(' ', text).strip()


if __name__ == '__main__':
    TUMBLRAUTH = dict(consumer_key='5wEwFCF0rbiHXYZQQeQnNetuwZMmIyrUxIePLqUMcZlheVXwc4',
                      consumer_secret='GCLMI2LnMZqO2b5QheRvUSYY51Ujk7nWG2sYroqozW06x4hWch',
                      oauth_token='7OaJ7GOFwVxi4VnquAY7E7kcJ3LMX7B0WcIX1zakhQ2p46xxDj',
                      oauth_secret='RdF74sWaG0N6GXQo0P7iq1wLIutkYaHoSf05WX5rFYrMMmcXKk')
    try:
        tclient = TumblrRestClient(**TUMBLRAUTH)
        if tclient is not None:
            info = tclient.info()
            print info
            APIOK = True
    except:
        tclient = None
        APIOK = False
        print "Couldn't get TumblrRestClient object"
    try:
        if tclient is None and not APIOK:
            otoken = plugin.get_setting('oauth_token')
            osecret = plugin.get_setting('oauth_secret')
            TUMBLRAUTH.update({'oauth_token': otoken, 'oauth_secret': osecret})
            tclient = TumblrRestClient(**TUMBLRAUTH)
            info = tclient.info()
            if info is not None and 'user' in info.keys():
                APIOK = True
            else:
                APIOK = False
    except:
        APIOK = False
        try:
            TUMBLRAUTH = getoauth()
            tclient = TumblrRestClient(**TUMBLRAUTH)
            info = tclient.info()
            if info is not None and info.get('user', None) is not None:
                APIOK = True
            else:
                APIOK = False
        except:
            plugin.notify(
                msg="Required Tumblr OAUTH token missing..Backup plan!",
                title="Tumblr Login Failed", delay=10000)
            plugin.log.error(
                msg="Tumblr API OAuth settings invalid. This addon requires you to authorize this Addon in your Tumblr account and in turn in the settings you must provide the TOKEN and SECRET that Tumblr returns.\nhttps://api.tumblr.com/console/calls/user/info\n\tUse the Consumer Key and Secret from the addon settings to authorize this addon and the OAUTH Token and Secret the website returns must be put into the settings.")
            try:  # Try an old style API key from off github as a backup so some functionality is provided?
                TUMBLRAUTH = dict(consumer_key='5wEwFCF0rbiHXYZQQeQnNetuwZMmIyrUxIePLqUMcZlheVXwc4',
                                  consumer_secret='GCLMI2LnMZqO2b5QheRvUSYY51Ujk7nWG2sYroqozW06x4hWch',
                                  oauth_token='RBesLWIhoxC1StezFBQ5EZf7A9EkdHvvuQQWyLpyy8vdj8aqvU',
                                  oauth_secret='GQAEtLIJuPojQ8fojZrh0CFBzUbqQu8cFH5ejnChQBl4ljJB4a')
                TUMBLRAUTH.update({'api_key', '5wEwFCF0rbiHXYZQQeQnNetuwZMmIyrUxIePLqUMcZlheVXwc4'})
                tclient = TumblrRestClient(**TUMBLRAUTH)
            except:
                plugin.notify(msg="Read Settings for instructions", title="COULDN'T AUTH TO TUMBLR")
    viewmode = int(plugin.get_setting('viewmode'))
    plugin.run()    
    #txtout = "-=**" + ("*"*10) + " {0} " + ("*"*10) + "**=-"
    #reqout = "PATH: {0} QUERY: {1}\nURL: {2} ARGS: {3}".format(str(plugin.request.path), str(plugin.request.query_string), str(plugin.request.url), str(plugin.request.args))
    #txtout = txtout.format(reqout)
    #plugin.log.info(msg=txtout)
    #print (txtout)
    ctxlist = []
    plugin.set_content(content='episodes')
    viewmodel = 551
    viewmodet = 500
    if str(plugin.request.path).startswith('/taglist/') or str(plugin.request.path).startswith('/dashboard/')  or plugin.request.path == '/': #or str(plugin.request.path).startswith('/blogsfollowing/')
        viewmodel = int(plugin.get_setting('viewmodelist'))
        if viewmodel == 0: viewmodel = 551
        plugin.set_view_mode(viewmodel)
    else:
        viewmodet = int(plugin.get_setting('viewmodethumb'))
        if viewmodet == 0: viewmodet = 500
        plugin.set_view_mode(viewmodet)
