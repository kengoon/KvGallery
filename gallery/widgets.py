from json import loads

from kivy import platform
from kivymd.uix.textfield import MDTextField

from libs.libpy.cartcheckout import DropDown


class Locator(MDTextField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with open("location.json") as file:
            self.locations = loads(file.read())
            self.locations.pop("UNIZIK Temp Site Junction Awka")
        menu_items = [{"icon": "map-marker-radius", "text": i} for i in self.locations]
        self.menu = DropDown(
            items=menu_items,
            width_mult=4,
            caller=self
        )
        self.menu.bind(on_release=self.set_item)

    def set_item(self, instance_menu, instance_menu_item):
        self.text = instance_menu_item.text
        instance_menu.dismiss()

    def on_focus(self, *args):
        if args[1]:
            self.menu.open()
        if platform == "android":
            from kvdroid import activity
            from android.runnable import run_on_ui_thread

            @run_on_ui_thread
            def fix_back_button():
                activity.onWindowFocusChanged(False)
                activity.onWindowFocusChanged(True)

            if not args[1]:
                fix_back_button()

    def insert_text(self, substring, from_undo=False):
        MDTextField.insert_text(self, None, from_undo=from_undo)
