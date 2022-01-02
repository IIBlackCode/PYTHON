import mimetypes
import os
import urllib

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.generic import View
from rest_framework.views import APIView
from django.template import loader
from datetime import datetime
import random
import json
import csv

from rest_framework.views import APIView

#------------------------- Simulator 관련 변수
from .Stock import *

from tkinter.filedialog import *
from tkinter.simpledialog import *
from tkinter import *

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.font_manager as fm
import pandas as pd
import numpy as np

import datetime
import time

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from datetime import datetime
import random


modelPath = './models'
csvPath = './project_bigdata/csv'
fontPath = './NanumFontSetup_TTF_SQUARE'
fontLight = fm.FontProperties(fname=fontPath + '/NanumSquareL.ttf', size=18)
fontBold = fm.FontProperties(fname=fontPath + '/NanumSquareB.ttf', size=18)
g_theme, g_stock, g_term, g_data = '', '', '', ''
g_model, g_predictDate = '', ''

dfStock = []
xy = []
column = []
standardDate = ""
modelName = ""
#------------------------- End


def index(request) :
    context = {}
    return render(request, 'Simulator.html', context)


def data_sync(request) :
    print("데이터 동기화 버튼")
    return render(request, 'Simulator.html')


def elements(request) :
    print("PAGE : elements")
    return render(request, 'elements.html')


def icons(request) :
    print("PAGE : icons")
    return render(request, 'icons.html')


# 테마 선택
def openCSV(filename):

    if 'Total' in filename:
        df_price = pd.read_csv(os.path.join(csvPath, filename + '.csv'), encoding='euc-kr')
    else:
        df_price = pd.read_csv(os.path.join(csvPath, filename + '.csv'), encoding='utf-8')
    return df_price


def radioTheme(request) :
    global g_theme, g_stock, g_term, g_data
    global g_model, g_predictDate
    #POST 방식으로 SELECT태그에 선택된 문자 받아온다.
    g_theme = request.POST.get('select_theme')
    print("테마 : "+g_theme)

    # 선택된 테마에 해당되는 종목을 'Total.csv'에서 찾아 종목리스트에 출력
    dfTotal = openCSV('Total')
    npTotal = dfTotal.to_numpy()
    npTheme = []

    if g_theme == "게임":
        npTheme = np.where(npTotal == "게임")
    elif g_theme == "겨울":
        npTheme = np.where(npTotal == "겨울")
    elif g_theme == "항공여행":
        npTheme = np.where(npTotal == "항공여행")
    elif g_theme == "자율주행차":
        npTheme = np.where(npTotal == "자율주행차")
    elif g_theme == "인공지능":
        npTheme = np.where(npTotal == "인공지능")

    themeList = []
    print(npTheme)
    for stock in npTotal[npTheme[0], 0]:
        themeList.append(stock)

    print(themeList)
    return JsonResponse({'themeList' :themeList},status=200)

def radioStock(request) :
    global g_theme, g_stock, g_term, g_data
    global g_model, g_predictDate

    g_stock = request.POST.get('select_stock')
    print("종목 : " + g_stock)
    return JsonResponse({'stock' : g_stock}, status=200)

def radioTerm(request) :
    global g_theme, g_stock, g_term, g_data
    global g_model, g_predictDate

    g_term = request.POST.get('select_date')
    print("학습기간 : " + g_term)
    return JsonResponse({'term' : g_term}, status=200)

def radioData(request) :
    global g_theme, g_stock, g_term, g_data
    global g_model, g_predictDate

    g_data = request.POST.get('stock_kind')
    print("학습데이터 : " + g_data)
    return JsonResponse({'data' : g_data}, status=200)

def radioModel(request) :
    global g_theme, g_stock, g_term, g_data
    global g_model, g_predictDate

    g_model = request.POST.get('model')
    print("학습데이터 : " + g_model)
    return JsonResponse({'model' : g_model}, status=200)

def radioPredictDate(request) :
    global g_theme, g_stock, g_term, g_data
    global g_model, g_predictDate

    g_predictDate = request.POST.get('predictDate')
    print("예측일 : " + g_predictDate)
    return JsonResponse({'predictDate' : g_predictDate}, status=200)

