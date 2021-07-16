from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file('kivyfun.kv')


class MyWidget(Widget):
    name = ObjectProperty(None)
    country = ObjectProperty(None)
    fav_color = ObjectProperty(None)

    def press_submit(self):
        name = self.name.text
        country = self.country.text
        fav_color = self.fav_color.text
        print(f'Your name is {name}, your country is {country} and your fav color is {fav_color}')
        self.name.text = ""
        self.country.text = ""
        self.fav_color.text = ""


class Main(App):
    def build(self):
        return MyWidget()


if __name__ == "__main__":
    Main().run()
