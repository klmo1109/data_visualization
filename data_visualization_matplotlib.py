# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 14:01:04 2020

@author: E0090
"""

import pandas as pd
import cx_Oracle
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import seaborn as sns
from datetime import datetime
import matplotlib.ticker as mtick
import matplotlib.ticker as ticker
from matplotlib.font_manager import FontProperties 

font = FontProperties(fname='C:/Users/E0090/Anaconda3/Lib/site-packages/matplotlib/mpl-data/fonts/ttf/TaipeiSansTCBeta-Bold.ttf')
matplotlib.rcParams['axes.unicode_minus']=False

###get data from SQL
passw = "XXXX" 
user= "XXXX"
db = cx_Oracle.connect(user, passw, 'xx.xxx.x.xxx:xxx/SERVER1')
printHeader = True
cursor = db.cursor()
sql = "select * from tab" # get a list of all tables
cursor.execute (sql)



### save data to csv
results = pd.read_sql(sql,db)
data = pd.read_sql("SELECT * FROM THISDATA",db)
base = pd.read_sql("SELECT * FROM THISBASE",db)
db.close
data_csv = data.to_csv("C:/Users/E0090/Downloads/this_data.csv")
base_csv = base.to_csv("C:/Users/E0090/Downloads/this_base.csv")


base_dict= pd.Series(base.THIS_NAME.values,index=base.THIS_CODE).to_dict()
code = ["THIS007","THIS003","THIS018","THIS050","THIS053","THIS058","THIS011"]
THIS_CODE = data.groupby("THIS_CODE")


### 視覺化資料 
def ani_plot(b) : 
    name = base_dict.get(b)
    f = THIS_CODE.get_group(b)
    
    #先分類資料 (XY)
    x = sorted (f["YYMM"],reverse=False) #tolist()
    y = sorted (f["THIS_DATA"],reverse=False,key = lambda x: (len (x), x))
    
    
    #x 轉成日期
    x_date =[]
    for x1 in x:
        x2 = int(x1) + 191100
        x_time= datetime.strptime(str(x2),"%Y%m")
        x_date.append(x_time)
    x_max = max(x_date)
    x_min = min(x_date)

    
    
    # Y 軸 
    y_list = [] #值
    y_loc = [] #max
    y_show = [] #刻度 str
    for y1 in y:
        #print(y1)
        if "%" in y1 :
            y_list.append((float(y1.replace("%"," ")))*100/10000)
            y_show.append(str(y1))
            if max(y_list) <= 1 :
                y_loc = 1
            else:
                y_loc = (max(y_list))
        else:
            y_list.append(np.around(float(y1)))
            if max(y_list) % 5 == 0:
                y_loc = (max(y_list))
            else :
                y_loc = (max(y_list) + (5+(max(y_list)% 5)))

    fig1=plt.figure(figsize = (20,10))
    if y_loc == 1 :
        ax1 = plt.axes(xlim=(x_min,x_max),ylim=(0,max(y_list)))
        ax1.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1))

    else:
        ax1 = plt.axes(xlim=(x_min,x_max),ylim=(min(y_list),y_loc))
    
    line, = ax1.plot([], [], lw=2)
    plt.tick_params(axis='x', labelsize=20)
    plt.tick_params(axis='y', labelsize=20)
    plt.style.use('seaborn')
    
    plt.xlabel("日期", fontproperties=font,fontsize = 30)
    plt.ylabel("  ", fontproperties=font,fontsize = 30)
    plt.title (name, fontproperties=font,fontsize = 30,loc = "left",)

    writer = animation.FFMpegFileWriter(fps=15, metadata=dict(artist='Me'), bitrate=1800)

    #以上 XY座標以解決
    def init():
        line.set_data([], [])
        return line,
    
    #給予 line 內容
    def animate(i):
        line.set_data(x_date[:i], y_list[:i])
        return line,

    
    ani = FuncAnimation(fig1, animate, init_func=init, frames=len(x_date),  
                        interval=50, blit=True)
    ani.save(str(b)+".mp4",writer =writer, dpi=100)
    plt.savefig(str(b),dpi = 300 ,bbox_inches='tight')
    




for code_co in base["THIS_CODE"]:
    ani_plot(code_co)










