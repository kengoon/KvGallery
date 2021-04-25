from kivy.event import EventDispatcher
from kivy.metrics import dp
from kivy.properties import ListProperty, StringProperty
from kivymd.uix.card import MDCard
from kivy.lang import Builder

__all__ = "M_CardLoader"

Builder.load_string(
    """
# kv_start
<M_CardLoader>:
    md_bg_color: 0, 0, 0, 0
    radius: [dp(10), ]
    ripple_behavior: True
    RelativeLayout:
        AsyncImage:
            id: image
            color: 0,0,0,0
            source: root.source
            anim_delay: .1
            allow_stretch: True
            keep_ratio: False
            nocache: True
            on_load:
                root.dispatch("on_load")
            canvas.before:
                StencilPush
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: root.radius
                StencilUse

            canvas.after:
                StencilUnUse
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: root.radius
                StencilPop
            
        M_AKImageLoader:
            id: loader
            radius: root.radius
            circle: False
        MDBoxLayout:
            id:box
            opacity: 0
            padding: dp(10)
            adaptive_height: True
            md_bg_color: 0, 0, 0, .6
            radius: [0, 0, root.radius[0], root.radius[0]]
            M_AKLabelLoader:
                text: root.text
                radius: root.text_radius
                size_hint_y: None
                theme_text_color: "Custom"
                text_color: root.text_color
                height: dp(20) if not self.text else self.texture_size[1]
                font_style: "Money"
                font_size: dp(16)
                halign:"center"
# kv_end
"""
)


class M_CardLoader(MDCard):
    text = StringProperty("")
    text_radius = ListProperty([dp(5), ])
    text_color = ListProperty([1, 1, 1, 1])
    source = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type("on_load")

    def on_load(self):
        self.ids.loader.opacity = 0
        self.ids.image.color = [1, 1, 1, 1]

    def on_touch_down(self, touch):
        self.root.pause_clock()

    def on_touch_up(self, touch):
        timer = touch.time_end - touch.time_start
        if timer < 0.2:
            self.root.ids.raw.switch_tab("feeds")
        self.root.resume_clock()

    def on_release(self):
        self.root.ids.feeds.dispatch("on_tab_release")
