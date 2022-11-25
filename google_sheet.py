import requests
import config as conf

def google_sheet_update(data1, data2, data3, data4, data5):
    url = conf.GAS_URL
    # need to pass str params to the url otherwise process fails
    if isinstance(data4, int): 
        requests.get(url + '?data1=' + data1 + '&data2=' + str(data2) + '&data3=' + data3)
    else:
        requests.get(url + '?data1=' + data1 + '&data2=' + str(data2) + '&data3=' + data3 + '&data4=' + data4 + '&data5=' + data5)