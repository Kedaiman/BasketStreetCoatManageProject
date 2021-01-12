import requests
from ..models import Goal, User, Prefecture, Impression, Changedhistory, Changeapplication
from django.utils.timezone import localtime
from django.utils import timezone
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

# ページ情報返却
def getpage(request):
    if 'page_dict' in request.session and 'goal' in request.session:
        page_dict = request.session['page_dict']
        goal = request.session['goal']

        app_page = page_dict['changeApplication']
        imp_page = page_dict['impression']
        his_page = page_dict['changeHistory']

        changeapp_all = Changeapplication.objects.filter(goal_id=goal).all().reverse()
        changehis_all = Changedhistory.objects.filter(goal_id=goal).all().reverse()
        impression_all = Impression.objects.filter(goal_id=goal).all().reverse()

        changeapp_list = changeapp_all[(5*(app_page-1)) : 5*app_page]
        changehis_list = changehis_all[(5*(his_page-1)) : 5*his_page]
        impression_list = impression_all[(5*(imp_page-1)) : 5*imp_page]

        request.session['changeapp_list'] = changeapp_list
        request.session['impression_list'] = impression_list
        request.session['changehis_list'] = changehis_list

        # 変更申請一覧の最大ページを計算 
        if (len(changeapp_all) % 5) == 0:
            if len(changeapp_all) != 0:
                app_page_max = len(changeapp_all) // 5
            else:
                app_page_max = 1
        else:
            app_page_max = (len(changeapp_all) // 5) + 1

        # 感想一覧の最大ページを計算 
        if (len(impression_all) % 5) == 0:
            if len(impression_all) != 0: 
                imp_page_max = len(impression_all) // 5
            else:
                imp_page_max = 1
        else:
            imp_page_max = (len(impression_all) // 5) + 1

        # 変更履歴一覧の最大ページを計算 
        if (len(changehis_all) % 5) == 0:
            if len(changehis_all) != 0:
                his_page_max = len(changehis_all) // 5
            else:
                his_page_max = 1
        else:
            his_page_max = (len(changehis_all) // 5) + 1

        page_data = {
                  'app_page': app_page,
                  'app_page_max': app_page_max,
                  'imp_page': imp_page,
                  'imp_page_max': imp_page_max,
                  'his_page': his_page,
                  'his_page_max': his_page_max,
        }
        return page_data
    else:
        return None

            
def get_lat_lon_from_address(address):
    url = 'http://www.geocoding.jp/api/'
    #latlons = []
    payload = {"v": 1.1, 'q': address}
    r = requests.get(url, params=payload)
    ret = BeautifulSoup(r.content,'lxml')
    if ret.find('error'): 
        raise ValueError(f"Invalid address submitted. {address}")
    else:
        lat = ret.find('lat').string
        lon = ret.find('lng').string
        latlon = {"lat":lat, "lon":lon}
            
    return latlon 

def get_lat_lon_from_addresses(address_list):
    latlon_list = []
    for address in address_list:
        latlon = get_lat_lon_from_address(address)
        latlon_list.append(tuple(latlon.values()))
    return latlon_list
