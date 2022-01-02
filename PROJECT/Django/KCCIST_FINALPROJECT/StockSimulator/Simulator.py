from StockSimulator.Stock import *

from tkinter.filedialog import *
from tkinter.simpledialog import *
from tkinter import *

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.font_manager as fm
import pandas as pd
import numpy as np

modlePath = './models'
csvPath = './csv'
fontPath = './NanumFontSetup_TTF_SQUARE'
fontLight = fm.FontProperties(fname=fontPath + '/NanumSquareL.ttf', size=18)
fontBold = fm.FontProperties(fname=fontPath + '/NanumSquareB.ttf', size=18)

Simulator = Tk()
figure = plt.Figure()
pltsub = figure.add_subplot()
canvas = None

frame1, frame2, frame3, frame4 = None, None, None, None
lbTheme, lbStock, lbTerm, lbData = None, None, None, None
mbTheme, mbStock, mbTerm, mbData = None, None, None, None
btnSaveModel, btnSaveChart = None, None

g_theme, g_stock, g_term, g_data = StringVar(), StringVar(), StringVar(), StringVar()
g_model, g_predictDate = StringVar(), StringVar()
g_theme.set('테마 선택')
g_stock.set('종목 선택')
g_term.set('학습 기간 선택')
g_data.set('학습 데이터 선택')
g_model.set('RNN')
g_predictDate.set('1일')

dfStock = []
xy = []
column = []
standardDate = ""
modelName = ""

def openCSV(filename):
    if 'Total' in filename:
        df_price = pd.read_csv(os.path.join(csvPath, filename + '.csv'), encoding='euc-kr')
    else:
        df_price = pd.read_csv(os.path.join(csvPath, filename + '.csv'), encoding='utf-8')
    return df_price

def radioTheme() :
    global g_theme, g_stock, g_term, g_data
    global mbTheme, mbStock, mbTerm, mbData

    # 테마 재선택 시 종목명, 기간, 데이터 전부 초기화
    g_stock.set('종목 선택')
    g_term.set('학습 기간 선택')
    g_data.set('학습 데이터 선택')
    mbStock['state'] = DISABLED
    mbTerm['state'] = DISABLED
    mbData['state'] = DISABLED
    btnTrain['state'] = DISABLED

    # 선택된 테마에 해당되는 종목을 'Total.csv'에서 찾아 종목리스트에 출력
    dfTotal = openCSV('Total')
    npTotal = dfTotal.to_numpy()
    npTheme = []


    if g_theme.get() == "게임":
        npTheme = np.where(npTotal == "게임")
    elif g_theme.get() == "겨울":
        npTheme = np.where(npTotal == "겨울")
    elif g_theme.get() == "항공여행":
        npTheme = np.where(npTotal == "항공여행")
    elif g_theme.get() == "자율주행차":
        npTheme = np.where(npTotal == "자율주행차")
    elif g_theme.get() == "인공지능":
        npTheme = np.where(npTotal == "인공지능")

    mbStock.menu = Menu(mbStock, tearoff=0, bg='#AFFFFF')
    mbStock["menu"] = mbStock.menu
    for stock in npTotal[npTheme[0], 0]:
        mbStock.menu.add_radiobutton(label=stock, value=stock, variable=g_stock, command=radioStock)

    # 종목 선택 버튼 켜기
    mbStock['state'] = NORMAL

def radioStock() :
    global g_theme, g_stock, g_term, g_data
    global mbTheme, mbStock, mbTerm, mbData
    global dfStock

    # 기간 선택 버튼 켜기
    mbTerm['state'] = NORMAL

def radioTerm() :
    global g_theme, g_stock, g_term, g_data
    global mbTheme, mbStock, mbTerm, mbData
    global standardDate

    # 선택된 기간을 standardDate에 저장
    if g_term.get() == "2017년 부터":
        standardDate = "2017"
    elif g_term.get() == "2018년 부터":
        standardDate = "2018"
    elif g_term.get() == "2019년 부터":
        standardDate = "2019"
    elif g_term.get() == "2020년 부터":
        standardDate = "2020"

    # 데이터 선택 버튼 켜기
    mbData['state'] = NORMAL

