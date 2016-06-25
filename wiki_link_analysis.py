
from event_extract_package import *
import wikipedia
wikipedia.set_lang("zh-tw")


# load wiki content :

# 台灣歷史年表
# 台灣歷史
# 台灣日治時期
# TODO: 若整個頁面有一個地點，所有裡面的歷史事件就用該頁面的地點
# TODO: 若整個頁面非一個地點，所有歷史事件就用該句子中有包含的地點。若該歷史事件的句子還是沒有

# TODO:
# 從台灣古蹟列表
# 名稱、經緯度、年、（月、日）、URL、地址、introduction

page = wikipedia.page('台灣古蹟列表')

link_data = dict()
len(page.links)
len(page.links)

for link in page.links[10:100]:
    try:
        link_page = wikipedia.page(link)
        event_lists,sentences = get_clean_events(link_page)
        link_data[link]={
            "sentences":sentences,
            "event_lists":event_lists,
            "links":link_page.links
        }
    except:
        None
link_data.keys()

for key in link_data.keys():
    print(key)
    print("historical word count : ",len("。".join(get_value_list(link_data[key]['event_lists'],'description'))))
    print("total word count : ",len("。".join(link_data[key]['sentences'])))
    print("historical description count :",len(link_data[key]['event_lists']))
    print("total description count :",len(link_data[key]['sentences']))
