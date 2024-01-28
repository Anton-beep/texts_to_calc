import os
import re
from typing import *

import templates

MAKE_WITH_SEARCHER = False


def prepare_text(text: str) -> str:
    """here will be all text preparation"""

    text = text.replace("ü", "u#").replace("ö", "o#").replace("ä", "a#").replace("ß", "s#").replace("Ü", "U#").replace(
        "Ö", "O#").replace("Ä", "A#")

    LIMIT_SYMBOLS_LINE = 28
    words = text.split(' ')
    lines = []

    for word in words:
        if len(lines) == 0:
            lines.append(word)
        elif '\n' in word:
            lines_words = word.split('\n')
            if len(lines_words[0]) + len(lines[-1]) + 1 <= LIMIT_SYMBOLS_LINE:
                lines[-1] += ' ' + lines_words[0]
            else:
                lines.append(lines_words[0])

            for el in lines_words[1:]:
                lines.append(el)
        elif len(lines[-1]) + len(word) + 1 <= LIMIT_SYMBOLS_LINE:
            lines[-1] += ' ' + word
        else:
            lines.append(word)
    return '\n'.join(lines)


def text_to_code(text: str, name: str) -> str:
    text = text.replace('"', '\"').replace("'", "\'")
    return f'{name} = """\n{text}\n"""'


def text_to_part_of_files(text: str, name: str) -> (str, str, str):
    return (templates.script_template_cpp_1part % (name, name, text)) + '\n\n' + (
            templates.script_template_cpp_2part % (
        name, name)), templates.script_store_cpp % name, templates.script_template_h % name


def insert_data_in_searcher(names: list) -> str:
    with open("searcher.py", "r", encoding='utf-8') as file:
        text = file.read()

    # list of vars

    text = 'vars_names = ' + list(
        names).__repr__().replace('\'', '') + '\n\n' + text

    # imports

    text = '\n'.join([f"from {el} import *" for el in names]) + '\n\n' + text

    return text

def main():
    script_template_cpp = []
    script_store_cpp = []
    script_template_h = []
    python_vars = []
    names = []
    for name in os.listdir("texts"):
        with open("texts/" + name, "r", encoding='utf-8') as file:
            text = prepare_text(file.read())
        name = name.split('.')[0].replace('(', '').replace(')', '')
        name = ''.join([el[0].upper() + el[1:] for el in re.split('[ _]', name)])

        if MAKE_WITH_SEARCHER:
            text = name + f' = """{name}\n' + text + '\n"""'

        v1, v2, v3 = text_to_part_of_files(text, name)

        script_template_cpp.append(v1)
        script_store_cpp.append(v2)
        script_template_h.append(v3)

        code = text_to_code(text, name)

        python_vars.append(code)
        names.append(name)

    if MAKE_WITH_SEARCHER:
        searcher_code = insert_data_in_searcher(names)

        v1, v2, v3 = text_to_part_of_files(searcher_code, "searcher")
        script_template_cpp.insert(0, v1)
        script_store_cpp.insert(0, v2)
        script_template_h.insert(0, v3)

    with open("output.txt", "w", encoding='utf-8') as file:
        file.write('all files are stored in apps/code/\n\n')
        file.write('script_template.cpp:\n\n')
        file.write('\n\n'.join(script_template_cpp) + '\n')
        file.write('-' * 30)
        file.write('\n\nscript_store.cpp:\n\n')
        file.write('\n\n'.join(script_store_cpp) + '\n')
        file.write('-' * 30)
        file.write('\n\nscript_template.h:\n\n')
        file.write('\n\n'.join(script_template_h) + '\n')
        file.write('-' * 30)


if __name__ == '__main__':
    main()
