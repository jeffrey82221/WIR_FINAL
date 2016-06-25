from util_package import *
def get_places(site_name,constrain_set=None):
    key   = "AIzaSyBpk_fl186DGDalxmf2MSzG1126EFDBauM"
    #token = "EAALoPr8WJz4BACuIz1hSKsDdez4DRztUghLXsEzQKZB92ssnv8kOR1YYdUB2ZCTU1i3DLHRSkWZA3eH0ZBYOnZBPZCGKaBX7H17Kv6wtPQYUEhgjkrVb7LtOXo4m5OodgNRZCKVLXZAnZAAmGbvZCaonfz33ZAmW4wsiKQZD"
    import json
    import sys
    import urllib
    from urllib.parse import quote

    import numpy as np

    def get_json_from_google(site_name,key):
        input = quote(site_name)
        url = "https://maps.googleapis.com/maps/api/place/queryautocomplete/json?input=%s&key=%s&language=zh-TW" % (input, key)
        import urllib.request, json
        response = urllib.request.urlopen(url)
        content = response.read()
        jsongeocode = json.loads(content.decode("utf8"))
        return jsongeocode
    def query_fix(jsongeocode,constrain_set):
        ok_prediction = []
        for predict in jsongeocode['predictions']:
            predict_ok = False
            for term in predict['terms']:
                if term['value'] in constrain_set:
                    predict_ok = True
            if predict_ok:
                ok_prediction.append(predict)
        scores = []
        ok_prediction[0]
        for term in ok_prediction[0]['terms']:
            scores.append(edition_distance(term['value'],site_name))

        query_list = []
        for i in range(np.argmin(scores)+1):
            query_list.append(ok_prediction[0]['terms'][i]["value"])

        return " ".join(query_list)

    jsongeocode = get_json_from_google(site_name,key)

    if jsongeocode['status'] != 'OK':
        print(jsongeocode['status'])
        return None
    # reselect site
    if 'place_id' not in jsongeocode['predictions'][0]:
        new_query = query_fix(jsongeocode,constrain_set)
        jsongeocode = get_json_from_google(new_query,key)


    if jsongeocode['status'] != 'OK':
        print(jsongeocode['status'])
        return None
    id  = jsongeocode['predictions'][0]['place_id']


    url = "https://maps.googleapis.com/maps/api/place/details/json?placeid=%s&key=%s" % (id, key)
    response = urllib.request.urlopen(url)
    content = response.read()
    jsongeocode = json.loads(content.decode("utf8"))


    if jsongeocode['status'] != 'OK':
        print(jsongeocode['status'])
        return None

    return jsongeocode
    #dis = "1000"
    #url = 'https://graph.facebook.com/search?type=place&center=' + lat + ',' + lng + '&distance=' + dis + '&access_token=' + token
    #response = urllib.request.urlopen(url)
    #jsongeocode = json.loads(response.read().decode("utf8"))

    #return jsongeocode['data']


#site_name = "中正紀念堂"
#get_places(site_name,constrain_set=constrain_set)
#input = "三崁店"
#input = '台南孔廟'
#get_places('台南孔廟')

#jsongeocode['result']['formatted_address']
#jsongeocode["result"]["geometry"]['viewport']
#lat = str(jsongeocode["result"]["geometry"]["location"]['lat'])
#    lng = str(jsongeocode["result"]["geometry"]["location"]['lng'])
