from util_package import *
# TODO:segmentization of chinese sentences :
import jieba
import jieba.analyse
import jieba.posseg as pseg
jieba.set_dictionary('dict.txt.big.txt')
jieba.enable_parallel(4)
jieba.analyse.set_stop_words('stop_words.txt')
jieba.analyse.set_idf_path('idf.txt.big.txt')
jieba.initialize()

def tokenize(sentence,addwords=None):
    if(addwords!=None):
        for word in addwords:
            jieba.add_word(word)
    tokens = []
    for term in jieba.tokenize(sentence):
        tokens.append(term[0])
    return tokens
def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

def split_times(times):
    positions = [values[1] for values in merge_lists(times.values())]

    splits = split_list_by_gap(positions,2)

    split_zip = []
    for i in range(len(splits)):
        for position in splits[i]:
            split_zip.append((position,i))
    split_dict = dict(split_zip)


    split_times_dict = dict()
    for i in range(len(splits)):
        split_times_dict[i] = {'年':[],'月':[],'日':[]}


    for ymd in times.keys():
        for time in times[ymd]:

            split_times_dict[split_dict[time[1]]][ymd].append(time[0])

    return split_times_dict
def split_list_by_gap(num_list,merge_gap):
    num_sets = [set([num])for num in num_list]
    num_sets
    def two_num_set_close(A,B,diff):
        for a in A:
            for b in B:
                if(abs(a-b)<=diff):
                    return True
        return False

    for i in range(len(num_sets)):
        for j in range(i+1,len(num_sets)):

            if(two_num_set_close(num_sets[i],num_sets[j],merge_gap)):
                num_sets[j] = num_sets[j]|num_sets[i]
                num_sets[i] = set()
                break

    splits = []
    for num_set in num_sets:
        if(len(num_set)!=0):
            splits.append(list(num_set))
    return splits

def filter_event(sentences):
    import numpy as np

    event_list = []
    for sentence in sentences:
        event_dict = dict()
        tokens = tokenize(sentence)
        #tags = [tag[1].split('#')[1] for tag in st.tag(tokens)]
        time_dict = dict()
        time_dict['年'] = []
        time_dict['月'] = []
        time_dict['日'] = []
        if np.sum(np.array([token.isdigit() for token in tokens])==True)>0:
            is_event = False
            for cd_tag_index in list(np.where(np.array([token.isdigit() for token in tokens])==True)[0]):
                try:
                    if tokens[cd_tag_index+1]=='年' or tokens[cd_tag_index+1]=='月' or tokens[cd_tag_index+1]=='日' or tokens[cd_tag_index+1]=='世紀':
                        #print('time:',tokens[cd_tag_index],tokens[cd_tag_index+1])
                        time_dict[tokens[cd_tag_index+1]].append((tokens[cd_tag_index],cd_tag_index+1))
                        is_event = True
                except:
                    None
            if is_event:
                event_dict['time']=time_dict
                event_dict['description']=sentence
                event_list.append(event_dict)
        else:
            None







    for event in event_list:
        event['time']=split_times(event['time'])
    return event_list
