def s(in_val, characters=20):
    global vars_names
    for text, name in vars_names:
        find_res = text.find(in_val)
        while find_res != -1:
            print("in file" + name + '\n' + text[max(0, find_res - characters):min(find_res + characters, len(text))] + '\n')
            find_res = text.find(in_val, find_res + 1)
