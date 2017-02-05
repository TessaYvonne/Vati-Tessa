from get_text_from_xml_new import get_text_from_xml
from nltk import sent_tokenize
from nltk import word_tokenize
import os
import re
import fuzzy1
from fuzzywuzzy import fuzz

def find_title(folder, metadata_json, ratio):

    outfile = open("output.txt", "w")
    data = fuzzy1.read_data(metadata_json)
    book_and_version = fuzzy1.search_titles(data)
    choices = list(book_and_version.keys())

    for item in choices:
        if item == '':
            choices.remove(item)

    for filename in os.listdir(folder):
        threadidxml = filename.lstrip("thread.")
        threadid = threadidxml.rstrip(".xml")
        file = folder + "/" + filename
        postdict = get_text_from_xml(file)

        for postid, post in postdict.items():
            print(postid)
            sents = sent_tokenize(post)
            results = []

            for sent in sents:
                match1 = re.search(r"[A-Z]\w+.\w+.\w+.\w+.\w+.by", sent)
                match2 = re.search(r"((\b[Rr]ead(ing)?\b)|(\b[Ff]inish(ed)?\b)|(\b[Ll]ike(d)?\b)|(\b[Ee]njoy(ed)?\b)|(\b[Ll]ove(d)?\b)|(\b[Nn]amed\b)|(\b[Cc]alled\b)|(\b[Ee]ntitled\b)|(\'s\b))..?[A-Z]\w+.\w+.\w+.\w+.\w+.\w+",sent)

                if match1:
                    get_highest_score = {}
                    searchsent = match1.group(0).rstrip(" by")
                    print(searchsent)

                    for title, workid in book_and_version.items():
                        zoekresultaat = fuzz.ratio(title, searchsent)
                        if zoekresultaat > ratio:
                            get_highest_score[zoekresultaat] = (threadid, postid, workid)

                    if len(get_highest_score.keys()) > 0:
                        highest = max(get_highest_score.keys())
                        results.append(get_highest_score[highest])

                            #print(threadid, postid, searchsent, zoekresultaat, title)
                            #results.append((threadid, postid, workid))

                if match2:
                    get_highest_score = {}
                    searchsent1 = match2.group(0)
                    searchsent2 = word_tokenize(searchsent1)
                    if (searchsent2[-1])[0].islower():
                        searchsent = " ".join(searchsent2[1:-1])
                    else:
                        searchsent = " ".join(searchsent2[1:])

                    print(searchsent)

                    for title, workid in book_and_version.items():
                        zoekresultaat = fuzz.ratio(title, searchsent)
                        if zoekresultaat > ratio:
                            get_highest_score[zoekresultaat] = (threadid, postid, workid)

                    if len(get_highest_score.keys()) > 0:
                        highest = max(get_highest_score.keys())
                        results.append(get_highest_score[highest])

                            #print(threadid, postid, searchsent, zoekresultaat, title)
                            #results.append((threadid, postid, workid))

            if len(results) > 0:
                resultset = set(results)
                print(set(results))
                for item in resultset:
                    item_string = " ".join(item)
                    outfile.write(item_string)
                    outfile.write("\n")
            else:
                print("no titles")


    outfile.close()

