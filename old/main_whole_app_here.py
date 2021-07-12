from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class KivyFun2(App):
    def build(self):
        self.main_window = GridLayout()
        self.main_window.cols = 1
        self.main_window.inner_window = GridLayout(row_force_default=True,
                                                   row_default_height=50,
                                                   col_force_default=True,
                                                   col_default_width=400
                                                   )
        self.main_window.inner_window.cols = 1
        self.main_window.add_widget(self.main_window.inner_window)

        self.main_window.inner_window.add_widget(Image(source="assets/ryanmeme.png"))
        self.label = Label(text="chuj")
        self.main_window.inner_window.add_widget(self.label)

        self.input_name = TextInput(multiline=False)
        self.main_window.inner_window.add_widget(self.input_name)

        self.input_country = TextInput(multiline=False)
        self.main_window.inner_window.add_widget(self.input_country)

        self.submit = Button(text='Submit', font_size=21, height=50, size_hint_y=None)
        self.submit.bind(on_press=self.submit_data)
        self.main_window.add_widget(self.submit)


        return self.main_window

    def submit_data2(self, instance):
        name = self.input_name.text
        country = self.input_country.text
        print(name)
        self.label.text += name


if __name__ == "__main__2":
    KivyFun2().run()
