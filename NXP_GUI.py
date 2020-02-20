import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3d
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import datetime as dt
import time
import PySimpleGUIQt as qt
import tkinter as tk
from tkinter import ttk
from ni845x18October2019 import NI845x
import openpyxl as xl

LARGE_FONT = ("Verdana", 12)


class TKApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.resizable(True, True)
        tk.Tk.iconbitmap(self, default="RadioIcon.ico")
        tk.Tk.wm_title(self, "LUT Handler")
        self.fig = Figure(figsize=(5,5), dpi=100)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # label = tk.Label(container, text="Graph Page!", font=LARGE_FONT)
        # label.pack(pady=10, padx=10)
        f = self.fig
        self.canvas = FigureCanvasTkAgg(f, container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, container)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar.pack()

        self.ax = self.fig.add_subplot(121, projection='polar')
        self.ax2 = self.fig.add_subplot(122, projection='3d')
        self.line, = self.ax.plot([], [])
        self.plot = 0

        self.GuiElements()
        self.create_3d()


    def GuiElements(self):
        self.DeviceSwitch =0
        self.canvas2 = tk.Canvas(self, width=70, height=70)
        self.canvas2.pack()
        self.canvas2.create_oval(5, 5, 70, 70, fill='grey', tags='DeviceSwitch')
        self.canvas2.place(x=22, y=30)
        self.canvas2.tag_bind('DeviceSwitch', '<Button-1>', self.clicked)

        self.button1 = tk.Button(self, text="Create 3D", command=lambda: self.create_3d(), width = 30, height =2 )
        self.button1.configure(foreground = 'blue')
        self.button1.pack()
        self.button1.place(x=1100, y=30)

        self.button2 = tk.Button(self, text="Write to File", command=lambda: self.Write_LUT(),width =30, height=2)
        self.button2.configure(foreground = 'green')
        self.button2.pack()
        self.button2.place(x=840, y=30)

        self.button3 = tk.Button(self, text="Upload LUT", command=lambda: self.Upload_LUT(), width=10, height=3)
        self.button3.configure(foreground='red')
        self.button3.pack()
        self.button3.place(x=1360, y=22)

        self.ModeLabel = ttk.Label(text="Mode", style="BW.TLabel")
        self.ModeLabel.pack()
        self.ModeLabel.place(x=210, y=30)
        self.mode = ttk.Combobox(self, values=["Tx","Rx","Tx & Rx both"], state='readonly')
        self.mode.pack()
        self.mode.place(x=250, y=30)
        self.mode.current(1)
        self.mode.bind("<<ComboboxSelected>>", self.ModeOrLUTRowChange)

        self.ModeLabel = ttk.Label(text="Lookup Table Row #", style="BW.TLabel")
        self.ModeLabel.pack()
        self.ModeLabel.place(x=133, y=50)
        self.LUTRow =ttk.Combobox(self,values= list(range(64)), state = 'readonly' )
        self.LUTRow.pack()
        self.LUTRow.place(x=250, y=50)
        self.LUTRow.current(0)
        self.LUTRow.bind("<<ComboboxSelected>>", self.ModeOrLUTRowChange)

        self.ThetaLabel = ttk.Label(text="Elevation\n      (θ)", style="BW.TLabel")
        self.ThetaLabel.pack()
        self.ThetaLabel.place(x=25, y=823)
        self.ThetaSlider = tk.Scale(self, from_=-90, to=90, length=650, command = self.find_phase_forTheta, orient = 'horizontal')
        self.ThetaSlider.pack()
        self.ThetaSlider.place(x=75, y=820)
        self.ThetaSlider.set(0)

        self.ThetaLabel = ttk.Label(text="Azimuth \n     (Φ)", style="BW.TLabel")
        self.ThetaLabel.pack()
        self.ThetaLabel.place(x=750, y=823)
        self.PhiSlider = tk.Scale(self, from_=0, to=180, length=650, command = self.find_phase_forTheta,  orient = 'horizontal')
        self.PhiSlider.pack()
        self.PhiSlider.place(x=800, y=820)
        self.PhiSlider.set(90)

        self.A1Label = ttk.Label(text="Antenna 1,2 --> phase", style="BW.TLabel")
        self.A1Label.pack()
        self.A1Label.place(x=400, y =30)
        self.A1Phase = tk.Entry(self)
        self.A1Phase.pack()
        self.A1Phase.place(x = 530, y =30)

        self.A2Label = ttk.Label(text="Antenna 3,4 --> phase", style="BW.TLabel")
        self.A2Label.pack()
        self.A2Label.place(x=400, y=50)
        self.A2Phase = tk.Entry(self)
        self.A2Phase.pack()
        self.A2Phase.place(x=530, y=50)

        self.A1GainLabel = ttk.Label(text="Gain", style="BW.TLabel")
        self.A1GainLabel.pack()
        self.A1GainLabel.place(x=660, y=30)
        self.A1Gains = ttk.Combobox(self, values=list(range(64)), state='readonly')
        self.A1Gains.pack()
        self.A1Gains.place(x=690, y=30)
        self.A1Gains.current(16)
        # self.A1Gains.bind("<<ComboboxSelected>>", self.LUTRowChange)

        self.A2GainLabel = ttk.Label(text="Gain", style="BW.TLabel")
        self.A2GainLabel.pack()
        self.A2GainLabel.place(x=660, y=50)
        self.A2Gains = ttk.Combobox(self, values=list(range(64)), state='readonly')
        self.A2Gains.pack()
        self.A2Gains.place(x=690, y=50)
        self.A2Gains.current(16)
        # self.A2Gains.bind("<<ComboboxSelected>>", self.LUTRowChange)

        self.Progress = tk.DoubleVar()
        self.progress = ttk.Progressbar(self, orient = 'horizontal', length = 1000, mode ='determinate', variable = self.Progress, maximum = 64)
        self.progress.pack()
        self.progress.place(x=200, y=500)
        self.progress.lower()


    def Upload_LUT(self):
        # self.device = NI845x()
        # if(self.device):
        #     self.progress.lift()
        #     self.device.Write_LUT(self.Progress)
        #     self.progress.lower()
        self.progress.lift()
        for i in range(64):
            self.Progress.set(float(i+1))
            self.update()
            time.sleep(.1)
        self.progress.lower()

    def clicked(self,x):
        if(self.DeviceSwitch ==0):
            self.DeviceSwitch = 1
            self.canvas2.itemconfigure('DeviceSwitch', fill = 'green')
        else:
            self.DeviceSwitch = 0
            self.canvas2.itemconfigure('DeviceSwitch', fill='grey')



    def ModeOrLUTRowChange(self,event):
        mode = int(self.mode.current())%2
        my_wb = xl.load_workbook("input_LUT.xlsx")
        Row = self.LUTRow.get()
        print(Row)
        my_sheet = my_wb.active
        if(mode==0): #TX
            X = int(my_sheet.cell(row=3 + int(Row), column=16+1).value)
            Y = int(my_sheet.cell(row=3 + int(Row), column=16+2).value)
        else:
            X = int(my_sheet.cell(row=3 + int(Row), column=16+3).value)
            Y = int(my_sheet.cell(row=3 + int(Row), column=16+4).value)
        self.ThetaSlider.set(X)
        self.PhiSlider.set(Y)

        # if (mode != 0):  # RX
        #     X = int(my_sheet.cell(row=3 + int(Row), column=1).value)
        #     Y = int(my_sheet.cell(row=3 + int(Row), column=9).value)
        # else:
        #     X = int(my_sheet.cell(row=3 + int(Row), column=3).value)
        #     Y = int(my_sheet.cell(row=3 + int(Row), column=11).value)
        # d = np.sqrt(8.3**2+5.3**2)/2000
        # u = 2*np.arctan(8.3/5.3)-np.pi/2
        # k = 2*np.pi/0.01070687
        # checkX, checkY =0,0
        #
        # X = X*5.625*np.pi/180
        # Y = Y * 5.625 * np.pi / 180
        # if(X > np.pi):
        #     X = X-2*np.pi
        #     checkX=1
        # if(Y>np.pi):
        #     Y = Y-2*np.pi
        #     checkY=1
        # if(Y ==0 and X==0):
        #     t=0
        #     p =  np.pi/2
        # elif(X == 0):
        #     p=u
        #     t = np.arcsin(Y/(k*d*np.cos(p-u)))
        #     print(p)
        #     print(t)
        # elif Y==0:
        #     p = np.pi/2
        #     t= np.arcsin(X/(k*d*np.sin(p)))
        #     print(p)
        #     print(t)
        # else:
        #     p = np.arctan(np.cos(u)/(Y/X-np.sin(u)))
        #     if(p<0):
        #         p = p+np.pi
        #         t = np.arcsin(Y / (k * d * np.cos(p - u)))
        #         print(p)
        #         print(t)
        #         print("p -ve")
        #     else:
        #         t = np.arcsin(Y / (k * d * np.cos(p - u)))
        #         print(p)
        #         print(t)
        # self.ThetaSlider.set(round(t*180/np.pi))
        # self.PhiSlider.set(round(p*180/np.pi))




    def Write_LUT(self):
        my_wb = xl.load_workbook("input_LUT.xlsx")
        my_sheet = my_wb.active
        phases = []
        phases[0:1] = str(self.A1Phase.get())[:5].split(",")
        phases[2:3]= str(self.A2Phase.get())[:5].split(",")
        gains =[]
        gains[0:1] = [self.A1Gains.current(), self.A1Gains.current()]
        gains[2:3] = [self.A2Gains.current(),self.A2Gains.current()]
        Row = self.LUTRow.get()
        for ch in range(4):
            if(self.mode.get()=="Tx" or self.mode.current() == 2):
                c = my_sheet.cell(row=3 + int(Row), column=ch*4+3)
                c.value = phases[ch]
                c = my_sheet.cell(row=3 + int(Row), column=ch * 4 + 4)
                c.value = gains[ch]
                c = my_sheet.cell(row=3 + int(Row), column=16 + 1)
                c.value = str(self.ThetaSlider.get())
                c = my_sheet.cell(row=3 + int(Row), column=16 + 2)
                c.value = str(self.PhiSlider.get())
            if(self.mode.get()=="Rx" or self.mode.current() == 2):
                c = my_sheet.cell(row=3 + int(Row), column=ch * 4 + 1)
                c.value = phases[ch]
                c = my_sheet.cell(row=3 + int(Row), column=ch * 4 + 2)
                c.value = gains[ch]
                c = my_sheet.cell(row=3 + int(Row), column=16 + 3)
                c.value = str(self.ThetaSlider.get())
                c = my_sheet.cell(row=3 + int(Row), column=16 + 4)
                c.value = str(self.PhiSlider.get())
        my_wb.save("input_LUT.xlsx")
        self.LUTRow.current((int(self.LUTRow.current())+1)%64)
        self.ModeOrLUTRowChange(2)


    def find_phase_forTheta(self, val2):
        stepsize = 2 * np.pi / 64
        theta = np.linspace(-np.pi / 2, np.pi / 2, 180)
        t = float(self.ThetaSlider.get())
        lam = 0.01070687
        k = 2 * np.pi / lam
        dx = 5.3 / 2
        phase = 0
        dy = 8.3 / 2
        d = np.sqrt(dx ** 2 + dy ** 2) / 1000
        x = 2 * np.arctan(8.3 / 5.3) - np.pi / 2
        if(self.plot != 0):
            p = float(self.PhiSlider.get()) * np.pi / 180
        else:
            p = np.pi/2
        self.A2Phase["state"] = "normal"
        self.A1Phase["state"] = "normal"
        maxPhase = k * d * np.sin(t * np.pi / 180) * np.sin(p)
        YZPhase = round(maxPhase / stepsize) * stepsize
        self.A1Phase.delete(0, tk.END)
        if maxPhase <0:
            ch1phase = int(64-np.abs(round(maxPhase / stepsize)))%64
            ch2phase = int(abs(round(maxPhase / stepsize)))
        else:
            ch1phase = int(abs(round(maxPhase / stepsize)))
            ch2phase = int(64-np.abs(round(maxPhase / stepsize)))%64
        self.A1Phase.insert(0,str(ch1phase)+","+ str(ch2phase)+"  (±"+str(round(YZPhase,3))+" rad)")
        maxPhase = k * d * np.sin(t * np.pi / 180) * np.cos(p - x)
        XZPhase = round(maxPhase / stepsize) * stepsize
        self.A2Phase.delete(0, tk.END)
        if maxPhase < 0:
            ch3phase = int(64 - np.abs(round(maxPhase / stepsize))) % 64
            ch4phase = int(abs(round(maxPhase / stepsize)))
        else:
            ch3phase = int(abs(round(maxPhase / stepsize)))
            ch4phase = int(64 - np.abs(round(maxPhase / stepsize))) % 64
        self.A2Phase.insert(0, str(ch3phase) + "," + str(ch4phase) + "  (±" + str(round(XZPhase, 3)) + " rad)")
        self.A1Phase["state"] = "readonly"
        self.A2Phase["state"] = "readonly"
        s = 2.2 / 1000
        AF = (2 * np.cos(k * d * np.sin(theta) * np.sin(p) - YZPhase) + \
              2 * np.cos(k * d * np.sin(theta) * np.cos(p - x) - XZPhase)) * \
             (np.sqrt((np.sinc(.5 * k * s * np.sin(theta) * np.sin(p)) * np.cos(
                 k * s * np.sin(theta) * np.cos(p) / 2) * np.cos(p)) ** 2 + \
                      (np.sinc(.5 * k * s * np.sin(theta) * np.sin(p)) * np.cos(
                          k * s * np.sin(theta) * np.cos(p) / 2) * np.cos(theta) * np.sin(p)) ** 2))
        self.line.set_xdata(theta)
        self.line.set_ydata(np.absolute(AF) / 4)
        # self.text.set_text('Y-axis Phase difference= ' + str(2*round(XZPhase, 2)) + '\nX-axis Phase difference = ' + str(2*round(YZPhase, 2)))
        self.canvas.draw()

    def create_3d(self):
        stepsize = np.pi / 64
        if (self.plot != 0):
            self.plot.remove()
        t = self.ThetaSlider.get()
        lam = 0.01070687
        k = 2 * np.pi / lam
        dx = 5.3 / 2
        dy = 8.3 / 2
        d = np.sqrt(dx ** 2 + dy ** 2) / 1000
        x = 2 * np.arctan(8.3 / 5.3) - np.pi / 2
        p = float(self.PhiSlider.get()) * np.pi / 180
        maxPhase = k * d * np.sin(t * np.pi / 180) * np.sin(p)
        YZPhase = round(maxPhase / stepsize) * stepsize
        maxPhase = k * d * np.sin(t * np.pi / 180) * np.cos(p - x)
        XZPhase = round(maxPhase / stepsize) * stepsize
        theta = np.linspace(0 * -np.pi / 2, np.pi / 2, 40)
        phi = np.linspace(0, 2 * np.pi, 40)
        THETA, PHI = np.meshgrid(theta, phi)
        s = 2.2 / 1000
        AF = (2 * np.cos(k * d * np.sin(THETA) * np.sin(PHI) - YZPhase) + \
              2 * np.cos(k * d * np.sin(THETA) * np.cos(PHI - x) - XZPhase)) * \
             (np.sqrt((np.sinc(.5 * k * s * np.sin(THETA) * np.sin(PHI)) * np.cos(
                 k * s * np.sin(THETA) * np.cos(PHI) / 2) * np.cos(PHI)) ** 2 + \
                      (np.sinc(.5 * k * s * np.sin(THETA) * np.sin(PHI)) * np.cos(
                          k * s * np.sin(THETA) * np.cos(PHI) / 2) * np.cos(THETA) * np.sin(PHI)) ** 2))
        R = np.absolute(AF)
        X = R * np.sin(THETA) * np.cos(PHI)
        Y = R * np.sin(THETA) * np.sin(PHI)
        Z = R * np.cos(THETA)
        self.plot = self.ax2.plot_surface(
            X, Y, Z, rstride=1, cstride=1, cmap=plt.get_cmap('jet'),
            linewidth=0, antialiased=False, alpha=0.5)
        self.canvas.draw()


app = TKApplication()
app.mainloop()
