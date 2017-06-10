
class Liked(dict):

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
        : attribute player : array
        : attribute can_send_in_message : bool
        : attribute is_nsfw : bool
        : attribute nsfw_score : float
        : attribute duration : float
        : attribute blog : Blog
        : attribute photoset_layout : string
        : attribute html5_capable : bool
        : attribute type_property : string
        : attribute short_url : string
        : attribute caption : string
        : attribute links : Links
        : attribute liked : bool
        : attribute thumbnail_width : float
        : attribute display_avatar : bool
        : attribute can_like : bool
        : attribute followed : bool
        : attribute date : string
        : attribute reblog_key : string
        : attribute can_reblog : bool
        : attribute format : string
        : attribute tags : array
        : attribute thumbnail_height : float
        : attribute note_count : float
        : attribute thumbnail_url : string
        : attribute video_type : string
        : attribute can_reply : bool
        : attribute video_url : string
        : attribute photos : array
        : attribute image_permalink : string
        : attribute liked_timestamp : float
        : attribute post_author : string
        : attribute timestamp : float
        """
        super(Liked, self).__init__(**kwargs)
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
        self.player = None
        self.can_send_in_message = None
        self.is_nsfw = None
        self.nsfw_score = None
        self.duration = None
        self.blog = None
        self.photoset_layout = None
        self.html5_capable = None
        self.type_property = None
        self.short_url = None
        self.caption = None
        self.links = None
        self.liked = None
        self.thumbnail_width = None
        self.display_avatar = None
        self.can_like = None
        self.followed = None
        self.date = None
        self.reblog_key = None
        self.can_reblog = None
        self.format = None
        self.tags = None
        self.thumbnail_height = None
        self.recommended_color = None
        self.note_count = None
        self.thumbnail_url = None
        self.video_type = None
        self.can_reply = None
        self.video_url = None
        self.photos = None
        self.image_permalink = None
        self.liked_timestamp = None
        self.post_author = None
        self.timestamp = None
        for k,v in kwargs.iteritems():
            try:
                self.__setattr__(name=k, value=v)
            except:
                try:
                    self.__setattr__(name=str(k+"_property"), value=v)
                except:
                    pass


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
        : attribute header_image : string
        : attribute title_color : string
        : attribute body_font : string
        : attribute header_focus_height : float
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
        self.header_image = None
        self.title_color = None
        self.body_font = None
        self.header_focus_height = None
        self.show_header_image = None
        self.title_font = None
        self.header_full_width = None
        self.header_image_focused = None
        for k,v in kwargs.iteritems():
            try:
                self.__setattr__(name=k, value=v)
            except:
                pass


class NsfwSurvey(object):

    def __init__(self, **kwargs):
        """
        : attribute type_property : string
        : attribute href : string
        """
        self.type_property = None
        self.href = None
        for k,v in kwargs.iteritems():
            try:
                self.__setattr__(name=k, value=v)
            except:
                pass


class Reblog(object):

    def __init__(self, **kwargs):
        """
        : attribute comment : string
        : attribute tree_html : string
        """
        self.comment = None
        self.tree_html = None
        for k,v in kwargs.iteritems():
            try:
                self.__setattr__(name=k, value=v)
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
        for k,v in kwargs.iteritems():
            try:
                self.__setattr__(name=k, value=v)
            except:
                pass


class Links(object):

    def __init__(self, **kwargs):
        """
        : attribute nsfw_survey : NsfwSurvey
        """
        self.nsfw_survey = None
        for k,v in kwargs.iteritems():
            try:
                self.__setattr__(name=k, value=v)
            except:
                pass


class Trail(object):

    def __init__(self, **kwargs):
        """
        : attribute content_raw : string
        : attribute post : Post
        : attribute content : string
        : attribute is_root_item : bool
        : attribute blog : Blog
        : attribute is_current_item : bool
        """
        self.content_raw = None
        self.post = None
        self.content = None
        self.is_root_item = None
        self.blog = None
        self.is_current_item = None
        for k,v in kwargs.iteritems():
            try:
                self.__setattr__(name=k, value=v)
            except:
                pass


class Player(object):

    def __init__(self, **kwargs):
        """
        : attribute width : float
        : attribute embed_code : string
        """
        self.width = None
        self.embed_code = None
        for k,v in kwargs.iteritems():
            try:
                self.__setattr__(name=k, value=v)
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
        for k,v in kwargs.iteritems():
            try:
                self.__setattr__(name=k, value=v)
            except:
                pass


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
        for k,v in kwargs.iteritems():
            try:
                self.__setattr__(name=k, value=v)
            except:
                pass


class Blog(object):

    def __init__(self, **kwargs):
        """
        : attribute uuid : string
        : attribute description : string
        : attribute theme : Theme
        : attribute is_nsfw : bool
        : attribute updated : float
        : attribute is_adult : bool
        : attribute active : bool
        : attribute url : string
        : attribute can_be_followed : bool
        : attribute placement_id : string
        : attribute key : string
        : attribute title : string
        : attribute share_likes : bool
        : attribute share_following : bool
        : attribute can_message : bool
        : attribute name : string
        """
        self.uuid = None
        self.description = None
        self.theme = None
        self.is_nsfw = None
        self.updated = None
        self.is_adult = None
        self.active = None
        self.url = None
        self.can_be_followed = None
        self.placement_id = None
        self.key = None
        self.title = None
        self.share_likes = None
        self.share_following = None
        self.can_message = None
        self.name = None
        for k,v in kwargs.iteritems():
            try:
                self.__setattr__(name=k, value=v)
            except:
                pass


class Post(object):

    def __init__(self, id=None):
        """
        : attribute id_property : string
        """
        self.id_property = id