def radioData() :
    global g_theme, g_stock, g_term, g_data
    global mbTheme, mbStock, mbTerm, mbData
    global column

    # 선택된 데이터에 해당하는 컬럼을 리스트로 저장
    if g_data.get() == "주가":
        column = ['Open', 'High', 'Low', 'Close']
    elif g_data.get() == "주가 + 이평선":
        column = ['Open', 'High', 'Low', 'Close', '5Days', '10Days', '20Days', '60Days', '120Days']
    elif g_data.get() == "주가 + 뉴스":
        column = ['Open', 'High', 'Low', 'Close', 'Escore']
    elif g_data.get() == "주가 + 이평선 + 뉴스":
        column = ['Open', 'High', 'Low', 'Close', '5Days', '10Days', '20Days', '60Days', '120Days', 'Escore']
    elif g_data.get() == "뉴스":
        column = ['Escore', 'Close']
    elif g_data.get() == "주가 + 거래량":
        column = ['Open', 'High', 'Low', 'Close', 'Volume']
    elif g_data.get() == "주가 + 거래량 + 이평선":
        column = ['Open', 'High', 'Low', 'Close', 'Volume', '5Days', '10Days', '20Days', '60Days', '120Days']
    elif g_data.get() == "주가 + 거래량 + 이평선 + 뉴스":
        column = ['Open', 'High', 'Low', 'Close', 'Volume', '5Days', '10Days', '20Days', '60Days', '120Days', 'Escore']

    # 학습 실행 버튼 켜기
    btnTrain['state'] = NORMAL

