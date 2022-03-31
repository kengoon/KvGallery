if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from kivy.properties import NumericProperty, BoundedNumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from CustomUI import path
from kivy.lang import Builder

Builder.load_file(str(path / "card.kv"))


class MD3Card(MDCard, FakeRectangularElevationBehavior):
    pass


class Card(ButtonBehavior, MDBoxLayout):
    errorhandler = ObjectProperty(lambda x: 1 if x > 1 else 0)
    shadow_r = BoundedNumericProperty(0, min=0.0, max=1.0, errorhandler=errorhandler.defaultvalue)
    shadow_g = BoundedNumericProperty(0, min=0.0, max=1.0, errorhandler=errorhandler.defaultvalue)
    shadow_b = BoundedNumericProperty(0, min=0.0, max=1.0, errorhandler=errorhandler.defaultvalue)
    shadow_color = ReferenceListProperty(shadow_r, shadow_g, shadow_b)
    elevation = NumericProperty(0.005)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = [1, 1, 1, 1]

    def __draw_shadow__(self, origin, end, context=None):
        pass


if __name__ == "__main__":
    from kivymd.app import MDApp
    from kivy.lang import Builder
    from kivy.animation import Animation
    from random import uniform


    class Test(MDApp):
        def build(self):
            from textwrap import dedent
            return Builder.load_string(
                dedent(
                    """
                # kv_start
                #:import uniform random.uniform
                FloatLayout:
                    Card:
                        size_hint: .5, .5
                        pos_hint: {"center": [.5, .5]}
                        radius: dp(30)
                        shadow_color: 0, 1, 2
                        elevation: 0.03
                        on_release: self.shadow_color=[uniform(0, 1), uniform(0, 1), uniform(0, 1)]
                # kv_end
                """
                )
            )

        # def on_start(self):
        #     anim1 = Animation(shadow_color=[uniform(0, 1), uniform(0, 1), uniform(0, 1)], d=3)
        #     anim2 = Animation(shadow_color=[uniform(0, 1), uniform(0, 1), uniform(0, 1)], d=3)
        #     anim = anim1 + anim2
        #     anim.repeat = True
        #     anim.start(self.root.children[0])

    Test().run()
