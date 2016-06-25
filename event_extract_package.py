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

    splits = split_list_by_gap(positions,3)

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

def get_sentences(page):
    from hanziconv import HanziConv
    sentences = []
    for line in HanziConv.toTraditional(page.content).splitlines():
        sentences.extend(line.split('。'))
    return sentences


def filter_event(sentences):
    import numpy as np

    event_list = []
    for sentence in sentences:
        event_dict = dict()
        tokens = tokenize(sentence.replace(',',''))
        #tags = [tag[1].split('#')[1] for tag in st.tag(tokens)]
        time_dict = dict()
        time_dict['年'] = []
        time_dict['月'] = []
        time_dict['日'] = []
        time_dict['其他'] = []
        if np.sum(np.array([token.isdigit() for token in tokens])==True)>0:
            is_event = False
            for cd_tag_index in list(np.where(np.array([token.isdigit() for token in tokens])==True)[0]):
                try:
                    #print(tokens[cd_tag_index+1][0:1])
                    if tokens[cd_tag_index+1][0:2]=='年前':
                        time_dict['年'].append((-int(tokens[cd_tag_index]),cd_tag_index))
                    elif tokens[cd_tag_index+1][0:1]=='年':
                        # REVIEW : calcultate the real number with chinese char
                        pre_year = int(tokens[cd_tag_index])
                        if tokens[cd_tag_index-1]=='萬':
                            pre_year=int(tokens[cd_tag_index-2])*10000+int(tokens[cd_tag_index])
                        # REVIEW fix the year to 公元
                        if(tokens[cd_tag_index-1][-2:]=='元前'):
                            year = -pre_year
                        elif(tokens[cd_tag_index-1][-2:]=='約'):
                            if(tokens[cd_tag_index-2][-2:]=='元前'):
                                year = -pre_year
                            else:
                                year = pre_year
                        elif(pre_year<=4000):
                            year = pre_year
                        else:
                            year = 2000-pre_year

                        time_dict['年'].append((year,cd_tag_index))
                        is_event = True
                    elif tokens[cd_tag_index+1][0:2]=='萬年':
                        pre_year=int(tokens[cd_tag_index])*10000
                        #print(pre_year)
                        time_dict['年'].append((-pre_year,cd_tag_index))
                        is_event = True
                    elif tokens[cd_tag_index+1][0:2]=='世紀':
                        #print(tokens[cd_tag_index])
                        #print(tokens[cd_tag_index+1])
                        #print(tokens[cd_tag_index-1][-2:])
                        if(tokens[cd_tag_index-1][-2:]=='元前'):
                            #print(-(int(tokens[cd_tag_index])*100))
                            time_dict['年'].append((-int(tokens[cd_tag_index])*100,cd_tag_index))

                        else:
                            time_dict['年'].append((int(tokens[cd_tag_index])*100,cd_tag_index))
                        is_event = True
                    elif(tokens[cd_tag_index-1][-2:]=='元前'):
                        #if tokens[cd_tag_index+1]=='世紀':
                        time_dict['年'].append((-int(tokens[cd_tag_index]),cd_tag_index))
                        #else:
                        #    time_dict['年'].append((-int(tokens[cd_tag_index]),cd_tag_index))
                        is_event = True
                    #elif tokens[cd_tag_index+1][0:1]=='年前':
                    #    pre_year = int(tokens[cd_tag_index])
                    #    if tokens[cd_tag_index-1]=='萬':
                    #        pre_year=(int(tokens[cd_tag_index-2])*10000+int(tokens[cd_tag_index]))
                    #    if(pre_year<=4000):
                    #        year = pre_year
                    #    else:
                    #        year = 2000-pre_year
                    #    time_dict['年'].append((int(tokens[cd_tag_index]),cd_tag_index+1))
                    #    is_event = True
                    elif tokens[cd_tag_index+1][0:1]=='月':
                        time_dict['月'].append((int(tokens[cd_tag_index]),cd_tag_index))
                        is_event = True
                    elif tokens[cd_tag_index+1][0:1]=='日':
                        time_dict['日'].append((int(tokens[cd_tag_index]),cd_tag_index))
                        is_event = True
                    #else:
                    #    time_dict['其他'].append(tokens[cd_tag_index])
                    #if tokens[cd_tag_index+1][0:1]=='年' or tokens[cd_tag_index+1][0:1]=='月' or tokens[cd_tag_index+1][0:1]=='日' or tokens[cd_tag_index+1][0:2]=='世紀':
                        #print('time:',tokens[cd_tag_index],tokens[cd_tag_index+1])
                    #    time_dict[tokens[cd_tag_index+1]].append((tokens[cd_tag_index],cd_tag_index+1))
                    #    is_event = True
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


def remove_wrong_year(sentences):
    sentences_clean = []
    for sent in sentences[:len(sentences)]:
        try:
            sentences_clean.append(find_parensis(sent)[0])
        except:
            None

    return sentences_clean


def show_times(event_lists):
    for event in event_lists:
        print(event['description'])
        for time in event['time'].values():
            print(time['年'],time['月'],time['日'])

# TODO adding years to other event without year
def event_year_correct(event_lists):
    for event in event_lists:
        loss_year = False
        loss_year_time = []
        with_year_time = []
        for time in event['time'].values():
            if len(time['年'])==0 and len(time['月'])==1:
                loss_year_time.append(time)
                loss_year = True
            else:
                with_year_time.append(time)

        if(loss_year==True):
            if len(with_year_time)>0:
                for time in loss_year_time:
                    time['年']=with_year_time[0]['年']
                print(event['description'])
                print(with_year_time)
                print(loss_year_time)
            elif(len(with_year_time)>1):
                print('ERROR:more then one time element have year : Please choose one!')
    return event_lists


# TODO:add loss year to event from previous event
def add_loss_year(event_lists):
    for event in event_lists:
        for time in event['time'].values():
            #print(len(time['年']),len(time['月']),len(time['日']))
            if len(time['年'])==0 and len(time['月'])==1:
                print(event['description'])
                print('loss year')
                time['年']=previous_time['年']
            #print(time['年'],time['月'],time['日'])
        if len(time['年'])==1:
            previous_time = time
    return event_lists

# @REVIEW final get event code !
def get_clean_events(page):
    sentences=get_sentences(page)
    sentences=remove_wrong_year(sentences)
    event_lists = filter_event(sentences)
    event_lists = event_year_correct(event_lists)
    event_lists = add_loss_year(event_lists)
    return event_lists,sentences
