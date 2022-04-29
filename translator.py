import requests
from bs4 import BeautifulSoup
import sys

languages = {1: 'Arabic', 2: 'German', 3: 'English', 4: 'Spanish',
             5: 'French', 6: 'Hebrew', 7: 'Japanese', 8: 'Dutch', 9: 'Polish', 10: 'Portuguese', 11: 'Romanian',
             12: 'Russian', 13: 'Turkish'}
headers = {'User-Agent': 'Mozilla/5.0'}
args = sys.argv


def soup_parser(n_language):
    url = f'https://context.reverso.net/translation/{orig_language.lower()}-{n_language.lower()}/{word}'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    if r.status_code != 200 and soup.find(id='no-results') is None:
        print('Something wrong with your internet connection')
    return soup


def translated_words_list(highlighted_words_bs4):
    t_words = []
    for w in highlighted_words_bs4[0]:
        if w.text.lower() not in t_words:
            t_words.append(w.text.lower().strip())
    t_words = [i for i in t_words if i != '']
    return t_words


def translated_ex_list(examples_bs4):
    t_examples = []
    for s in examples_bs4:
        t_examples.append(s.text.strip())
    return t_examples


def print_translated(n_language):
    soup = soup_parser(n_language)
    highlighted_words_bs4 = soup.find_all('div', {'id': 'translations-content'})
    examples_bs4 = soup.find_all(class_=('src ltr', 'trg ltr', 'trg rtl arabic', 'trg rtl'))

    t_words = translated_words_list(highlighted_words_bs4)
    t_examples = translated_ex_list(examples_bs4)

    example_print = f'\n{n_language.title()} Examples:\n'

    if new_language == 'all':
        trans_print = f'{n_language.title()} Translations:\n{t_words[0]}\n'
        example_print = f'\n{n_language.title()} Examples:\n{t_examples[0]}\n{t_examples[1]}\n\n\n'
    else:
        trans_print = f'{n_language.title()} Translations:\n' + '\n'.join(t_words[:5]) + '\n'
        example_print += ''.join([f'{t_examples[i]}\n{t_examples[i + 1]}\n\n\n' for i in range(0, 10, 2)])

    print(trans_print, end='')
    print(example_print, end='')
    txt.write(trans_print + example_print)


orig_language = args[1]
new_language = args[2]
word = args[3]

with open(f'{word}.txt', 'w', encoding='utf-8') as txt:
    if new_language == 'all':
        for language in languages.values():
            if language.lower() != orig_language:
                try:
                    print_translated(language)
                except IndexError:
                    if soup_parser(language).find(id='no-results') is not None:
                        print(f'Sorry, unable to find {word}')
                        break
                    print(f"Sorry, the program doesn't support {orig_language}")
                    break
            else:
                continue
    else:
        try:
            print_translated(new_language)
        except IndexError:
            if orig_language.title() not in languages.values():
                print(f"Sorry, the program doesn't support {orig_language}")
            elif new_language.title() not in languages.values():
                print(f"Sorry, the program doesn't support {new_language}")
            else:
                print(f'Sorry, unable to find {word}')
print()
