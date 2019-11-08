import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import mpl_toolkits.mplot3d.axes3d as axes3d
from  ipywidgets import widgets

# Data:
mu = 1
e = 1
a = 1
c = 1

beta = np.linspace(0,360,64)
C = (mu*((e*a)**2)) / (16*(np.pi**2)*c)


fig = plt.figure()
ax = plt.subplot(121, projection ='polar')
ax2 = plt.subplot(122, projection = '3d')
line, = ax.plot([],[])

text = ax.text(0.0, 0.95, '', transform=ax.transAxes)
YZPhase = 0
XZPhase = 0
plot = 0


def find_phase_forTheta(t):
    global XZPhase
    global YZPhase
    stepsize = 2*np.pi/64
    theta = np.linspace(-np.pi/2,np.pi/2,180)
    t = samp.val
    lam = 0.01070687
    k = 2 * np.pi / lam
    dx =  5.3 / 2
    phase = 0
    dy =  8.3 / 2
    d = np.sqrt(dx ** 2 + dy ** 2)/1000
    x = 2 * np.arctan(8.3 / 5.3) - np.pi / 2
    p = samp2.val*np.pi/180
    maxPhase = 2*k*d*np.sin(t*np.pi/180) * np.sin(p)
    YZPhase = round(maxPhase/stepsize)*stepsize
    maxPhase = 2*k * d * np.sin(t*np.pi/180)*np.cos(p-x)
    XZPhase = round(maxPhase/stepsize)*stepsize
    AF = np.exp(1j * phase) * np.exp(1j * k * d * np.sin(theta) * np.sin(p)) + \
         np.exp(1j * YZPhase) * np.exp(-1j * k * d * np.sin(theta) * np.sin(p))  +\
         np.exp(1j * phase) * np.exp(1j * k * d * np.sin(theta)*np.cos(p-x))+ \
         np.exp(1j * XZPhase) * np.exp(-1j * k * d * np.sin(theta)*np.cos(p-x))
    line.set_xdata(theta)
    line.set_ydata(np.absolute(AF/4))
    text.set_text('XZPhase = ' + str(round(XZPhase,2))+'\nYZPhase = ' + str(round(YZPhase,2))+"\nfor Main lobet at Theta : "+str(round(t,2)))


def create_3d(*args, **kwargs ):
    global plot
    stepsize = np.pi/64
    if(plot !=0):
        plot.remove()
    t = samp.val
    lam = 0.01070687
    k = 2 * np.pi / lam
    dx = 5.3 / 2
    dy = 8.3 / 2
    d = np.sqrt(dx ** 2 + dy ** 2) / 1000
    x =2 * np.arctan(8.3 / 5.3) - np.pi / 2
    p = samp2.val * np.pi / 180
    maxPhase = 2 * k * d * np.sin(t * np.pi / 180) * np.sin(p)
    YZPhase = round(maxPhase/stepsize)*stepsize
    maxPhase = 2 * k * d * np.sin(t * np.pi / 180) * np.cos(p - x)
    XZPhase = round(maxPhase/stepsize)*stepsize
    phase = 0
    theta = np.linspace(0*-np.pi/2,np.pi/2,40)
    phi = np.linspace(0,2*np.pi,40)
    THETA ,PHI = np.meshgrid(theta,phi)
    AF = np.exp(1j * phase) * np.exp(1j * k * d * np.sin(THETA) * np.sin(PHI)) + \
         np.exp(1j * YZPhase) * np.exp(-1j * k * d * np.sin(THETA) * np.sin(PHI)) + \
         np.exp(1j * phase) * np.exp(1j * k * d * np.sin(THETA) * np.cos(PHI - x)) + \
         np.exp(1j * XZPhase) * np.exp(-1j * k * d * np.sin(THETA) * np.cos(PHI - x))
    R = np.absolute(AF)
    X = R * np.sin(THETA) * np.cos(PHI)
    Y = R * np.sin(THETA) * np.sin(PHI)
    Z = R * np.cos(THETA)
    # fig2 = plt2.figure()
    # ax2 = fig2.add_subplot(1, 2, 1, projection='3d')
    plot = ax2.plot_surface(
        X, Y, Z, rstride=1, cstride=1, cmap=plt.get_cmap('jet'),
        linewidth=0, antialiased=False, alpha=0.5)
    print("button clicked")
