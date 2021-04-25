from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import BooleanProperty, NumericProperty, ListProperty
from kivy.uix.image import AsyncImage
from kivymd.material_resources import dp
from kivymd.theming import ThemableBehavior
from kivymd.uix.label import MDLabel

__all__ = ("M_AKLabelLoader", "M_AKImageLoader")

Builder.load_string(
    """
# kv_start
<M_AKLabelLoader>:
    canvas.before:
        Color:
            rgba: root.theme_cls.bg_darkest
            a: root.fr_rec_opacity
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: root.radius
        Color:
            rgba: root.theme_cls.bg_dark
            a: root.bg_rec_opacity
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: root.radius


<M_AKImageLoader>:
    source: ' '
    canvas.before:
        Color:
            rgba: root.theme_cls.bg_darkest
            a: root.fr_rec_opacity
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [(self.size[0]/2),] if root.circle else root.radius
        Color:
            rgba: root.theme_cls.bg_dark
            a: root.bg_rec_opacity
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [(self.size[0]/2,self.size[1]/2),] if root.circle else root.radius
# kv_end
"""
)


class M_AKLabelLoader(MDLabel):

    bg_rec_opacity = NumericProperty(0)
    fr_rec_opacity = NumericProperty(0)
    radius = ListProperty([dp(10), ])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_anim = None
        Clock.schedule_once(lambda x: self._update(self.text))

    def _update(self, text):
        if self._check_text(text):
            self._stop_animate()
        else:
            self._start_animate()

    @staticmethod
    def _check_text(text):
        return bool(text)

    def _start_animate(self):
        self.bg_rec_opacity = 1
        self.fr_rec_opacity = 1
        self.start_anim = Animation(
            bg_rec_opacity=1, t="in_quad", duration=0.8
        ) + Animation(bg_rec_opacity=0, t="out_quad", duration=0.8)
        self.start_anim.repeat = True
        self.start_anim.start(self)

    def _stop_animate(self):

        if self.start_anim:
            self.start_anim.cancel_all(self)

        if self.bg_rec_opacity != 0 and self.fr_rec_opacity != 0:
            self.stop_anim = Animation(
                fr_rec_opacity=0, t="out_quad", duration=0.8
            )
            self.stop_anim &= Animation(
                bg_rec_opacity=0, t="out_quad", duration=0.8
            )
            self.stop_anim.start(self)

    def on_text(self, *args):
        if self._check_text(self.text):
            self._stop_animate()
        else:
            self._start_animate()


class M_AKImageLoader(ThemableBehavior, AsyncImage):

    bg_rec_opacity = NumericProperty(0)
    fr_rec_opacity = NumericProperty(0)
    circle = BooleanProperty(True)
    radius = ListProperty([dp(10), ])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_anim = None

    def _check_source(self, source):
        if source and len(source.strip()) != 0:
            return True
        self.source = ""
        return False

    def _start_animate(self):
        self.bg_rec_opacity = 1
        self.fr_rec_opacity = 1
        self.color = [1, 1, 1, 0]
        self.start_anim = Animation(
            bg_rec_opacity=1, t="in_quad", duration=0.8
        ) + Animation(bg_rec_opacity=0, t="out_quad", duration=0.8)
        self.start_anim.repeat = True
        self.start_anim.start(self)

    def _stop_animate(self):

        self.color = [1, 1, 1, 1]
        if self.start_anim:
            self.start_anim.cancel_all(self)
            self.stop_anim = Animation(
                fr_rec_opacity=0, t="out_quad", duration=0.8
            )
            self.stop_anim &= Animation(
                bg_rec_opacity=0, t="out_quad", duration=0.8
            )
            self.stop_anim.start(self)

    def on_source(self, *args):
        if self._check_source(self.source):
            self._stop_animate()
        else:
            self._start_animate()
