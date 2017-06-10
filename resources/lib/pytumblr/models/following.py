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
        for k, v in kwargs.iteritems():
            try:
                self.__setattr__(name=k, value=v)
            except:
                pass


class Blogs(Theme):

    def __init__(self, **kwargs):
        """
        : attribute uuid : string
        : attribute description : string
        : attribute theme : Theme
        : attribute is_nsfw : bool
        : attribute updated : float
        : attribute is_adult : bool
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
        super(Blogs, self).__init__(**kwargs)
        self.uuid = None
        self.description = None
        self.theme = None
        self.is_nsfw = None
        self.updated = None
        self.is_adult = None
        self.url = None
        self.can_be_followed = None
        self.placement_id = None
        self.key = None
        self.title = None
        self.share_likes = None
        self.share_following = None
        self.can_message = None
        self.name = None
        for k, v in kwargs.iteritems():
            try:
                if k == 'theme':
                    self.theme = Theme(**v)
                else:
                    self.__setattr__(name=k, value=v)
            except:
                pass


class Following(dict):

    def __init__(self, **kwargs):
        """
        : attribute blogs : array
        : attribute total_blogs : float
        """
        super(Following, self).__init__(**kwargs)
        self.blogs = Blogs
        self.total_blogs = None
        for k, v in kwargs.iteritems():
            try:
                if k == 'blogs':
                    self.blogs = Blogs(**v)
                elif k == 'total_blogs':
                    self.total_blogs = int(v)
                    # if self.__getattribute__(k) is not None:
                    #    self.__setattr__(name=k, value=v)
            except:
                pass