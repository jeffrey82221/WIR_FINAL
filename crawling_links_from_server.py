import numpy as np
import pickle
import six.moves.cPickle as pickle
# load data
with open("data_dict2.dat", 'rb') as f:
    data_dict = pickle.load(f)

import pandas as pd

new_data_dict = dict()
for key in data_dict.keys():
    if data_dict[key]['geo_info'] != None and data_dict[key]['wiki'] != None:
        new_data_dict[key] = data_dict[key]

key = list(new_data_dict.keys())[0]

all_links = []
for key in new_data_dict.keys():
    all_links.extend(new_data_dict[key]['wiki']['links'])


link_set = set(all_links)
link_set

from get_places import *
from event_extract_package import *
import wikipedia
wikipedia.set_lang("zh-tw")

def get_json_from_page(page):
    from hanziconv import HanziConv
    stopwords = load_stop_words()
    cat_constrain_set = set(tokenize(HanziConv.toTraditional("。".join(page.categories)),stopwords))
    summary_constrain_set = set(tokenize(HanziConv.toTraditional("。".join(page.summary)),stopwords))
    return get_places(page.title,cat_constrain_set|summary_constrain_set)



data_dict = dict()
count = 0

for link in list(link_set):
    count=count+1
    print(count,link)
    try:
        site_page = wikipedia.page(link)
    except:
        "cannot match with any wiki page"
        continue
    geo_dict = dict()
    wiki_dict = dict()
    try:
        jsongeocode=get_json_from_page(site_page)

        geo_dict={
            'name':jsongeocode['result']['name'],
            'geometry':jsongeocode['result']['geometry'],
            'address':jsongeocode['result']['formatted_address'],
            'map_url':jsongeocode['result']['url'],
            'site_type':jsongeocode['result']['types']
        }

    except:
        print('no geo_info:',link)
        geo_dict=None
    try:
        event_lists,sentences = get_clean_events(site_page)
        wiki_dict={
            "url":site_page.url,
            "sentences":sentences,
            "event_lists":event_lists,
            "links":site_page.links,
            "historical_word_count":len("。".join(get_value_list(event_lists,'description'))),
            "historical_description_count":len(event_lists),
            "total_word_count":len("。".join(sentences)),
            "total_description_count":len(sentences),

        }
    except:
        print("no wiki info:",link)
        wiki_dict=None
    data_dict[link]={
        'wiki':wiki_dict,
        'geo_info':geo_dict

    }

import six.moves.cPickle as pickle
# save data
with open("link_data_dict.dat", "wb") as f:
    pickle.dump(data_dict, f, protocol=1)
