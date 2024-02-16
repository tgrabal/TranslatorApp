# -*- coding: utf-8 -*-

"""
"""
from __future__ import annotations

from contextlib import suppress
from enum import Enum, auto
from typing import Optional, List


####################
# TASK - CLASSES NO 1
# Prepare implementation of Translator class

# TASK - CLASSES NO 2
# Propose solution for the following use cases:
# User is able to translate in both directions (e.g. from English to Polish and from Polish to English)
# User is able to add translation to more than one language (e.g. from Polish to English and Spanish)
####################

class TranslationNotFound(Exception):
    def __init__(self, word: str, dictionary_description: str):
        self.message = f"Translation of the word '{word}' not found in {dictionary_description}!"
        super().__init__(self.message)


class DictionaryNotFound(Exception):
    def __init__(self, dictionary_description: str, translator_description: str):
        self.message = f"{dictionary_description} not found in {translator_description}!"
        super().__init__(self.message)


class Languages(Enum):
    ENGLISH = auto()
    POLISH = auto()
    SPANISH = auto()
    GERMAN = auto()


class Dictionary:

    @staticmethod
    def get_dictionary_description(from_lang: Languages, to_lang: Languages):
        return f"{from_lang.name.capitalize()} -> {to_lang.name.capitalize()} dictionary"

    def __init__(self, from_lang: Languages, to_lang: Languages):
        self._from_lang = from_lang
        self._to_lang = to_lang
        self._translations = dict()

    @property
    def languages(self):
        return self._from_lang, self._to_lang

    def __str__(self):
        return self.get_dictionary_description(self._from_lang, self._to_lang)

    def add_translation(self, from_word: str, *args):
        with suppress(KeyError):
            self._translations[from_word].union(set(args))
            return
        self._translations[from_word] = set(args)

    def get_translation(self, word: str):
        if (translation := self._translations.get(word)) is None:
            raise TranslationNotFound(word, str(self))
        return translation


class Translator:
    def __init__(self, dictionaries: Optional[List[Dictionary]] = None):
        self._language_dictionaries = dictionaries

    def add_new_dictionary(self, new_dictionary: Dictionary):
        self._language_dictionaries.append(new_dictionary)

    def __str__(self):
        languages_str = [
            f'{language_dictionary.languages[0].name.capitalize()} -> {language_dictionary.languages[1].name.capitalize()}' for
            language_dictionary in
            self._language_dictionaries]
        return f"Translator({', '.join(languages_str)})"

    def translate_word(self, word: str, from_lang: Languages, to_lang: Languages):
        for language_dictionary in self._language_dictionaries:
            if language_dictionary.languages == (from_lang, to_lang):
                return language_dictionary.get_translation(word)
        raise DictionaryNotFound(Dictionary.get_dictionary_description(from_lang, to_lang), str(self))


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

translator = Translator(dictionaries=[d_pol_eng, d_eng_pol])
translator.add_new_dictionary(d_pol_esp)
print(translator.translate_word("kot", from_lang=Languages.POLISH, to_lang=Languages.SPANISH))
print(translator.translate_word("spring", from_lang=Languages.ENGLISH, to_lang=Languages.POLISH))
try:
    translator.translate_word("guten tag", from_lang=Languages.GERMAN, to_lang=Languages.POLISH)
except DictionaryNotFound as dictionary_not_found:
    print(dictionary_not_found.message)

try:
    translator.translate_word("pies", from_lang=Languages.POLISH, to_lang=Languages.ENGLISH)
except TranslationNotFound as translation_not_found:
    print(translation_not_found.message)