def clkTrain() :
    global g_theme, g_stock, g_term, g_data, g_predictDate, g_model
    global mbTheme, mbStock, mbTerm, mbData
    global dfStock, xy, column, standardDate
    global pltsub, figure, canvas
    global btnSaveModel, btnSaveChart
    global modelName

    # 학습 인자들 선언 및 초기화
    predictDate, seqLength, hidden, unit, epoch, batch = 0, 0, 0, 0, 0, 0
    tmpLabel = ''
    # 선택된 종목 csv파일을 열고
    # 선택된 종목, 기간, 데이터에 해당하는 컬럼을 numpy ndarray로 저장
    dfStock = openCSV(g_stock.get())
    dfStock = dfStock.set_index('Date')
    dfStock = dfStock[standardDate:]
    xy = dfStock[column].to_numpy(np.float64)

    if g_data.get() != "뉴스":
        xy = np.c_[xy, xy[:, [3]]]

    # 모델명 설정 및 학습 인자 설정
    modelName = g_stock.get() + '-' + g_model.get()

    if g_predictDate.get() == '1일':
        modelName = modelName + '5to1d-'
        predictDate, seqLength, hidden, unit, epoch, batch = 1, 5, 0, 20, 100, 32
        tmpLabel = '1'
    elif g_predictDate.get() == '5일':
        modelName = modelName + '20to5d-'
        predictDate, seqLength, hidden, unit, epoch, batch = 5, 20, 0, 20, 100, 32
        tmpLabel = '5'
    elif g_predictDate.get() == '20일':
        modelName = modelName + '60to20d-'
        predictDate, seqLength, hidden, unit, epoch, batch = 20, 60, 0, 80, 100, 32
        tmpLabel = '20'
    elif g_predictDate.get() == '60일':
        modelName = modelName + '180to60d-'
        predictDate, seqLength, hidden, unit, epoch, batch = 60, 180, 0, 40, 60, 128
        tmpLabel = '60'

    modelName = modelName + standardDate

    if g_data.get() == "주가":
        modelName = modelName + '(Stock)'
    elif g_data.get() == "주가 + 이평선":
        modelName = modelName + '(Stock, MA)'
    elif g_data.get() == "주가 + 뉴스":
        modelName = modelName + '(Stock, Emo)'
    elif g_data.get() == "주가 + 이평선 + 뉴스":
        modelName = modelName + '(Stock, MA, Emo)'
    elif g_data.get() == "뉴스":
        modelName = modelName + '(Emo)'
    elif g_data.get() == "주가 + 거래량":
        modelName = modelName + '(Stock, Vol)'
    elif g_data.get() == "주가 + 거래량 + 이평선":
        modelName = modelName + '(Stock, Vol, MA)'
    elif g_data.get() == "주가 + 거래량 + 이평선 + 뉴스":
        modelName = modelName + '(Stock, Vol, MA, Emo)'

    print(modelName)

    # 모델 학습
    model, res = getModel(xy, predictDate, seqLength, modelName, hidden, unit, epoch, batch)

    # 그래프에 출력될 최근 실제 주가
    xy2 = xy[-(seqLength + predictDate):]

    # 예측가 1
    scal = MinMaxScaler(xy2[:, :-1])
    testX = getX(scal[:-predictDate], seqLength)
    predictVal1 = getPredict(model, testX, xy2[:, :-1])
    predictVal1 = np.append(xy2[:-predictDate, [-1]], predictVal1)
    print(predictVal1)

    # 예측가 2
    testX2 = getX(scal[predictDate:], seqLength)
    predictVal2 = getPredict(model, testX2, xy2[predictDate:,:-1])
    predictVal2 = np.append(xy2[:,[-1]], predictVal2)
    print(predictVal2)

    # 차트 초기화
    pltsub.clear()
    canvas.get_tk_widget().pack_forget()
    btnSaveModel.pack_forget()
    btnSaveChart.pack_forget()

    # 차트 출력
    canvas = FigureCanvasTkAgg(figure, frame4)
    canvas.get_tk_widget().pack(side=TOP)
    pltsub = figure.add_subplot()
    pltsub.plot(predictVal2, label=tmpLabel + "days predict")
    pltsub.plot(predictVal1, label="last " + tmpLabel + "days predict")
    pltsub.plot(xy2[:, [-1]], label="actual stock")
    pltsub.set_xlabel('날짜', fontproperties=fontLight)
    pltsub.set_ylabel('종가', fontproperties=fontLight)
    pltsub.text(0, np.min(predictVal2), 'loss: ' + str(res[0]) + '   mae: ' + str(res[1]))
    #print(np.min(predictVal2))
    pltsub.legend(prop={'size': 10}, loc='best')
    pltsub.set_title(g_stock.get(), fontproperties=fontBold)

    # 저장 버튼
    btnSaveModel = Button(frame4, text='모델 저장', fg='black', bd=3, bg='#3FFFFF', command=saveModel)
    btnSaveModel.pack(side='right', ipadx=20, ipady=10, padx=10)

    btnSaveChart = Button(frame4, text='차트 저장', fg='black', bd=3, bg='#3FFFFF', command=saveChart)
    btnSaveChart.pack(side='right', ipadx=20, ipady=10)


    # plt.figure()
    # plt.plot(predictVal2, label="5days predict")
    # plt.plot(predictVal1, label="last 5days predict")
    # plt.plot(xy2[:, [-1]], label="actual stock")
    # plt.xlabel('date')
    # plt.ylabel('price')
    # plt.legend(prop={'size': 10}, loc='best')
    # plt.show()

def syncData():
    updateStockCSV()
    updateThemeCSV()

def saveChart():
    global pltsub, figure, canvas
    if modelName == '' or modelName == None:
        return

    saveFp = asksaveasfile(mode='wb', defaultextension='*.png',
                           filetypes=(("그림 파일", "*.png;*.jpg;*.bmp;*.tif"), ('All File', '*.*')), initialfile=modelName)

    if saveFp == '' or saveFp == None:
        return

    figure.savefig(saveFp.name)

def saveModel():
    if modelName == '' or modelName == None:
        return

    saveFp = asksaveasfile(mode='wb', defaultextension='*.h5',
                           filetypes=(("모델 파일", "*.h5"), ('All File', '*.*')), initialfile=modelName)

    if saveFp == '' or saveFp == None:
        return

    model = keras.models.load_model(modlePath + '/' + modelName + '.h5')
    model.save(saveFp.name)

