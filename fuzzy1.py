import json
from fuzzywuzzy import fuzz

def read_data(metadata_json):  # directory to file
    """Opens a JSON-file, reads it line by line
    to create a list of all the elements in the
    file."""

    data = []
    with open(metadata_json) as f:
        for line in f:
            data.append(json.loads(line))
    f.close()

    return data

def search_titles(data):
    """Takes the output of read_data() and returns
    a dictionary of {titles: workids}"""

    book_and_version = {}
    for book in data:
        for version in book["versions"]:
            book_and_version[version["booktitle"]] = book["workID"]

    return(book_and_version)

def fuzzy_match(dictionary, metadata_json, ratio):
    """""Takes a dict of postids and tagged sentences and
    returns the postids, found titles and workids"""

    choices = list(metadata_json.keys())

    for item in choices:
        if item == '':
            choices.remove(item)

    for postid, post in dictionary.items():
        if type(post) == list:
            plist = []
            for sentence in post:
                slist = []
                for word in sentence:
                    newword = word[0]
                    slist.append(newword)
                sstring = " ".join(slist)
                plist.append(sstring)
            text = " ".join(plist)
            print(text)

            for title in choices:
                result = fuzz.token_set_ratio(title, text)
                if result > ratio:
                    print(postid, title, result)

        elif type(post) == str:
            text = post
            print(text)

            for title in choices:
                result = fuzz.token_set_ratio(title, text)
                if result > ratio:
                    print(postid, title, result)