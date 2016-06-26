def get_table(lower,upper,save_table=None,site_input=None):
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

    for key in new_data_dict.keys():
        new_data_dict[key]['geo_info'].update(new_data_dict[key]['wiki'])
        new_data_dict[key] = new_data_dict[key]['geo_info']


    for key in new_data_dict.keys():
        new_data_dict[key].update(new_data_dict[key]['geometry'])
        new_data_dict[key].update(new_data_dict[key]['location'])
        # new_data_dict[key].update(new_data_dict[key]['viewport'])

    all_event_lists = []
    for key in new_data_dict.keys():
        for event in new_data_dict[key]['event_lists']:
            event['key'] = key
        all_event_lists.extend(new_data_dict[key]['event_lists'])

    for event in all_event_lists:
        event.update(event['time'])

    for event in all_event_lists:
        for i in range(5):
            try:
                event[i] = float(event[i]['年'][0])
            except:
                event[i] = float('nan')
                None

    all_event_table = pd.DataFrame.from_dict(all_event_lists)

    # all_event_table.to_csv('all_event_table.csv')

    all_event_table = all_event_table.drop('time', 1)
    all_event_table.index = np.array(all_event_table['key'])
    all_event_table = all_event_table.drop('key', 1)

    def range_filter(df, keys, lower, upper):
        key = keys[0]
        true_false_table = np.array(df[[key]] <= upper) & np.array(df[[key]] >= lower)
        for key in keys:
            true_false_table = true_false_table | (np.array(df[[key]] <= upper) & np.array(df[[key]] >= lower))
        return df[true_false_table]

    new_data_table = pd.DataFrame.from_dict(new_data_dict).transpose()
    new_data_table

    new_data_table = new_data_table.drop('sentences', 1)
    new_data_table = new_data_table.drop('site_type', 1)
    new_data_table = new_data_table.drop('location', 1)
    new_data_table = new_data_table.drop('links', 1)
    new_data_table = new_data_table.drop('geometry', 1)
    new_data_table = new_data_table.drop('event_lists', 1)


    #new_data_table[['historical_word_count']]
    #new_data_table[['total_word_count']]
    #new_data_table[['historical_description_count']]
    #new_data_table[['total_description_count']]


    # TODO: re calculate historial score
    for site in new_data_table.index:
        try:
            result_table = range_filter(
                all_event_table, [0, 1, 2, 3, 4], lower, upper).transpose()[[site]]
            description_count = len(result_table.transpose())
            word_count = len(np.array2string(
                np.array(result_table.transpose()[['description']])))
            new_data_table.set_value(
                site, 'historical_description_count', description_count)
            new_data_table.set_value(site, 'historical_word_count', word_count)
        except:
            new_data_table.set_value(site, 'historical_description_count', 0)
            new_data_table.set_value(site, 'historical_word_count', 0)





    score_table = pd.DataFrame((np.array(new_data_table[['historical_description_count']]) + np.array(new_data_table[['historical_word_count']])) /(np.log(np.array(new_data_table[['total_word_count']], dtype=float)) + np.log(np.array(new_data_table[['total_description_count']], dtype=float))))
    #score_table = pd.DataFrame((np.array(new_data_table[['historical_description_count']]) + np.array(new_data_table[['historical_word_count']])) / (
    #    np.array(new_data_table[['total_word_count']], dtype=float) + np.array(new_data_table[['total_description_count']], dtype=float)))
    # score_table = pd.DataFrame(np.array(new_data_table[['total_description_count']]) / np.log(
    #    np.array(new_data_table[['total_description_count']], dtype=float)))
    score_table.index = new_data_table.index


    static_table = pd.concat([new_data_table, score_table],
                             axis=2).sort(0, ascending=False)
    static_table



    if site_input!=None:
        try:
            result_table = range_filter(
                all_event_table, [0, 1, 2, 3, 4], lower, upper).transpose()[[site_input]].transpose()
        except:
            print('no matched result')
            result_table = None
            None
    else:
        result_table = range_filter(
            all_event_table, [0, 1, 2, 3, 4], lower, upper)

    if save_table!=None:
        static_table.to_csv("site"+save_table)
        try:
            result_table.to_csv("event"+save_table)
        except:
            None

    return static_table,result_table


table = get_table(0,3000,save_table='table.csv')
table[0]

table2 = get_table(0,3000,save_table='table.csv',site_input='臺灣')

table2[1]
import numpy as np

np.array(table2[1][['description']]).tolist()
