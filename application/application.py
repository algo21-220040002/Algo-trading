import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk

plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['lines.linewidth'] = 0.5


class application:
    def __init__(self):
        plt.ion()
        self.delay = 0.5
        self.ay = []
        self.by = []
        self.date=[]

    def gui(self):
        window = tk.Tk()
        window.title('GUI - echoes')
        window.geometry('200x200')

        def give():
            self.delay = float(e1.get())

        l1 = tk.Label(window, text='please enter the bar time')
        l1.pack()
        e1 = tk.Entry(window, width=15)
        e1.pack()
        b1 = tk.Button(window, text="change", command=give)
        b1.pack()
        b2 = tk.Button(window, text='quit', command=window.quit)
        b2.pack()
        window.mainloop()

    def plot(self,date, position, balance, cumreturn, sharpe, maxdd,hour_ret):
        plt.clf()
        plt.suptitle("GUI", fontsize=30)

        self.ay.append(balance)
        self.date.append(date)

        ax1 = plt.subplot(2, 1, 1)
        ax1.set_title('pnl')
        ax1.set_ylabel('net value', fontsize=10)
        ax1.plot(self.date,self.ay,'g-')
        plt.annotate('hour_ret:' + str(round(hour_ret, 3)), xy=(0.02, 0.95), xycoords='axes fraction', fontsize=12,
                     xytext=(0, 0), textcoords='offset points', ha='left', va='top')
        plt.annotate('cum_ret:' + str(round(cumreturn, 3)), xy=(0.02, 0.85), xycoords='axes fraction', fontsize=12,
                     xytext=(0, 0), textcoords='offset points', ha='left', va='top')
        plt.annotate('sharp ratio:' + str(round(sharpe, 3)), xy=(0.02, 0.75), xycoords='axes fraction', fontsize=12,
                     xytext=(0, 0), textcoords='offset points', ha='left', va='top')
        plt.annotate('maxdrawdown:' + str(round(maxdd, 3)), xy=(0.02, 0.65), xycoords='axes fraction', fontsize=12,
                     xytext=(0, 0), textcoords='offset points', ha='left', va='top')



        self.by.append(position)
        ax2 = plt.subplot(2, 1, 2)
        ax2.set_title('position')
        ax2.set_ylabel('num', fontsize=10)
        ax2.plot(self.date,self.by)
        plt.annotate('position:' + str(round(position, 2)), xy=(0.02, 0.95), xycoords='axes fraction', fontsize=12,
                     xytext=(0, 0), textcoords='offset points', ha='left', va='top')

        plt.pause(self.delay)  # 设置暂停时间，太快图表无法正常显示

    def __del__(self):
        plt.ioff()


def main():
    data = pd.read_excel('./net value.xlsx').set_index('Date')

    app1 = application()
    app1.gui()
    for i in range(len(data)):
        date=data.index[i]
        app1.plot(date,np.random.random(), data.iloc[i, 0], np.random.random(), np.random.random(), np.random.random())

if __name__=="__main__":
    main()