def SliderAndThetaUpdate(angle,*args, **kwargs):
    if (str(angle.inaxes)=="Axes(0.05,0.96;0.06x0.03)"):
        samp.set_val(75)
    elif  (str(angle.inaxes)=="Axes(0.05,0.91;0.06x0.03)"):
        samp.set_val(60)
    elif  (str(angle.inaxes)=="Axes(0.05,0.86;0.06x0.03)"):
        samp.set_val(45)
    elif  (str(angle.inaxes)=="Axes(0.05,0.81;0.06x0.03)"):
        samp.set_val(30)
    elif  (str(angle.inaxes)=="Axes(0.05,0.76;0.06x0.03)"):
        samp.set_val(15)
    elif  (str(angle.inaxes)=="Axes(0.05,0.71;0.06x0.03)"):
        samp.set_val(0)
    elif  (str(angle.inaxes)=="Axes(0.05,0.66;0.06x0.03)"):
        samp.set_val(-15)
    elif  (str(angle.inaxes)=="Axes(0.05,0.61;0.06x0.03)"):
        samp.set_val(-30)
    elif  (str(angle.inaxes)=="Axes(0.05,0.56;0.06x0.03)"):
        samp.set_val(-45)
    elif  (str(angle.inaxes)=="Axes(0.05,0.51;0.06x0.03)"):
        samp.set_val(-60)
    elif  (str(angle.inaxes)=="Axes(0.05,0.45;0.06x0.03)"):
        samp.set_val(-75)

def SliderAndPhiUpdate(angle,*args, **kwargs):
    if (str(angle.inaxes)=="Axes(0.91,0.96;0.06x0.03)"):
        samp2.set_val(165)
    elif  (str(angle.inaxes)=="Axes(0.91,0.91;0.06x0.03)"):
        samp2.set_val(150)
    elif  (str(angle.inaxes)=="Axes(0.91,0.86;0.06x0.03)"):
        samp2.set_val(135)
    elif  (str(angle.inaxes)=="Axes(0.91,0.81;0.06x0.03)"):
        samp2.set_val(120)
    elif  (str(angle.inaxes)=="Axes(0.91,0.76;0.06x0.03)"):
        samp2.set_val(105)
    elif  (str(angle.inaxes)=="Axes(0.91,0.71;0.06x0.03)"):
        samp2.set_val(90)
    elif  (str(angle.inaxes)=="Axes(0.91,0.66;0.06x0.03)"):
        samp2.set_val(75)
    elif  (str(angle.inaxes)=="Axes(0.91,0.61;0.06x0.03)"):
        samp2.set_val(60)
    elif  (str(angle.inaxes)=="Axes(0.91,0.56;0.06x0.03)"):
        samp2.set_val(45)
    elif  (str(angle.inaxes)=="Axes(0.91,0.51;0.06x0.03)"):
        samp2.set_val(30)
    elif  (str(angle.inaxes)=="Axes(0.91,0.45;0.06x0.03)"):
        samp2.set_val(15)



