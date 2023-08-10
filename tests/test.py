import os

from main import text_to_code, text_to_part_of_files, insert_data_in_searcher
import inser_data_in_searcher_test_samples.in_vals.names
from searcher import s, vars_names

vars_names = []

class TestClass:
    bob = """
    bib
    """

    test1 = """
    test
    test
    test
    """

    test2 = """
    bib'bob''
    """

    vars_names = [(bob, "bob"), (test1, "test1"), (test2, "test2")]

    def s(in_val, characters=20):
        global vars_names
        for text, name in vars_names:
            find_res = text.find(in_val)
            while find_res != -1:
                print(f"in file {name}" + '\n' + text[max(0, find_res - characters):min(find_res + characters,
                                                                                        len(text))] + '\n')
                find_res = text.find(in_val, find_res + 1)



    def test_text_to_code(self):
        in_vals = []
        out_vals = []
        for name in os.listdir("text_to_code_test_samples/in"):
            with open(f"text_to_code_test_samples/in/{name}", "r", encoding='utf-8') as file:
                in_vals.append((file.read(), name.split('.')[0]))
            with open(f"text_to_code_test_samples/out/{name.split('.')[0] + '.py'}", "r", encoding='utf-8') as file:
                out_vals.append(file.read())

        for in_val, out_val in zip(in_vals, out_vals):
            assert text_to_code(*in_val) == out_val

    def test_text_to_templates(self):
        in_vals = []
        out_vals = []
        for name in os.listdir("text_to_templates_test_samples/in"):
            with open(f"text_to_templates_test_samples/in/{name}", "r", encoding='utf-8') as file:
                in_vals.append((file.read(), name.split('.')[0]))
            with open(f"text_to_templates_test_samples/out/{name}", "r", encoding='utf-8') as file:
                out_vals.append(file.read())

        for in_val, out_val in zip(in_vals, out_vals):
            assert '\n\n'.join(text_to_part_of_files(*in_val)) == out_val

    def test_inser_data_in_searcher(self):
        in_vals = []
        out_vals = []
        for name in os.listdir("inser_data_in_searcher_test_samples/in_vals"):
            if name == "names.py" or name == "__pycache__":
                continue
            else:
                with open(f"inser_data_in_searcher_test_samples/in_vals/{name}", "r", encoding='utf-8') as file:
                    in_vals.append((file.read(), inser_data_in_searcher_test_samples.in_vals.names.names[name]))
                with open(f"inser_data_in_searcher_test_samples/out/{name}", "r", encoding='utf-8') as file:
                    out_vals.append(file.read())

        for in_val, out_val in zip(in_vals, out_vals):
            assert insert_data_in_searcher(*in_val) == out_val
