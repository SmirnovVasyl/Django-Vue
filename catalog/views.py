from django.http import HttpResponse
from catalog.models import btc_price
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser

import time
import bitfinex
import datetime
import pandas as pd

@api_view(['GET'])
def insertPriceList(request):
    priceLists = btc_price.objects.all().values()
    if(len(priceLists) <= 0):
        pair = 'BTCUSD'
        TIMEFRAME = '4h'
        api_v2 = bitfinex.bitfinex_v2.api_v2()

        t_start = datetime.datetime(2022, 9, 1, 0, 0)
        t_start = time.mktime(t_start.timetuple()) * 1000

        t_stop = datetime.datetime(2023, 2, 1, 0, 0)
        t_stop = time.mktime(t_stop.timetuple()) * 1000

        result = api_v2.candles(symbol=pair, interval=TIMEFRAME, limit=1000, start=t_start, end=t_stop)
        # names = ['Date', 'Open', 'Close', 'High', 'Low', 'Volume']

        for data in result:
            date =  pd.to_datetime(data[0], unit='ms')
            btc_price(Date=date, Open=data[1], Close=data[2], High=data[3], Low=data[4], Volume=data[5]).save()

    return HttpResponse('<h1>Django Project</h1>')
    
@api_view(['GET'])
def getPriceList(request):
    priceLists = btc_price.objects.all().values()
    if(len(priceLists) <= 0):
        pair = 'BTCUSD'
        TIMEFRAME = '4h'
        api_v2 = bitfinex.bitfinex_v2.api_v2()

        t_start = datetime.datetime(2022, 9, 1, 0, 0)
        t_start = time.mktime(t_start.timetuple()) * 1000

        t_stop = datetime.datetime(2023, 2, 1, 0, 0)
        t_stop = time.mktime(t_stop.timetuple()) * 1000

        result = api_v2.candles(symbol=pair, interval=TIMEFRAME, limit=1000, start=t_start, end=t_stop)
        # names = ['Date', 'Open', 'Close', 'High', 'Low', 'Volume']

        for data in result:
            date =  pd.to_datetime(data[0], unit='ms')
            btc_price(Date=date, Open=data[1], Close=data[2], High=data[3], Low=data[4], Volume=data[5]).save()
    
    priceLists = btc_price.objects.all().values()
    return Response(priceLists)

@api_view(['POST'])
@parser_classes([JSONParser])
def deleteItem(request):
    btc_price.objects.filter(id=request.data['key']).delete()

    priceLists = btc_price.objects.all().values()
    return Response(priceLists)
