
class Dashboard(list):

    def __init__(self, **kwargs):
        """
        : attribute value : array
        : attribute posts : array
        : attribute class_property : string
        : attribute type_property : string
        : attribute name : string
        """
        super(Dashboard, self).__init__()
        #self.__value = None
        #self.posts = None
        #self.__class__ = type("Dashboard") #_property = None
        self.__type__ = type(self, **kwargs) #type_property = None
        #self.name = None
        postlist = kwargs.get("posts", [])
        self.__posts__ = Posts(**postlist)
        for post in postlist:
            self.append(Post(**post))
            #self.__posts__.append(Post(**post))

    @property
    def posts(self, **kwargs):
        return self.__posts__
    @posts.setter
    def posts(self, value):
        if isinstance(value, list):
            self.__init__(**value)
        elif isinstance(value, Post):
            self.append(value)
        elif isinstance(value, dict):
            self.append(Post(**value))

class Theme(object):

    def __init__(self, **kwargs):
        """
        : attribute title_font_weight : string
        : attribute header_image_scaled : string
        : attribute header_focus_width : float
        : attribute header_bounds : string
        : attribute show_description : bool
        : attribute avatar_shape : string
        : attribute show_avatar : bool
        : attribute show_title : bool
        : attribute header_full_height : float
        : attribute header_stretch : bool
        : attribute background_color : string
        : attribute link_color : string
        : attribute header_focus_height : float
        : attribute title_color : string
        : attribute header_image : string
        : attribute body_font : string
        : attribute show_header_image : bool
        : attribute title_font : string
        : attribute header_full_width : float
        : attribute header_image_focused : string
        """
        self.title_font_weight = None
        self.header_image_scaled = None
        self.header_focus_width = None
        self.header_bounds = None
        self.show_description = None
        self.avatar_shape = None
        self.show_avatar = None
        self.show_title = None
        self.header_full_height = None
        self.header_stretch = None
        self.background_color = None
        self.link_color = None
        self.header_focus_height = None
        self.title_color = None
        self.header_image = None
        self.body_font = None
        self.show_header_image = None
        self.title_font = None
        self.header_full_width = None
        self.header_image_focused = None


class Blogs(object):

    def __init__(self, **kwargs):
        """
        : attribute primary : bool
        : attribute facebook : string
        : attribute twitter_send : bool
        : attribute admin : bool
        : attribute messages : float
        : attribute ask_page_title : string
        : attribute tweet : string
        : attribute class_property : string
        : attribute is_nsfw : bool
        : attribute updated : float
        : attribute url : string
        : attribute description : string
        : attribute ask_anon : bool
        : attribute type_property : string
        : attribute type_property : string
        : attribute posts : float
        : attribute can_send_fan_mail : bool
        : attribute drafts : float
        : attribute likes : float
        : attribute ask : bool
        : attribute name : string
        : attribute facebook_opengraph_enabled : string
        : attribute name : string
        : attribute followed : bool
        : attribute subscribed : bool
        : attribute is_blocked_from_primary : bool
        : attribute twitter_enabled : bool
        : attribute followers : float
        : attribute is_adult : bool
        : attribute reply_conditions : string
        : attribute share_likes : bool
        : attribute queue : float
        : attribute title : string
        : attribute can_subscribe : bool
        : attribute total_posts : float
        """
        self.primary = None
        self.facebook = None
        self.twitter_send = None
        self.admin = None
        self.messages = None
        self.ask_page_title = None
        self.tweet = None
        self.class_property = None
        self.is_nsfw = None
        self.updated = None
        self.url = None
        self.description = None
        self.ask_anon = None
        self.type_property = None
        self.type_property = None
        self.posts = None
        self.can_send_fan_mail = None
        self.drafts = None
        self.likes = None
        self.ask = None
        self.name = None
        self.facebook_opengraph_enabled = None
        self.name = None
        self.followed = None
        self.subscribed = None
        self.is_blocked_from_primary = None
        self.twitter_enabled = None
        self.followers = None
        self.is_adult = None
        self.reply_conditions = None
        self.share_likes = None
        self.queue = None
        self.title = None
        self.can_subscribe = None
        self.total_posts = None


class Photos(object):

    def __init__(self, **kwargs):
        """
        : attribute caption : string
        : attribute original_size : OriginalSize
        : attribute alt_sizes : array
        """
        self.caption = None
        self.original_size = None
        self.alt_sizes = None


class Liked(object):

    def __init__(self, **kwargs):
        """
        : attribute value : array
        : attribute liked_posts : array
        : attribute class_property : string
        : attribute type_property : string
        : attribute liked_count : float
        : attribute name : string
        """
        self.value = None
        self.liked_posts = None
        self.class_property = None
        self.type_property = None
        self.liked_count = None
        self.name = None


