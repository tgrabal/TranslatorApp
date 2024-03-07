import unittest
from translator import Languages, Dictionary, Translator, DictionaryNotFound, TranslationNotFound

class TestDictionary(unittest.TestCase):

    def setUp(self) -> None:
        """
        This method will run its code before every single test.

        Create a few dictionaries (object instances) to be used in tests.
        """
        self.d_pol_eng = Dictionary(Languages.POLISH, Languages.ENGLISH)
        self.d_pol_ita = Dictionary(Languages.POLISH, Languages.ITALIAN)
        self.d_eng_ita = Dictionary(Languages.ENGLISH, Languages.ITALIAN)

    def test_get_dictionary_description(self):

        # REDUNDANT tests as logic could be tested just once???
        self.assertEqual(self.d_pol_eng.__str__(), "Polish -> English dictionary")
        self.assertEqual(self.d_pol_ita.__str__(), "Polish -> Italian dictionary")
        self.assertEqual(self.d_eng_ita.__str__(), "English -> Italian dictionary")

    def test_languages(self):

        # REDUNDANT tests as logic could be tested just once???
        self.assertEqual(self.d_pol_eng.languages, (Languages.POLISH, Languages.ENGLISH))
        self.assertEqual(self.d_pol_ita.languages, (Languages.POLISH, Languages.ITALIAN))
        self.assertEqual(self.d_eng_ita.languages, (Languages.ENGLISH, Languages.ITALIAN))

    def test_add_translation(self):

        # 1st TC
        self.d_pol_eng.add_translation("zamek", "castle")
        self.d_pol_eng.add_translation("zamek", "castle", "lock")
        self.d_pol_eng.add_translation("zamek", "lock")
        self.d_pol_ita.add_translation("chlopiec", "ragazzo")

        # Since _translations are a private field, testing through the public interface get_translation()
        # From Python 3.7, dict type maintains insertion order.
        self.assertEqual(self.d_pol_eng.get_translation("zamek"), {'castle', 'lock'})

        self.assertEqual(self.d_pol_ita.get_translation("chlopiec"), {"ragazzo"})

    def test_get_translation(self):

        # 1st TC - redundant as this method was tested above?
        self.d_pol_eng.add_translation("zima", "winter")
        self.d_pol_ita.add_translation("mleko", "latte")
        self.d_eng_ita.add_translation("girl", "ragazza")

        # REDUNDANT tests as logic could be tested just once???
        self.assertEqual(self.d_pol_eng.get_translation("zima"), {'winter'})
        self.assertEqual(self.d_pol_ita.get_translation("mleko"), {"latte"})
        self.assertEqual(self.d_eng_ita.get_translation("girl"), {"ragazza"})

        # 2nd TC - translation not found
        # Logic could be tested just once???
        with self.assertRaises(TranslationNotFound):
            self.d_pol_eng.get_translation("lato")
        with self.assertRaises(TranslationNotFound):
            self.d_pol_ita.get_translation("jesien")
        with self.assertRaises(TranslationNotFound):
            self.d_eng_ita.get_translation("summer")

    def test_import_translations(self):

        # 1st TC - import an existing file and get its translations
        self.filename = "pol_eng.json"
        self.assertEqual(self.d_pol_eng.import_translations(self.filename), None)
        self.assertEqual(self.d_pol_eng.get_translation("kobieta"), {"female", "woman"})

        # 2nd TC - try importing a file that doesn't exist
        self.filename2 = "pol_eng2.json"
        with self.assertRaises(FileNotFoundError):
            self.d_pol_eng.import_translations(self.filename2)

    def test_export_translations(self):

        # Test by exporting some translations which then will be imported to a new dictionary;
        # finally test translations themselves
        self.d_pol_eng.add_translation("slon", "elephant")
        self.d_pol_eng.add_translation("kon", "horse")
        self.d_pol_eng.add_translation("auto", "car", "auto")
        self.d_pol_eng.export_translations("pol_eng_test_file.json")

        self.new_dict = Dictionary(Languages.POLISH, Languages.ENGLISH)
        self.new_dict.import_translations("pol_eng_test_file.json")
        self.assertEqual(self.new_dict.get_translation("slon"), {"elephant"})
        self.assertEqual(self.new_dict.get_translation("auto"), {"car", "auto"})


