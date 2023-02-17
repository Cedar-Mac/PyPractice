import sys
import argparse
import requests
from bs4 import BeautifulSoup
import re

parser = argparse.ArgumentParser(description='A multilingual translator for single words and phrases.\
                                             Supported langauges include: Arabic, German, English, Spanish, French, \
                                             Hebrew, Japanese, Dutch, Polish, Portuguese, Romanian, Russian, Turkish')

parser.add_argument('language_1', help='Enter language name in all lowercase.')
parser.add_argument('language_2', help='Enter language name in all lowercase.')
parser.add_argument('word', help='Enter the word or phrase, make sure there are no typos. \
                                  If you want to translate to all supported languages enter "all"')
args = parser.parse_args()

supported_languages = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese', 'dutch', 'polish',
                       'portuguese', 'romanian', 'russian', 'turkish', 'all']


def get_language():
        starting_language = args.language_1.lower()
        desired_language = args.language_2.lower()
        if starting_language not in supported_languages:
            print(f"Sorry, the program doesn't support {starting_language}")
            quit()
        elif desired_language not in supported_languages:
            print(f"Sorry, the program doesn't support {desired_language}")
            quit()
        else:
            supported_languages.pop(supported_languages.index(starting_language)) # Remove starting lang from list of all langs
            return [starting_language, desired_language]


def get_web_page(start_lang, tran_lang, wd):
    url = f'https://context.reverso.net/translation/{start_lang}-{tran_lang}/{wd}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    if r.ok:
        bs = BeautifulSoup(r.text, 'html.parser')
        return bs
    else:
        print(r.status_code)
        print('Something wrong with your internet connection')


def get_word_translations(sp, lang):
    word_translations_mess = sp.find_all('a', attrs={"data-term": True})
    if len(word_translations_mess) > 0:
        word_translations = [wrd.text.strip('\n') for wrd in word_translations_mess]
        translation = f'\n{lang} Translations:\n'
        for wrd in word_translations[:1]:
            translation += f'{wrd}\n'
        return translation
    else:
        print(f'Sorry, unable to find {word}')


def get_sentence_translations(sp, lang):
    translated_sentences_mess = sp.find_all(class_=re.compile("^trg"))  # regex finds all classes that start with trg
    if len(translated_sentences_mess) > 0:
        translated_sentences = [sentence.text.strip() for sentence in translated_sentences_mess]
        original_sentences_mess = sp.find_all(class_=re.compile("^src"))
        original_sentences = [sentence.text.strip() for sentence in original_sentences_mess]
        sentences = zip(original_sentences, translated_sentences)
        examples = f'{lang} Examples:\n'
        for sentence in list(sentences)[:1]:
            examples += f'{sentence[0]}\n{sentence[1]}\n'
        return examples
    else:
        return None


def translate_one_language():
    soup = get_web_page(translation_direction[0], translation_direction[1], word)
    if soup == None:
        print(f'Sorry, unable to find {word}')
    else:
        translation = get_word_translations(soup, translation_direction[1])
        translation += '\n' + get_sentence_translations(soup, translation_direction[1])
        print(translation)
        with open(f'{word}.txt', 'w', encoding='utf-8') as file:
            file.write(translation)


def translate_all_languages():
    supported_languages.pop(12)  # remove all from list of languages
    translation = ""
    for i in supported_languages:
        soup = get_web_page(translation_direction[0], i, word)
        if soup == None:
            print(f'Sorry, unable to find {word}')
            break
        else:
            translation += get_word_translations(soup, i)
            translation += '\n' + get_sentence_translations(soup, i)
    print(translation)
    with open(f'{word}.txt', 'w', encoding='utf-8') as file:
        file.write(translation)


translation_direction = get_language()
word = args.word

if translation_direction[1] == 'all':
    translate_all_languages()
else:
    translate_one_language()
