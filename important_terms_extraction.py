# 1. all wikipedia links
links = set(page.links)
len(links)
# 2. all high textrank terms
for link in links:
    jieba.add_word(link)
high_textrank_terms = set(jieba.analyse.textrank(page.content, topK=int(len(page.content)*0.1), withWeight=False))
len(high_textrank_terms)
high_textrank_terms

# 3. all nouns in sentences grab by jeiba
nouns = set()
for event in event_lists:
    nouns = nouns|set(jieba.analyse.extract_tags(event['description'], topK=1000, withWeight=False, allowPOS=('ns', 'n')))

len(nouns)


# 4. all nouns in sentences grab by jeiba
verbs = set()
for event in event_lists:
    verbs = verbs|set(jieba.analyse.extract_tags(event['description'], topK=1000, withWeight=False, allowPOS=('vn', 'v')))
len(verbs)

# 5. all kind of noun and verbs grab by StanfordPOSTagger
NN = set()
NR = set()
VV = set()
# REVIEW : initialize tagger
from nltk.tag import StanfordPOSTagger
stanford_pos_dir = '/Users/jeffrey_mac/stanford-postagger-full-2015-12-09/'
chi_model_filename= stanford_pos_dir + 'models/chinese-distsim.tagger'
my_path_to_jar= stanford_pos_dir + 'stanford-postagger.jar'

st = StanfordPOSTagger(model_filename=chi_model_filename, path_to_jar=my_path_to_jar)


for event in event_lists:
    tags = st.tag(tokenize(event['description']))
    token_tag_pair = []
    for tag in tags:
        token_tag_pair.append((tag[1].split('#')[1],tag[1].split('#')[0]))
    tag_dict = dict()
    for pair in token_tag_pair:
        if pair[0] in tag_dict:
            tag_dict[pair[0]]=tag_dict[pair[0]]|set([pair[1]])
        else:
            tag_dict[pair[0]]=set([pair[1]])
    print(event['description'])
    #print(tag_dict)
    def token_set(tag):
        try:
            return tag_dict[tag]
        except:
            return set()
    NN = NN|token_set('NN')
    NR = NR|token_set('NR')
    VV = VV|token_set('VV')
NN
NR
VV

from nltk.tag import StanfordNERTagger
stanford_ner_dir = '/Users/jeffrey_mac/stanford-ner-2015-12-09//'
chi_model_filename= stanford_ner_dir + 'classifiers/chinese.misc.distsim.crf.ser.gz'
my_path_to_jar= stanford_ner_dir + 'stanford-ner.jar'

ner_st = StanfordNERTagger(model_filename=chi_model_filename,path_to_jar=my_path_to_jar)


tag_dict = dict()
for event in event_lists:
    token_tag_pair = ner_st.tag(tokenize(event['description']))
    print(event['description'])
    for pair in token_tag_pair:
        if pair[1] in tag_dict:
            tag_dict[pair[1]]=tag_dict[pair[1]]|set([pair[0]])
        else:
            tag_dict[pair[1]]=set([pair[0]])

    #print(tag_dict)
GPE=set(tag_dict['GPE'])
PERSON=set(tag_dict['PERSON'])
ORG=set(tag_dict['ORG'])
LOC=set(tag_dict['LOC'])
MISC=set(tag_dict['MISC'])


terms_lists = [links,           # 0
    high_textrank_terms,        # 1
    nouns,                      # 2
    verbs,                      # 3
    NN,                         # 4
    NR,                         # 5
    VV,                         # 6
    GPE,                        # 7
    PERSON,                     # 8
    ORG,                        # 9
    LOC,                        # 10
    MISC]                       # 11
