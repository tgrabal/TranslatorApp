from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner

from src.translator import Translator, Languages, Dictionary


# Kivy app definition
class TranslatorApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.translator = self._build_translator()

    def _build_translator(self) -> Translator:
        d_pol_eng = Dictionary(Languages.POLISH, Languages.ENGLISH)
        d_pol_eng.add_translation("kot", "cat")
        d_pol_eng.add_translation("pasta", "paste")
        d_pol_eng.add_translation("makaron", "pasta")
        d_pol_eng.add_translation("herb", "crest")
        d_pol_eng.add_translation("zioło", "herb")
        d_pol_eng.add_translation("szkło", "glass")
        d_pol_eng.add_translation("szklanka", "glass")
        d_pol_eng.add_translation("wiosna", "spring")
        d_pol_eng.add_translation("sprężyna", "spring")

        d_eng_pol = Dictionary(Languages.ENGLISH, Languages.POLISH)
        d_eng_pol.add_translation("cat", "kot")
        d_eng_pol.add_translation("spring", "wiosna", "sprężyna")

        d_pol_esp = Dictionary(Languages.POLISH, Languages.SPANISH)
        d_pol_esp.add_translation("kot", "gato")

        return Translator(dictionaries=[d_pol_eng, d_eng_pol])

    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10)

        self.word_input = TextInput(hint_text='Enter word to translate')
        layout.add_widget(self.word_input)

        self.source_lang_spinner = Spinner(text='Source Language', values=[lang.name for lang in Languages])
        layout.add_widget(self.source_lang_spinner)

        self.target_lang_spinner = Spinner(text='Target Language', values=[lang.name for lang in Languages])
        layout.add_widget(self.target_lang_spinner)

        translate_button = Button(text='Translate')
        translate_button.bind(on_press=self.translate_word)
        layout.add_widget(translate_button)

        self.translation_label = Label(text='')
        layout.add_widget(self.translation_label)

        return layout

    def translate_word(self, instance):
        word = self.word_input.text.strip()
        source_lang = Languages[self.source_lang_spinner.text]
        target_lang = Languages[self.target_lang_spinner.text]

        translation = self.translator.translate_word(word, source_lang, target_lang)
        self.translation_label.text = f'Translation: {translation}'


if __name__ == '__main__':
    TranslatorApp().run()