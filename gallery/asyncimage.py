from kivy import Logger
from kivy.resources import resource_find
from kivy.uix.image import AsyncImage, Loader


class AsyncMe(AsyncImage):
    def __init__(self, **kwargs):
        self._found_source = None
        self._coreimage = None
        global Loader
        if not Loader:
            from kivy.loader import Loader
        self.fbind('source', self._load_source)
        super().__init__(**kwargs)

    def on_load(self, *args):
        pass

    def on_source(self, x, y):
        pass

    def _on_source_load(self, value):
        image = self._coreimage.image
        if not image:
            return
        self.texture = image.texture
        self.dispatch('on_load')

    def _load_source(self, *args):
        source = self.source
        if not source:
            self._clear_core_image()
            return
        if not self.is_uri(source):
            source = resource_find(source)
            if not source:
                Logger.error('AsyncImage: Not found <%s>' % self.source)
                self._clear_core_image()
                return
        self._found_source = source
        self._coreimage = image = Loader.image(
            source,
            nocache=self.nocache,
            mipmap=self.mipmap,
            anim_delay=self.anim_delay
        )
        image.bind(
            on_load=self._on_source_load,
            on_error=self._on_source_error,
            on_texture=self._on_tex_change
        )
        self.texture = image.texture