if __name__ == '__main__' :
    Simulator.title("Stock Simulator Ver 1.0")
    Simulator.geometry('1080x600')
    Simulator.resizable(height=False, width=True)
    Simulator.configure(bg='#CFFFFF')

    ## 데이터 설정 프레임
    frame1 = Frame(Simulator, relief=SUNKEN, background="#CFFFFF", bd=2)
    frame1.pack(side="left", fill="both")

    ## 테마 선택
    lbTheme = Label(frame1, relief='flat', bd=1, bg='#AFFFFF', textvariable=g_theme)
    lbTheme.pack(side='top', fill='x', ipady=20)
    mbTheme = Menubutton(frame1, relief='raised', bd=1, text='▼', cursor='hand2', bg='#AFFFFF')
    mbTheme.pack(side='top', fill='x')
    mbTheme.menu = Menu(mbTheme, tearoff=0, bg='#AFFFFF')
    mbTheme["menu"] = mbTheme.menu
    mbTheme.menu.add_radiobutton(label="게임", value='게임', variable=g_theme, command=radioTheme)
    mbTheme.menu.add_radiobutton(label="겨울", value='겨울', variable=g_theme, command=radioTheme)
    mbTheme.menu.add_radiobutton(label="인공지능", value='인공지능', variable=g_theme, command=radioTheme)
    mbTheme.menu.add_radiobutton(label="자율주행차", value='자율주행차', variable=g_theme, command=radioTheme)
    mbTheme.menu.add_radiobutton(label="항공여행", value='항공여행', variable=g_theme, command=radioTheme)

    ## 종목 선택
    lbStock = Label(frame1, relief='flat', bd=1, bg='#AFFFFF', textvariable=g_stock)
    lbStock.pack(side='top', fill='x', ipady=20)
    mbStock=Menubutton(frame1, relief='raised', bd=1, text='▼', cursor='hand2', bg='#AFFFFF', state=DISABLED)
    mbStock.pack(side='top', fill='x')

    ## 학습기간 선택
    lbTerm = Label(frame1, relief='flat', bd=1, bg='#AFFFFF', textvariable=g_term)
    lbTerm.pack(side='top', fill='x', ipady=20)
    mbTerm=Menubutton(frame1, relief='raised', bd=1, text='▼', cursor='hand2', bg='#AFFFFF', state=DISABLED)
    mbTerm.pack(side='top', fill='x')
    mbTerm.menu = Menu(mbTerm, tearoff=0, bg='#AFFFFF')
    mbTerm["menu"] = mbTerm.menu
    mbTerm.menu.add_radiobutton(label="2017년 부터", value='2017년 부터', variable=g_term, command=radioTerm)
    mbTerm.menu.add_radiobutton(label="2018년 부터", value='2018년 부터', variable=g_term, command=radioTerm)
    mbTerm.menu.add_radiobutton(label="2019년 부터", value='2019년 부터', variable=g_term, command=radioTerm)
    mbTerm.menu.add_radiobutton(label="2020년 부터", value='2020년 부터', variable=g_term, command=radioTerm)

    ## 학습데이터 선택
    lbData = Label(frame1, relief='flat', bd=1, bg='#AFFFFF', textvariable=g_data)
    lbData.pack(side='top', ipadx=30, ipady=20)
    mbData=Menubutton(frame1, relief='raised', bd=1, text='▼', cursor='hand2', bg='#AFFFFF', state=DISABLED)
    mbData.pack(side='top', fill='x')
    mbData.menu = Menu(mbData, tearoff=0, bg='#AFFFFF')
    mbData["menu"] = mbData.menu
    mbData.menu.add_radiobutton(label="시가, 고가, 저가, 종가", value='주가', variable=g_data, command=radioData)
    mbData.menu.add_radiobutton(label="시가, 고가, 저가, 종가, 이동평균선", value='주가 + 이평선', variable=g_data, command=radioData)
    mbData.menu.add_radiobutton(label="시가, 고가, 저가, 종가, 뉴스", value='주가 + 뉴스', variable=g_data, command=radioData)
    mbData.menu.add_radiobutton(label="시가, 고가, 저가, 종가, 이동평균선, 뉴스", value='주가 + 이평선 + 뉴스', variable=g_data, command=radioData)
    mbData.menu.add_radiobutton(label="뉴스", value='뉴스', variable=g_data, command=radioData)
    mbData.menu.add_radiobutton(label="시가, 고가, 저가, 종가, 거래량", value='주가 + 거래량', variable=g_data, command=radioData)
    mbData.menu.add_radiobutton(label="시가, 고가, 저가, 종가, 거래량, 이동평균선", value='주가 + 거래량 + 이평선', variable=g_data, command=radioData)
    mbData.menu.add_radiobutton(label="시가, 고가, 저가, 종가, 거래량, 이동평균선, 뉴스", value='주가 + 거래량 + 이평선 + 뉴스', variable=g_data, command=radioData)

    ## 동기화 버튼
    btnSync = Button(frame1, text='데이터 동기화', fg='black', bd=3, bg='#AFFFFF', command=syncData)
    btnSync.pack(side=BOTTOM, fill='x', padx=10, pady=10, ipady=20)


    ### 모델 설정 프레임
    frame2 = Frame(Simulator, relief=SUNKEN, background="#CFFFFF", bd=2)
    frame2.pack(side="left", fill="both")

    lbModel = Label(frame2, relief='groove', bd=1, text = '모델 선택', bg='#AFFFFF')
    lbModel.pack(side='top', fill='x', ipadx=30, ipady=20, padx=20, pady=20)

    radioModel1 = tkinter.Radiobutton(frame2, text="RNN", value="RNN", variable=g_model, bg="#CFFFFF")
    radioModel1.pack(side="top", ipady=20)

    radioModel2 = tkinter.Radiobutton(frame2, text="LSTM", value="LSTM", variable=g_model, bg="#CFFFFF")
    radioModel2.pack(side="top", ipady=20)

    radioModel3 = tkinter.Radiobutton(frame2, text="양방향 LSTM", value="양방향 LSTM", variable=g_model, bg="#CFFFFF")
    radioModel3.pack(side="top", ipady=20)

    radioModel4 = tkinter.Radiobutton(frame2, text="GRU", value="GRU", variable=g_model, bg="#CFFFFF")
    radioModel4.pack(side="top", ipady=20)


    ### 예측 기간 설정 프레임
    frame3 = Frame(Simulator, relief=SUNKEN, background="#CFFFFF", bd=2)
    frame3.pack(side="left", fill="both")

    lbModel = Label(frame3, relief='groove', bd=1, text = '예측 기간 선택', bg='#AFFFFF')
    lbModel.pack(side='top', fill='x', ipadx=15, ipady=20, padx=20, pady=20)

    radioDate1 = tkinter.Radiobutton(frame3, text="1일", value="1일", variable=g_predictDate, bg="#CFFFFF")
    radioDate1.pack(side="top", ipady=20)

    radioDate2 = tkinter.Radiobutton(frame3, text="5일", value="5일", variable=g_predictDate, bg="#CFFFFF")
    radioDate2.pack(side="top", ipady=20)

    radioDate3 = tkinter.Radiobutton(frame3, text="20일", value="20일", variable=g_predictDate, bg="#CFFFFF")
    radioDate3.pack(side="top", ipady=20)

    radioDate4 = tkinter.Radiobutton(frame3, text="60일", value="60일", variable=g_predictDate, bg="#CFFFFF")
    radioDate4.pack(side="top", ipady=20)

    ## 학습 버튼
    btnTrain = Button(frame3, text='학습 실행', fg='black', bd=3, bg='#3FFFFF', state=DISABLED, command=clkTrain)
    btnTrain.pack(side='bottom', fill='x', ipady=20, padx=10, pady=10)


    ### 차트 출력 프레임
    frame4 = Frame(Simulator, relief=SUNKEN, background="#CFFFFF", bd=2)
    frame4.pack(side="left", fill="both")

    # 차트 출력
    canvas = FigureCanvasTkAgg(figure, frame4)
    canvas.get_tk_widget().pack(side=TOP)

    ## 저장 버튼
    btnSaveModel = Button(frame4, text='모델 저장', fg='black', bd=3, bg='#3FFFFF', state=DISABLED)
    btnSaveModel.pack(side='right', ipadx=20, ipady=10, padx=10)

    btnSaveChart = Button(frame4, text='차트 저장', fg='black', bd=3, bg='#3FFFFF', state=DISABLED)
    btnSaveChart.pack(side='right', ipadx=20, ipady=10)

    Simulator.mainloop()