from get_places import *
from event_extract_package import *
import wikipedia
wikipedia.set_lang("zh-tw")
page = wikipedia.page('台灣古蹟列表')

print(len(page.links))
site_pages = []
count = 0
for link in page.links[100:120]:
    count=count+1
    print(count)
    site_pages.append(wikipedia.page(link))



def get_json_from_page(page):
    from hanziconv import HanziConv
    stopwords = load_stop_words()
    cat_constrain_set = set(tokenize(HanziConv.toTraditional("。".join(page.categories)),stopwords))
    summary_constrain_set = set(tokenize(HanziConv.toTraditional("。".join(page.summary)),stopwords))
    return get_places(page.title,cat_constrain_set|summary_constrain_set)



jsons_dicts = dict()
for page in site_pages:
    try:
        jsongeocode=get_json_from_page(site_pages[0])

        jsons_dicts[page.title]={
            'name':jsongeocode['result']['name'],
            'geometry':jsongeocode['result']['geometry'],
            'address':jsongeocode['result']['formatted_address'],
            'map_url':jsongeocode['result']['url'],
            'site_type':jsongeocode['result']['types']
        }

    except:
        jsons_dicts[page.title]=None

import six.moves.cPickle as pickle
# save data
with open("geo_info.dat", "wb") as f:
    pickle.dump(jsons_dicts, f, protocol=1)
