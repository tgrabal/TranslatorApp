# -*- coding: utf-8 -*-

"""
"""
from __future__ import annotations

from contextlib import suppress
from enum import Enum, auto
from typing import Optional, List
import json
import os


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
    """
    Class representing languages using enum module.
    These are not mutable = once defined, these won't be changed.
    """
    ENGLISH = auto()
    POLISH = auto()
    SPANISH = auto()
    GERMAN = auto()
    ITALIAN = auto()
    FRENCH = auto()


class Dictionary:
    """
    Class representing a dictionary from one language to another.
    Each Dictionary is initialized with private attributes.
    Use setters & getters to interact with them instead of accessing them directly.
    Each Dictionary comes with an empty dictionary of translations.
    Use the appropriate method to add new translations to this dictionary.
    """

    @staticmethod
    def get_dictionary_description(from_lang: Languages, to_lang: Languages):
        """
        Method to return description of the Dictionary = the languages pair
        It's a @staticmethod as it can't change object instance state nor class state,
        this functionality is related to the class, but it doesn't need to access nor modify the class or its instances.
        """

        return f"{from_lang.name.capitalize()} -> {to_lang.name.capitalize()} dictionary"

    def __init__(self, from_lang: Languages, to_lang: Languages):
        self._from_lang = from_lang
        self._to_lang = to_lang
        self._translations = {}

    @property
    def languages(self):
        """
        Method to get the languages pair of this Dictionary.
        This is a 'getter' method and a property of each dictionary initialized from this class.
        """
        return self._from_lang, self._to_lang

    @property
    def all_translations(self):
        return self._translations

    def __str__(self):
        return self.get_dictionary_description(self._from_lang, self._to_lang)

    def import_translations(self, filename: str):
        """
        The file must be of .JSON format.
        The .JSON format doesn't support sets - translations must be arrays, e.g.:
        "zamek": ["castle", "lock"],
        "pies": ["dog"]
        """
        self._filename = filename

        try:
            with open(self._filename, 'r') as file:
                data = json.load(file)
            # Convert lists to sets and add imported translations to existing ones
            for key in data:
                data[key] = set(data[key])
                self._translations[key] = data[key]
        except FileNotFoundError:
            print(f"Error: The file '{self._filename}' was not found.")
        except json.JSONDecodeError:
            print(f"Error: The file '{self._filename}' contains invalid JSON.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def export_translations(self, file_name):
        """
        Export translations to a JSON file
        """
        self._filename = file_name
        # Construct the file path by joining the current working directory with the file name
        self._file_path = os.path.join(os.getcwd(), self._filename)

        # Translations must be in a list format, as JSON won't accept a set of values
        for word in self._translations:
            self._translations[word] = list(self._translations[word])

        with open(self._file_path, 'w') as self._filename:
            json.dump(self._translations, self._filename, indent=4)

    def add_translation(self, from_word: str, *args):
        """
        Takes from_word argument of type string and any number of additional arguments.
        There's no type hint for additional arguments but those should be strings.
        It uses a 'suppress' context manager. If KeyError is raised within the code below it,
        it's caught and ignored. It handles cases where 'from_word' doesn't exist in '_translations' dictionary.
        If KeyError is raised, the next line of code after the 'with' statement is executed,
        i.e., create a new dictionary.
        If KeyError is not raised because the 'from_word' exists, use update() to add args to the set of values
        without duplicating them and the return statement exits the method.
        """

        with suppress(KeyError):
            self._translations[from_word].update(args)
            return
        self._translations[from_word] = set(args)

    def get_translation(self, word: str):
        """
        The walrus operator introduced in Python 3.8, assigns a value to a variable as part of an expression,
        allowing you to both perform an action and check its result in the same line.
        Try to get values from 'word' from the dictionary and assign it to the 'translation' variable.
        Get() returns None if it can't find the values;
        check if 'translation' is None and raise exception if that's the case
        """

        if (translation := self._translations.get(word)) is None:
            raise TranslationNotFound(word, str(self))
        return translation


class Translator:
    def __init__(self, dictionaries: Optional[List[Dictionary]] = None):
        """
        The constructor has a parameter with a default value of None.
        This parameter is expected to be of type None or a list of Dictionary objects.
        """

        self._language_dictionaries = dictionaries

    def add_new_dictionary(self, new_dictionary: Dictionary):
        if self._language_dictionaries is None:
            self._language_dictionaries = []
        self._language_dictionaries.append(new_dictionary)

    def __str__(self):
        """
        List comprehension to return string representation of all dictionaries in the Translator object
        """

        if self._language_dictionaries is not None:
            languages_str = [
                f'{language_dictionary.languages[0].name.capitalize()} -> ' \
                f'{language_dictionary.languages[1].name.capitalize()}'
                for language_dictionary in self._language_dictionaries]
            return f"Translator({', '.join(languages_str)})"
        else:
            return "An empty Translator!"

    def translate_word(self, word: str, from_lang: Languages, to_lang: Languages):
        """
        Go through all dictionaries within the Translator object and look for a dictionary that has these 2 languages
        pair in the exact order as needed - from_lang, to_lang.
        Once the dictionary is found, translate the word; if the dictionary isn't found - raise the exception.
        """

        if self._language_dictionaries is not None:
            for language_dictionary in self._language_dictionaries:
                if language_dictionary.languages == (from_lang, to_lang):
                    return language_dictionary.get_translation(word)
        raise DictionaryNotFound(Dictionary.get_dictionary_description(from_lang, to_lang), str(self))

    def detect_language_translate_word(self, word: str):
        """
        Take a word, go through all available dictionaries and return found translations.
        """

        self._translations_list = []
        if self._language_dictionaries is not None:
            for dictionary in self._language_dictionaries:
                translation = dictionary.all_translations.get(word)
                if translation is not None:
                    self._translations_list.append(translation)
        return (self._translations_list)


# d_pol_eng = Dictionary(Languages.POLISH, Languages.ENGLISH)
# d_pol_eng.add_translation("kot", "cat")
# d_pol_eng.add_translation("pasta", "paste")
# d_pol_eng.add_translation("makaron", "pasta")
# d_pol_eng.add_translation("herb", "crest")
# d_pol_eng.add_translation("zioło", "herb")
# d_pol_eng.add_translation("szkło", "glass")
# d_pol_eng.add_translation("szklanka", "glass")
# d_pol_eng.add_translation("wiosna", "spring")
# d_pol_eng.add_translation("sprężyna", "spring")
#
# d_eng_pol = Dictionary(Languages.ENGLISH, Languages.POLISH)
# d_eng_pol.add_translation("cat", "kot")
# d_eng_pol.add_translation("spring", "wiosna", "sprężyna")
#
# d_pol_esp = Dictionary(Languages.POLISH, Languages.SPANISH)
# d_pol_esp.add_translation("kot", "gato")
#
# translator = Translator(dictionaries=[d_pol_eng, d_eng_pol])
# translator.add_new_dictionary(d_pol_esp)
# print(translator.translate_word("kot", from_lang=Languages.POLISH, to_lang=Languages.SPANISH))
# print(translator.translate_word("spring", from_lang=Languages.ENGLISH, to_lang=Languages.POLISH))
# try:
#     translator.translate_word("guten tag", from_lang=Languages.GERMAN, to_lang=Languages.POLISH)
# except DictionaryNotFound as dictionary_not_found:
#     print(dictionary_not_found.message)
#
# try:
#     translator.translate_word("pies", from_lang=Languages.POLISH, to_lang=Languages.ENGLISH)
# except TranslationNotFound as translation_not_found:
#     print(translation_not_found.message)
