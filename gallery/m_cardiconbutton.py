from kivy.core.text import DEFAULT_FONT
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.card import MDCard
from kivy.uix.label import Label
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.icon_definitions import md_icons
from kivy.lang import Builder

Builder.load_string(
    """
# kv_start
<M_CardIconButton>:
    ripple_behavior: True
    radius: [dp(10)]
    size_hint: None, None
    height: self.minimum_height
    MDGridLayout:
        id: grid
        padding: dp(20)
        spacing: dp(20)
        cols: 2
        adaptive_size: True
        #col_force_default: True
        #row_force_default: True
        
# kv_end
"""
)


class M_CardIconButton(MDCard):
    icon = StringProperty("")
    icon_size = NumericProperty("15sp")
    icon_color = ListProperty([0, 0, 0, 1])
    text = StringProperty("")
    text_color = ListProperty([0, 0, 0, 1])
    text_font_style = StringProperty("Body1")
    text_font_size = NumericProperty("15sp")
    text_font_name = StringProperty(DEFAULT_FONT)
    text_markup = BooleanProperty(True)

    def __init__(self, **kwargs):
        self.icon_widget = MDIcon(theme_text_color="Custom")
        self.icon_label_widget = Label(markup=True)
        self.label = MDLabel(theme_text_color="Custom")
        super().__init__(**kwargs)
        if self.icon and self.icon in md_icons:
            self.icon_widget = MDIcon(
                theme_text_color="Custom",
                text_color=self.icon_color,
                icon=self.icon, font_size=self.icon_size
            )
            self.ids.grid.add_widget(self.icon_widget, index=1)
        elif self.icon:
            self.icon_label_widget = Label(
                markup=True, text=self.icon,
                color=self.icon_color
            )
            self.ids.grid.add_widget(self.icon_label_widget, index=1)

        if self.text:
            self.label = MDLabel(
                text=self.text,
                markup=self.text_markup,
                theme_text_color="Custom",
                text_color=self.text_color,
                font_name=self.text_font_name,
                font_size=self.text_font_size,
                font_style=self.text_font_style,
                halign="center", size_hint=(None, None),
                valign="center"
            )
            #self.label.text_size = self.label.size
            self.label.height = "200dp"
            self.label.width = "200dp"
            self.ids.grid.add_widget(self.label)

    def on_icon(self, instance, value):
        if value in md_icons:
            self.icon_widget.icon = value
            try:
                self.add_widget(self.icon_widget, index=1)
            except AttributeError:
                self.children.clear()
        else:
            self.icon_label_widget.text = value
            try:
                self.ids.grid.add_widget(self.icon_label_widget, index=1)
            except AttributeError:
                self.children.clear()

    def on_text(self, instance, value):
        self.label.text = value
        try:
            self.add_widget(self.label)
        except AttributeError:
            self.children.clear()

    def on_icon_color(self, instance, value):
        self.icon_widget.text_color = value

    def on_icon_size(self, instance, value):
        self.icon_widget.font_size = value

    def on_text_color(self, instance, value):
        self.label.text_color = value

    def on_font_name(self, instance, value):
        self.label.font_name = value

    def on_font_style(self, instance, value):
        self.label.font_style = value

    def on_font_size(self, instance, value):
        self.label.font_size = value

    def on_text_markup(self, instance, value):
        self.label.markup = value


if __name__ == "__main__":
    from kivymd.app import MDApp


    class TestApp(MDApp):
        def build(self):
            return Builder.load_string(
                """
# kv_start
M_CardIconButton:
    icon: "android"
    text: "hello"
    pos_hint: {"center_x": .5, "center_y": .5}
# kv_end
            """
            )


    TestApp().run()