class Reblog(object):

    def __init__(self, **kwargs):
        """
        : attribute class_property : string
        : attribute type_property : string
        : attribute comment : string
        : attribute name : string
        : attribute tree_html : string
        """
        self.class_property = None
        self.type_property = None
        self.comment = None
        self.name = None
        self.tree_html = None


class Posts(list):

    def __init__(self, **kwargs):
        """
        : attribute value : array
        : attribute reblog : Reblog
        : attribute summary : string
        : attribute id_property : float
        : attribute blog_name : string
        : attribute trail : array
        : attribute source_title : string
        : attribute state : string
        : attribute post_url : string
        : attribute source_url : string
        : attribute slug : string
        : attribute player : array
        : attribute can_send_in_message : bool
        : attribute class_property : string
        : attribute duration : float
        : attribute html5_capable : bool
        : attribute type_property : string
        : attribute short_url : string
        : attribute caption : string
        : attribute type_property : string
        : attribute posts : array
        : attribute liked : bool
        : attribute thumbnail_width : float
        : attribute display_avatar : bool
        : attribute name : string
        : attribute followed : bool
        : attribute date : string
        : attribute reblog_key : string
        : attribute can_like : bool
        : attribute can_reblog : bool
        : attribute format : string
        : attribute tags : array
        : attribute thumbnail_url : string
        : attribute note_count : float
        : attribute thumbnail_height : float
        : attribute video_type : string
        : attribute can_reply : bool
        : attribute video_url : string
        : attribute total_posts : float
        : attribute timestamp : float
        """
        super(Posts, self).__init__()
        for post in kwargs.get('posts', []):
            self.append(Post(**post)) #'(self.append()
        self.value = None
        self.reblog = None
        self.recommended_source = None
        self.summary = None
        self.id_property = None
        self.blog_name = None
        self.trail = None
        self.source_title = None
        self.state = None
        self.post_url = None
        self.source_url = None
        self.slug = None
        self.player = None
        self.can_send_in_message = None
        self.class_property = None
        self.duration = None
        self.html5_capable = None
        self.type_property = None
        self.short_url = None
        self.caption = None
        self.type_property = None
        self.posts = None
        self.liked = None
        self.thumbnail_width = None
        self.display_avatar = None
        self.name = None
        self.followed = None
        self.date = None
        self.reblog_key = None
        self.can_like = None
        self.can_reblog = None
        self.format = None
        self.tags = None
        self.thumbnail_url = None
        self.recommended_color = None
        self.note_count = None
        self.thumbnail_height = None
        self.video_type = None
        self.can_reply = None
        self.video_url = None
        self.total_posts = None
        self.timestamp = None
        for k,v in kwargs:
            try:
                self.__setattr__(k, v)
            except:
                pass


class OriginalSize(object):

    def __init__(self, **kwargs):
        """
        : attribute url : string
        : attribute width : float
        : attribute height : float
        """
        self.url = None
        self.width = None
        self.height = None


class User(object):

    def __init__(self, **kwargs):
        """
        : attribute type_property : string
        : attribute blogs : array
        : attribute name : string
        : attribute following : float
        : attribute default_post_format : string
        : attribute class_property : string
        : attribute likes : float
        : attribute name : string
        """
        self.type_property = None
        self.blogs = None
        self.name = None
        self.following = None
        self.default_post_format = None
        self.class_property = None
        self.likes = None
        self.name = None


class BlogPost(object):

    def __init__(self, **kwargs):
        """
        : attribute reblog : Reblog
        : attribute summary : string
        : attribute id_property : float
        : attribute blog_name : string
        : attribute trail : array
        : attribute post_url : string
        : attribute state : string
        : attribute can_send_in_message : bool
        : attribute player : array
        : attribute slug : string
        : attribute class_property : string
        : attribute source_url : string
        : attribute updated : float
        : attribute url : string
        : attribute duration : float
        : attribute text : string
        : attribute description : string
        : attribute html5_capable : bool
        : attribute photo : string
        : attribute source_title : string
        : attribute type_property : string
        : attribute short_url : string
        : attribute caption : string
        : attribute liked_posts : LikedPosts
        : attribute type_property : string
        : attribute liked : bool
        : attribute thumbnail_width : float
        : attribute name : string
        : attribute display_avatar : bool
        : attribute name : string
        : attribute date : string
        : attribute reblog_key : string
        : attribute followed : bool
        : attribute can_like : bool
        : attribute can_reblog : bool
        : attribute format : string
        : attribute video : string
        : attribute audio : string
        : attribute tags : array
        : attribute thumbnail_url : string
        : attribute note_count : float
        : attribute thumbnail_height : float
        : attribute video_type : string
        : attribute can_reply : bool
        : attribute video_url : string
        : attribute title : string
        : attribute timestamp : float
        """
        self.reblog = None
        self.recommended_source = None
        self.summary = None
        self.id_property = None
        self.blog_name = None
        self.trail = None
        self.post_url = None
        self.state = None
        self.can_send_in_message = None
        self.player = None
        self.slug = None
        self.class_property = None
        self.source_url = None
        self.updated = None
        self.url = None
        self.duration = None
        self.text = None
        self.description = None
        self.html5_capable = None
        self.photo = None
        self.source_title = None
        self.type_property = None
        self.short_url = None
        self.caption = None
        self.liked_posts = None
        self.type_property = None
        self.liked = None
        self.thumbnail_width = None
        self.name = None
        self.display_avatar = None
        self.name = None
        self.date = None
        self.reblog_key = None
        self.followed = None
        self.can_like = None
        self.can_reblog = None
        self.format = None
        self.video = None
        self.audio = None
        self.tags = None
        self.thumbnail_url = None
        self.recommended_color = None
        self.note_count = None
        self.thumbnail_height = None
        self.video_type = None
        self.can_reply = None
        self.video_url = None
        self.title = None
        self.timestamp = None