class TestTranslator(unittest.TestCase):

    def setUp(self) -> None:
        """
        This method will run its code before every single test.

        Create a few dictionaries and translators to be used in tests.
        """
        self.d_pol_eng = Dictionary(Languages.POLISH, Languages.ENGLISH)
        self.d_eng_pol = Dictionary(Languages.ENGLISH, Languages.POLISH)
        self.d_eng_ita = Dictionary(Languages.ENGLISH, Languages.ITALIAN)

        self.empty_translator = Translator()
        self.one_dict_translator = Translator([self.d_pol_eng])
        self.two_dict_translator = Translator([self.d_pol_eng, self.d_eng_pol])

    def test__str__(self):

        # 1st TC - a translator without dictionaries
        self.assertEqual(self.empty_translator.__str__(), "An empty Translator!")

        # 2nd TC - a translator with 1 dictionary
        self.assertEqual(self.one_dict_translator.__str__(), "Translator(Polish -> English)")

        # 3rd TC - a translator with two dictionaries
        self.assertEqual(self.two_dict_translator.__str__(), "Translator(Polish -> English, English -> Polish)")

    def test_add_new_dictionary(self):

        # 1st TC - adding a dictionary to an empty translator
        self.empty_translator.add_new_dictionary(self.d_pol_eng)
        self.assertEqual(self.empty_translator.__str__(), "Translator(Polish -> English)")

        # 2nd TC - adding a dictionary to a translator that already has 2 dictionaries
        self.two_dict_translator.add_new_dictionary(self.d_eng_ita)
        self.assertEqual(self.two_dict_translator.__str__(), "Translator(Polish -> English, English -> Polish, "
                                                             "English -> Italian)")

    def test_translate_word(self):

        # 1st TC - translate a word with a single translation
        self.d_pol_eng.add_translation("kot", "cat")
        self.assertEqual(self.one_dict_translator.translate_word("kot", Languages.POLISH, Languages.ENGLISH), {"cat"})

        # 2nd TC - translate a word with more than 1 translation
        self.d_pol_eng.add_translation("zamek", "castle", "lock")
        self.assertEqual(self.one_dict_translator.translate_word("zamek", Languages.POLISH, Languages.ENGLISH),
                         {"castle", "lock"})

        # 3rd ranslate a word that has more than 1 translation using a translator that contains multiple dictionaries
        self.d_eng_pol.add_translation("spring", "wiosna", "sprezyna")
        self.assertEqual(self.two_dict_translator.translate_word("spring", Languages.ENGLISH, Languages.POLISH),
                         {"wiosna", "sprezyna"})

        # 4th TC - try to translate a word using a dictionary that doesn't exist in that translator
        with self.assertRaises(DictionaryNotFound):
            self.empty_translator.translate_word("pies", Languages.POLISH, Languages.ENGLISH)
        with self.assertRaises(DictionaryNotFound):
            self.one_dict_translator.translate_word("kot", Languages.POLISH, Languages.FRENCH)

        # 5th TC - try to translate a word that doesn't exist in the specified dictionary
        with self.assertRaises(TranslationNotFound):
            self.assertEqual(self.one_dict_translator.translate_word("orangutan", Languages.POLISH, Languages.ENGLISH))

    def test_detect_language_translate_word(self):

        # 1st TC - translate a word that exists only in 1 dictionary
        self.d_pol_eng.add_translation("pies", "dog")
        self.assertEqual(self.one_dict_translator.detect_language_translate_word("pies"), [{"dog"}])

        # 2nd TC - translate a word that exists in multiple dictionaries
        self.d_pol_eng.add_translation("zamek", "castle")
        self.d_pol_eng.add_translation("zamek", "lock")
        self.d_pol_ita = Dictionary(Languages.POLISH, Languages.ITALIAN)
        self.d_pol_ita.add_translation("zamek", "serratura")
        self.multiple_dict_translator = Translator([self.d_pol_eng, self.d_pol_ita])
        self.assertEqual(self.multiple_dict_translator.detect_language_translate_word("zamek"),
                         [{"castle", "lock"}, {"serratura"}])

        # 3rd TC - try to get translations from an empty translator
        self.assertEqual(self.empty_translator.detect_language_translate_word("zyrafa"), [])


if __name__ == "__main__":
    unittest.main()