class ChartAPIView(APIView):
    def get(self, request):
        global g_theme, g_stock, g_term, g_data, g_predictDate, g_model
        global mbTheme, mbStock, mbTerm, mbData
        global dfStock, xy, column, standardDate
        global pltsub, figure, canvas
        global btnSaveModel, btnSaveChart
        global modelName

        print("g_theme :",g_theme)
        print("g_stock :",g_stock)
        print("g_term :",g_term)
        print("g_data :",g_data)
        print("g_model :",g_model)
        print("g_predictDate :", g_predictDate)

        # 학습 인자들 선언 및 초기화
        predictDate, seqLength, hidden, unit, epoch, batch = 0, 0, 0, 0, 0, 0

        # 선택된 데이터에 해당하는 컬럼을 리스트로 저장
        if g_data == "주가":
            column = ['Open', 'High', 'Low', 'Close']
        elif g_data == "주가 + 이평선":
            column = ['Open', 'High', 'Low', 'Close', '5Days', '10Days', '20Days', '60Days', '120Days']
        elif g_data == "주가 + 뉴스":
            column = ['Open', 'High', 'Low', 'Close', 'Escore']
        elif g_data == "주가 + 이평선 + 뉴스":
            column = ['Open', 'High', 'Low', 'Close', '5Days', '10Days', '20Days', '60Days', '120Days', 'Escore']
        elif g_data == "뉴스":
            column = ['Escore', 'Close']
        elif g_data == "주가 + 거래량":
            column = ['Open', 'High', 'Low', 'Close', 'Volume']
        elif g_data == "주가 + 거래량 + 이평선":
            column = ['Open', 'High', 'Low', 'Close', 'Volume', '5Days', '10Days', '20Days', '60Days', '120Days']
        elif g_data == "주가 + 거래량 + 이평선 + 뉴스":
            column = ['Open', 'High', 'Low', 'Close', 'Volume', '5Days', '10Days', '20Days', '60Days', '120Days',
                      'Escore']

        # 선택된 종목 csv파일을 열고
        # 선택된 종목, 기간, 데이터에 해당하는 컬럼을 numpy ndarray로 저장
        dfStock = openCSV(g_stock)
        date = dfStock['Date'].to_numpy()
        dfStock = dfStock.set_index('Date')
        dfStock = dfStock[g_term:]
        xy = dfStock[column].to_numpy(np.float64)


        if g_data != "뉴스":
            xy = np.c_[xy, xy[:, [3]]]

        # 모델명 설정 및 학습 인자 설정
        modelName = g_stock + '-' + g_model

        if g_predictDate == '1일':
            modelName = modelName + '5to1d-'
            predictDate, seqLength, hidden, unit, epoch, batch = 1, 5, 0, 20, 100, 32
            tmpLabel = '1'
        elif g_predictDate == '5일':
            modelName = modelName + '20to5d-'
            predictDate, seqLength, hidden, unit, epoch, batch = 5, 20, 0, 20, 100, 32
            tmpLabel = '5'
        elif g_predictDate == '20일':
            modelName = modelName + '60to20d-'
            predictDate, seqLength, hidden, unit, epoch, batch = 20, 60, 0, 80, 100, 32
            tmpLabel = '20'
        elif g_predictDate == '60일':
            modelName = modelName + '180to60d-'
            predictDate, seqLength, hidden, unit, epoch, batch = 60, 180, 0, 40, 60, 128
            tmpLabel = '60'

        modelName = modelName + standardDate
        date = date[-(seqLength + predictDate):]

        if g_data == "주가":
            modelName = modelName + '(Stock)'
        elif g_data == "주가 + 이평선":
            modelName = modelName + '(Stock, MA)'
        elif g_data == "주가 + 뉴스":
            modelName = modelName + '(Stock, Emo)'
        elif g_data == "주가 + 이평선 + 뉴스":
            modelName = modelName + '(Stock, MA, Emo)'
        elif g_data == "뉴스":
            modelName = modelName + '(Emo)'
        elif g_data == "주가 + 거래량":
            modelName = modelName + '(Stock, Vol)'
        elif g_data == "주가 + 거래량 + 이평선":
            modelName = modelName + '(Stock, Vol, MA)'
        elif g_data == "주가 + 거래량 + 이평선 + 뉴스":
            modelName = modelName + '(Stock, Vol, MA, Emo)'

        print("modelName :",modelName)

        # 모델 학습
        model, res = getModel(xy, predictDate, seqLength, modelName, hidden, unit, epoch, batch)

        # 그래프에 출력될 최근 실제 주가
        xy2 = xy[-(seqLength + predictDate):]

        # 예측가 1
        scal = MinMaxScaler(xy2[:, :-1])
        testX = getX(scal[:-predictDate], seqLength)
        predictVal1 = getPredict(model, testX, xy2[:, :-1])
        predictVal1 = np.append(xy2[:-predictDate, [-1]], predictVal1)

        # 예측가 2
        testX2 = getX(scal[predictDate:], seqLength)
        predictVal2 = getPredict(model, testX2, xy2[predictDate:, :-1])

        actList = []
        pre1List = []
        pre2List = []

        i = 0
        for d in date:
            actList.append([time.mktime(datetime.datetime.strptime(d, "%Y-%m-%d").timetuple()) * 1000 , xy2[:, [-1]].reshape(-1).tolist()[i]])
            pre1List.append([time.mktime(datetime.datetime.strptime(d, "%Y-%m-%d").timetuple()) * 1000 , round(predictVal1.tolist()[i])])
            pre2List.append([time.mktime(datetime.datetime.strptime(d, "%Y-%m-%d").timetuple()) * 1000 , xy2[:, [-1]].reshape(-1).tolist()[i]])
            i = i + 1

        today = date[-1]
        i = 1
        for pre in predictVal2:
            pre2List.append([time.mktime((datetime.datetime.strptime(today, "%Y-%m-%d").date() + datetime.timedelta(days = i)).timetuple()) * 1000 , round(pre)])
            i = i + 1

        print(actList)
        print(pre1List)
        print(pre2List)

        data = {
            'select_stock': g_stock,
            'modelName': modelName,
            'predictDate' : g_predictDate,
            'actual': actList,
            'predict1': pre1List,
            'predict2': pre2List,
            'loss': str(res[0]),
            'mae': str(res[1]),
        }

        return HttpResponse(json.dumps(data), content_type='text/json')

# class ChartView(View):
#     def get(self, request, *args, **kwargs):
#         print("request: ", request)
#         return render(request, 'project_bigdata/templates/Simulator.html')

def saveModel(request):
    file_path = os.path.join(modelPath, modelName + '.h5')
    print(file_path)
    file_name = urllib.parse.quote(modelName.encode('utf-8'))
    print(file_name)

    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/force-download")
        response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % file_name

        return response

    raise Http404


def syncData(request):
    print("syncData()")
    updateStockCSV()
    updateThemeCSV()
    data = {
        'return': 'ok'
    }
    return HttpResponse(json.dumps(data), content_type='text/json')