class PostType(object):

    def __init__(self, **kwargs):
        """
        : attribute value : array
        : attribute class_property : string
        : attribute type_property : string
        : attribute name : string
        """
        self.__value__ = None


class Trail(object):

    def __init__(self, **kwargs):
        """
        : attribute type_property : string
        : attribute post : (null)
        : attribute content : string
        : attribute name : string
        : attribute class_property : string
        : attribute content_raw : string
        : attribute blog : Blog
        """
        self.type_property = None
        self.post = None
        self.content = None
        self.name = None
        self.class_property = None
        self.content_raw = None
        self.blog = None


class Player(object):

    def __init__(self, **kwargs):
        """
        : attribute class_property : string
        : attribute type_property : string
        : attribute width : float
        : attribute name : string
        : attribute embed_code : string
        """
        self.class_property = None
        self.type_property = None
        self.width = None
        self.name = None
        self.embed_code = None


class Following(list):

    def __init__(self, **kwargs):
        """
        : attribute value : array
        : attribute class_property : string
        : attribute type_property : string
        : attribute total_blogs : float
        : attribute name : string
        : attribute blogs : array
        """
        super(Following, self).__init__()
        self.total_blogs = kwargs.get('total_blogs', None)
        self.blogs = kwargs.get('blogs', [])


class Blog(object):

    def __init__(self, **kwargs):
        """
        : attribute share_following : bool
        : attribute description : string
        : attribute is_blocked_from_primary : bool
        : attribute active : bool
        : attribute ask : bool
        : attribute likes : float
        : attribute url : string
        : attribute title : string
        : attribute followed : bool
        : attribute ask_page_title : string
        : attribute ask_anon : bool
        : attribute updated : float
        : attribute name : string
        : attribute name : string
        : attribute share_likes : bool
        : attribute subscribed : bool
        : attribute can_be_followed : bool
        : attribute total_posts : float
        : attribute can_send_fan_mail : bool
        : attribute is_nsfw : bool
        : attribute posts : float
        : attribute theme : Theme
        : attribute is_adult : bool
        : attribute class_property : string
        : attribute can_subscribe : bool
        : attribute type_property : string
        : attribute reply_conditions : string
        """
        self.share_following = None
        self.description = None
        self.is_blocked_from_primary = None
        self.active = None
        self.ask = None
        self.likes = None
        self.url = None
        self.title = None
        self.followed = None
        self.ask_page_title = None
        self.ask_anon = None
        self.updated = None
        self.name = None
        self.name = None
        self.share_likes = None
        self.subscribed = None
        self.can_be_followed = None
        self.total_posts = None
        self.can_send_fan_mail = None
        self.is_nsfw = None
        self.posts = None
        self.theme = None
        self.is_adult = None
        self.class_property = None
        self.can_subscribe = None
        self.type_property = None
        self.reply_conditions = None