beta =  np.linspace(0,180,180)
#ani = FuncAnimation(fig, find_phase, frames=beta, blit=True)
axamp = plt.axes([0.05, 0.05, 0.40, 0.03], facecolor="lightgoldenrodyellow")
axamp2 = plt.axes([0.55, 0.05, 0.4, 0.03], facecolor="lightgoldenrodyellow")
samp = Slider(axamp, 'Theta',-90, 90, valinit=0)
samp2 = Slider(axamp2, 'Phi',0, 180, valinit=90)
buttonAx = plt.axes([.05,.1,.2,.07], facecolor = "grey")
b = Button(buttonAx,"Update 3D Pattern")
b.on_clicked(create_3d)
buttonAx = plt.axes([.05,.96,.06,.03], facecolor = "grey")
ThetaButton1 = Button(buttonAx, "75")
ThetaButton1.on_clicked(SliderAndThetaUpdate)
buttonAx = plt.axes([.05,.91,.06,.03], facecolor = "grey")
ThetaButton2 = Button(buttonAx, "60")
ThetaButton2.on_clicked(SliderAndThetaUpdate)
buttonAx = plt.axes([.05,.86,.06,.03], facecolor = "grey")
ThetaButton3 = Button(buttonAx, "45")
ThetaButton3.on_clicked(SliderAndThetaUpdate)
buttonAx = plt.axes([.05,.81,.06,.03], facecolor = "grey")
ThetaButton4 = Button(buttonAx, "30")
ThetaButton4.on_clicked(SliderAndThetaUpdate)
buttonAx = plt.axes([.05,.76,.06,.03], facecolor = "grey")
ThetaButton5 = Button(buttonAx, "15")
ThetaButton5.on_clicked(SliderAndThetaUpdate)
buttonAx = plt.axes([.05,.71,.06,.03], facecolor = "grey")
ThetaButton6 = Button(buttonAx, "0")
ThetaButton6.on_clicked(SliderAndThetaUpdate)
buttonAx = plt.axes([.05,.66,.06,.03], facecolor = "grey")
ThetaButton7 = Button(buttonAx, "-15")
ThetaButton7.on_clicked(SliderAndThetaUpdate)
buttonAx = plt.axes([.05,.61,.06,.03], facecolor = "grey")
ThetaButton8 = Button(buttonAx, "-30")
ThetaButton8.on_clicked(SliderAndThetaUpdate)
buttonAx = plt.axes([.05,.56,.06,.03], facecolor = "grey")
ThetaButton9 = Button(buttonAx, "-45")
ThetaButton9.on_clicked(SliderAndThetaUpdate)
buttonAx = plt.axes([.05,.51,.06,.03], facecolor = "grey")
ThetaButton10 = Button(buttonAx, "-60")
ThetaButton10.on_clicked(SliderAndThetaUpdate)
buttonAx = plt.axes([.05,.45,.06,.03], facecolor = "grey")
ThetaButton11 = Button(buttonAx, "-75")
ThetaButton11.on_clicked(SliderAndThetaUpdate)


buttonAx = plt.axes([.91,.96,.06,.03], facecolor = "grey")
PhiButton1 = Button(buttonAx, "165")
PhiButton1.on_clicked(SliderAndPhiUpdate)
buttonAx = plt.axes([.91,.91,.06,.03], facecolor = "grey")
PhiButton2 = Button(buttonAx, "150")
PhiButton2.on_clicked(SliderAndPhiUpdate)
buttonAx = plt.axes([.91,.86,.06,.03], facecolor = "grey")
PhiButton3 = Button(buttonAx, "135")
PhiButton3.on_clicked(SliderAndPhiUpdate)
buttonAx = plt.axes([.91,.81,.06,.03], facecolor = "grey")
PhiButton4 = Button(buttonAx, "120")
PhiButton4.on_clicked(SliderAndPhiUpdate)
buttonAx = plt.axes([.91,.76,.06,.03], facecolor = "grey")
PhiButton5 = Button(buttonAx, "105")
PhiButton5.on_clicked(SliderAndPhiUpdate)
buttonAx = plt.axes([.91,.71,.06,.03], facecolor = "grey")
PhiButton6 = Button(buttonAx, "90")
PhiButton6.on_clicked(SliderAndPhiUpdate)
buttonAx = plt.axes([.91,.66,.06,.03], facecolor = "grey")
PhiButton7 = Button(buttonAx, "75")
PhiButton7.on_clicked(SliderAndThetaUpdate)
buttonAx = plt.axes([.91,.61,.06,.03], facecolor = "grey")
PhiButton8 = Button(buttonAx, "60")
PhiButton8.on_clicked(SliderAndPhiUpdate)
buttonAx = plt.axes([.91,.56,.06,.03], facecolor = "grey")
PhiButton9 = Button(buttonAx, "45")
PhiButton9.on_clicked(SliderAndPhiUpdate)
buttonAx = plt.axes([.91,.51,.06,.03], facecolor = "grey")
PhiButton10 = Button(buttonAx, "30")
PhiButton10.on_clicked(SliderAndPhiUpdate)
buttonAx = plt.axes([.91,.45,.06,.03], facecolor = "grey")
PhiButton11 = Button(buttonAx, "15")
PhiButton11.on_clicked(SliderAndPhiUpdate)

samp2.on_changed(find_phase_forTheta)
samp.on_changed(find_phase_forTheta)


plt.show()