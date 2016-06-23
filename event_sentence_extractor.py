
from event_extract_package import *
import wikipedia
wikipedia.set_lang("zh-tw")
import wikitextparser as wtp
# load wiki content :

page = wikipedia.page('台灣歷史年表')

sentences = []
for line in page.content.split():
    sentences.extend(line.split('。'))




event_lists = filter_event(sentences)

len(event_lists)
