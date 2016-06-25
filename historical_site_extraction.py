import wikipedia
wikipedia.set_lang("zh-tw")
import wikitextparser as wtp
from hanziconv import HanziConv

# 台灣歷史年表
# 台灣歷史
# 台灣日治時期
# 臺灣古蹟列表
# TODO: 若整個頁面有一個地點，所有裡面的歷史事件就用該頁面的地點
# TODO: 若整個頁面非一個地點，所有歷史事件就用該句子中有包含的地點。若該歷史事件的句子還是沒有
page = wikipedia.page('臺灣古蹟列表')

from get_place import *
for site in page.links[0:10]:
    print(site)
    print(get_places(site))
wikipedia.page('三崁店社')
中華民國直轄市定古蹟

wikipedia.search('古蹟')

wikipedia.page('中正紀念堂').coordinates
wikipedia.geosearch(25.03555555999999882033080211840569972991943359375,121.51972222000000556363374926149845123291015625)
