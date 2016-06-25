
import pickle
import six.moves.cPickle as pickle
# load data
with open("data_dict_small.dat", 'rb') as f:
    data_dict = pickle.load(f)

import pandas as pd

new_data_dict = dict()
for key in data_dict.keys():
    if data_dict[key]['geo_info']!=None and data_dict[key]['wiki']!=None:
        new_data_dict[key]=data_dict[key]

for key in new_data_dict.keys():
    new_data_dict[key]['geo_info'].update(new_data_dict[key]['wiki'])
    new_data_dict[key]=new_data_dict[key]['geo_info']


for key in new_data_dict.keys():
    new_data_dict[key].update(new_data_dict[key]['geometry'])
    new_data_dict[key].update(new_data_dict[key]['location'])
    #new_data_dict[key].update(new_data_dict[key]['viewport'])



all_event_lists = []
for key in new_data_dict.keys():
    for event in new_data_dict[key]['event_lists']:
        event['key']=key
    all_event_lists.extend(new_data_dict[key]['event_lists'])

for event in all_event_lists:
    event.update(event['time'])

for event in all_event_lists:
    for i in range(5):
        try:
            event[i]=event[i]['年'][0]
        except:
            None

all_event_table = pd.DataFrame.from_dict(all_event_lists)

all_event_table.to_csv('all_event_table.csv')

all_event_table
all_event_table = all_event_table.drop('time', 1)

new_data_table=pd.DataFrame.from_dict(new_data_dict).transpose()
new_data_table

new_data_table=new_data_table.drop('sentences',1)
new_data_table=new_data_table.drop('site_type',1)
new_data_table=new_data_table.drop('location',1)
new_data_table=new_data_table.drop('links',1)
new_data_table=new_data_table.drop('geometry',1)
new_data_table=new_data_table.drop('event_lists',1)

new_data_table[['historical_word_count']]
new_data_table[['total_word_count']]
new_data_table[['historical_description_count']]
new_data_table[['total_description_count']]

import numpy as np
score_table = pd.DataFrame(np.array(new_data_table[['historical_word_count']])/np.array(new_data_table[['total_word_count']]))
score_table
new_data_table[['historical_word_count']]=score_table
