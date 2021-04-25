from jnius import autoclass
from kivy import platform
from kivy.clock import mainthread
from kivymd.app import MDApp
from kivymd.toast.kivytoast import toast
from plyer import notification

if platform == "android":
    Build = autoclass("android.os.Build")
    VERSION = autoclass("android.os.Build$VERSION")
    Device = Build.MANUFACTURER
    version = int(VERSION.RELEASE[0])

app = MDApp.get_running_app()


@mainthread
def notify(message, background=app.theme_cls.primary_color, duration=3):
    if platform == "android" and version >= 8:
        notification.notify(message=message, toast=True, timeout=duration)
    else:
        toast(message, background=background, duration=duration)