class LikedPosts(object):

    def __init__(self, **kwargs):
        """
        : attribute reblog : Reblog
        : attribute summary : string
        : attribute id_property : float
        : attribute blog_name : string
        : attribute trail : array
        : attribute post_url : string
        : attribute state : string
        : attribute source_title : string
        : attribute source_url : string
        : attribute slug : string
        : attribute can_send_in_message : bool
        : attribute class_property : string
        : attribute type_property : string
        : attribute short_url : string
        : attribute caption : string
        : attribute type_property : string
        : attribute liked : bool
        : attribute display_avatar : bool
        : attribute name : string
        : attribute followed : bool
        : attribute date : string
        : attribute can_like : bool
        : attribute reblog_key : string
        : attribute can_reblog : bool
        : attribute format : string
        : attribute tags : array
        : attribute note_count : float
        : attribute can_reply : bool
        : attribute photos : array
        : attribute image_permalink : string
        : attribute liked_timestamp : float
        : attribute timestamp : float
        """
        self.reblog = None
        self.recommended_source = None
        self.summary = None
        self.id_property = None
        self.blog_name = None
        self.trail = None
        self.post_url = None
        self.state = None
        self.source_title = None
        self.source_url = None
        self.slug = None
        self.can_send_in_message = None
        self.class_property = None
        self.type_property = None
        self.short_url = None
        self.caption = None
        self.type_property = None
        self.liked = None
        self.display_avatar = None
        self.name = None
        self.followed = None
        self.date = None
        self.can_like = None
        self.reblog_key = None
        self.can_reblog = None
        self.format = None
        self.tags = None
        self.recommended_color = None
        self.note_count = None
        self.can_reply = None
        self.photos = None
        self.image_permalink = None
        self.liked_timestamp = None
        self.timestamp = None


class Post(object):

    def __init__(self, **kwargs):
        """
        : attribute reblog : Reblog
        : attribute summary : string
        : attribute id_property : float
        : attribute blog_name : string
        : attribute trail : array
        : attribute post_url : string
        : attribute state : string
        : attribute player : array
        : attribute can_send_in_message : bool
        : attribute slug : string
        : attribute class_property : string
        : attribute duration : float
        : attribute html5_capable : bool
        : attribute type_property : string
        : attribute short_url : string
        : attribute caption : string
        : attribute type_property : string
        : attribute liked : bool
        : attribute thumbnail_width : float
        : attribute display_avatar : bool
        : attribute name : string
        : attribute followed : bool
        : attribute date : string
        : attribute can_like : bool
        : attribute reblog_key : string
        : attribute can_reblog : bool
        : attribute format : string
        : attribute tags : array
        : attribute thumbnail_height : float
        : attribute thumbnail_url : string
        : attribute note_count : float
        : attribute video_type : string
        : attribute can_reply : bool
        : attribute video_url : string
        : attribute timestamp : float
        """
        self.reblog = None
        self.recommended_source = None
        self.summary = None
        self.id_property = None
        self.blog_name = None
        self.trail = None
        self.post_url = None
        self.state = None
        self.player = None
        self.can_send_in_message = None
        self.slug = None
        self.class_property = None
        self.duration = None
        self.html5_capable = None
        self.type_property = None
        self.short_url = None
        self.caption = None
        self.type_property = None
        self.liked = None
        self.thumbnail_width = None
        self.display_avatar = None
        self.name = None
        self.followed = None
        self.date = None
        self.can_like = None
        self.reblog_key = None
        self.can_reblog = None
        self.format = None
        self.tags = None
        self.thumbnail_height = None
        self.recommended_color = None
        self.thumbnail_url = None
        self.note_count = None
        self.video_type = None
        self.can_reply = None
        self.video_url = None
        self.timestamp = None
        for k,v in kwargs:
            try:
                if k == 'player':
                    self.__setattr__(k, Player(**v))
                elif k == 'trail':
                    self.__setattr__(k, Trail(**v))
                elif k == 'reblog':
                    self.__setattr__(k, Reblog(**v))
                else:
                    self.__setattr__(k, v)
            except:
                pass


class AltSizes(object):

    def __init__(self, **kwargs):
        """
        : attribute url : string
        : attribute width : float
        : attribute height : float
        """
        self.url = None
        self.width = None
        self.height = None


class Tumblr(object):

    def __init__(self, **kwargs):
        """
        : attribute player : Player
        : attribute post : Post
        : attribute post_type : PostType
        : attribute following : Following
        : attribute trail : Trail
        : attribute posts : Posts
        : attribute dashboard : Dashboard
        : attribute liked : Liked
        : attribute blog : Blog
        : attribute user : User
        """
        self.response = kwargs.get('response', None)
        self.meta = kwargs.get('meta', {})
        if self.response is not None:
            keys = self.response.keys()
            keys.pop('meta')
            kwargs = self.response
        #self.response = kwargs.get('response', {})
        #self.meta = kwargs.get('meta', {})
        self.following = Following(**kwargs.get("following", Following({})))
        self.posts = Posts(**kwargs.get("posts", Posts({})))
        self.dashboard = Dashboard(**kwargs.get("dashboard", Dashboard({})))
        self.liked = Liked(**kwargs.get("liked", Liked({})))
        self.blog = Blog(**kwargs.get("blog", Blog({})))
        self.user = User(**kwargs.get("user", User({})))