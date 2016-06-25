
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





import pickle
import six.moves.cPickle as pickle
# load data
with open("data_dict.dat", 'rb') as f:
    data_dict = pickle.load(f)


for key in data_dict.keys():
    if data_dict[key]['geo_info']==None:
        print(key)
        try:
            site_page=wikipedia.page(key)
            jsongeocode=get_json_from_page(site_page)

            geo_dict={
                'name':jsongeocode['result']['name'],
                'geometry':jsongeocode['result']['geometry'],
                'address':jsongeocode['result']['formatted_address'],
                'map_url':jsongeocode['result']['url'],
                'site_type':jsongeocode['result']['types']
            }
            data_dict[key]['geo_info']=geo_dict
        except:
            print("no match")
            None


import six.moves.cPickle as pickle
# save data
with open("data_dict2.dat", "wb") as f:
    pickle.dump(data_dict, f, protocol=1)
