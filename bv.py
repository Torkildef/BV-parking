import time
import math
import random
import pygame
import pyautogui


win = pygame.display.set_mode((400,400), pygame.RESIZABLE)

pygame.display.set_caption("Parking Bv")
ikon = pygame.image.load('parkering-ikon.png')
pygame.display.set_icon(ikon)

forhold = 0.4
lengdeV = 277 * forhold
#breddeV = 187 * forhold
breddeV = 182 * forhold

vogn = pygame.transform.scale(pygame.image.load('vogn.png'), (int(lengdeV),int(breddeV)))
vognBredde = vogn.get_width()
vognHoyde = vogn.get_height()

xPos = 180
yPos = 80
grad = 0
fart = 1
retning = 0
avstand = (lengdeV + 70) * forhold #Avstand mellom vogner
utslag = 1.6 #utslagsverdi per kall på ny retning
tolvSjuGrad = 0
tolvSjuGradMål = 0
brems = False
tidStoppet = 0
treffPunkter = []
bullets = []
smell = []

def mellompause(plass):
    pygame.draw.circle(win, (200,0,0), plass, 20, 0)
    pygame.display.update()
    time.sleep(2)
def krasj(KB,TFF, PX, PY, LX, LY, farge):
    global running
    global xPos
    global yPos
    global grad
    global fart
    global retning
    global smell
    pygame.draw.rect(win, farge, (PX, PY, LX, LY))
    pygame.draw.rect(win, (0,0,0), (PX, PY, LX, LY),2)
    for i in range(len(KB)):
        for j in range(len(KB[i])):
            if KB[i][j][0] > PX and KB[i][j][0] < (PX + LX) and KB[i][j][1] > PY and KB[i][j][1] < (PY + LY):
                smell.append(KB[i][j])
                break
    for i in range(len(TFF)):
        if TFF[i][0] > PX and TFF[i][0] < (PX + LX) and TFF[i][1] > PY and TFF[i][1] < (PY + LY):
            xPos = 180
            yPos = 80
            grad = 0
            fart = 0
            retning = 0
            return TFF[i]
            
def seier(TFF, PX, PY, LX, LY):
    innafor = 0
    global running

    for i in range(len(TFF)):
        if not (TFF[i][0] > PX and TFF[i][0] < (PX + LX) and TFF[i][1] > PY and TFF[i][1] < (PY + LY)):
             break
        else:
            innafor += 1

    if innafor == len(TFF):
        clock.tick(0.5)
        running = False
        print("Seier")

def seierPunkt(x,y,xl,yl):
    pygame.draw.rect(win, (70,70,70), (x, y, xl, yl))
    pygame.draw.rect(win, (0,150,0), (x-3,y-3,xl+6,yl+6),5)


def masseproduksjonAvTreffpunkt(P1, P2, verdi, retning, av):
    TP1X = int(P1 - verdi*av*math.cos((retning + grad)*(math.pi/180)))
    TP1Y = int(P2 + verdi*av*math.sin((retning + grad)*(math.pi/180)))
    hjelpeprikker((0,0,0),(TP1X, TP1Y))
    return (TP1X, TP1Y)

def masseproduksjonAvTreffpunktKort(P1, P2, verdi, retning, av):
    TP1X = int(P1 + verdi*av*math.sin((retning + grad)*(math.pi/180)))
    TP1Y = int(P2 + verdi*av*math.cos((retning + grad)*(math.pi/180)))
    hjelpeprikker((0,0,0),(TP1X, TP1Y))
    return (TP1X, TP1Y)

def plasseringhjelperX(utgangspunktX, utgangspunktY, endring):
    xPF = int(utgangspunktX + endring*math.cos((retning + grad)*(math.pi/180)))
    yPF = int(utgangspunktY - endring*math.sin((retning + grad)*(math.pi/180)))
    return (xPF, yPF)
def plasseringhjelperXogY(utgangspunktX, utgangspunktY, endringX, endringY, retning):
    xPF = int(utgangspunktX + endringY*math.sin((retning + grad)*(math.pi/180)) + endringX*math.cos((retning + grad)*(math.pi/180)))
    yPF = int(utgangspunktY + endringY*math.cos((retning + grad)*(math.pi/180)) - endringX *math.sin((retning + grad)*(math.pi/180)))
    return (xPF, yPF)
def hjelpeprikker(farge, posisjon):
    #pygame.draw.circle(win, farge, posisjon, 2, 1)
    return
def vridning_12_7(x, y):
    xL = round(x - pygame.mouse.get_pos()[0], 2)
    yL = round(y - pygame.mouse.get_pos()[1], 2)

    if not(xL == 0):
        if xL < 0:
            if yL < 0:
                return 360 -math.atan(yL/xL)*(180/math.pi)
            else:
                return -math.atan(yL/xL)*(180/math.pi)
        else:
            return 180-math.atan(yL/xL)*(180/math.pi)
    elif yL > 0:
        return 90
    else:
        return -90
def sakteVridning(tolvSjuGradMål, tolvSjuGrad):

    if not(tolvSjuGrad == tolvSjuGradMål):
        if tolvSjuGrad >= tolvSjuGradMål:
            if tolvSjuGrad - tolvSjuGradMål <= 180:
                tolvSjuGrad -= 2
            else:
                tolvSjuGrad += 2

        if tolvSjuGrad < tolvSjuGradMål:
            if tolvSjuGradMål - tolvSjuGrad <= 180:
                tolvSjuGrad += 2
            else:
                tolvSjuGrad -= 2

        if tolvSjuGrad > 360:
            return 0
        if tolvSjuGrad < 0:
            return 360
        return tolvSjuGrad
    else:
        return tolvSjuGradMål
class projoctile(object):
    def __init__(self, x, y, radius, color, grad, kulebane):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.grad = grad
        self.vel = 200 + random.randint(-30,30)
        self.kulebane = kulebane

    def draw(self,win):
        pygame.draw.circle(win, self.color, (int(self.x),int(self.y)), self.radius)


def vogne(posisjon, vogn, grad, retning, verdi, fart):

    BeregningX = math.cos((grad)*(math.pi/180))* (avstand*math.cos((retning)*(math.pi/180)))
    PosX = int(posisjon[0] + verdi* BeregningX)
    BeregningY = math.sin((grad)*(math.pi/180))* (avstand*math.cos((retning)*(math.pi/180)))
    PosY = int(posisjon[1] - verdi * BeregningY)
    Svogn = (PosX, PosY)
    vogn = pygame.transform.rotate(vogn, retning + grad)
    firkant = vogn.get_rect()
    firkant.center = Svogn
    hjelpeprikker((0,125,0),Svogn)
    PrikkForanX = int(PosX + verdi*53*math.cos((retning + grad)*(math.pi/180)))
    PrikkForanY = int(PosY - verdi*53*math.sin((retning + grad)*(math.pi/180)))
    hjelpeprikker((255,0,0),(PrikkForanX, PrikkForanY))
    PrikkVForanX = int(PrikkForanX - verdi*(breddeV/2)*math.sin((retning + grad)*(math.pi/180)))
    PrikkVForanY = int(PrikkForanY - verdi*(breddeV/2)*math.cos((retning + grad)*(math.pi/180)))
    hjelpeprikker((255,100,0),(PrikkVForanX, PrikkVForanY))
    PrikkHForanX = int(PrikkForanX + verdi*(breddeV/2)*math.sin((retning + grad)*(math.pi/180)))
    PrikkHForanY = int(PrikkForanY + verdi*(breddeV/2)*math.cos((retning + grad)*(math.pi/180)))
    hjelpeprikker((255,100,0),(PrikkHForanX, PrikkHForanY))
    PrikkBakX = int(PosX - verdi*55*math.cos((retning + grad)*(math.pi/180)))
    PrikkBakY = int(PosY + verdi*55*math.sin((retning + grad)*(math.pi/180)))
    hjelpeprikker((255,100,0),(PrikkBakX, PrikkBakY))
    #Disse er kansje ikke kalibret til ny bv
    PrikkVBakX = int(PrikkBakX - verdi*32*math.sin((retning + grad)*(math.pi/180)))
    PrikkVBakY = int(PrikkBakY - verdi*32*math.cos((retning + grad)*(math.pi/180)))
    hjelpeprikker((255,100,0),(PrikkVBakX, PrikkVBakY))

    senter12_7X = int(PosX - 28*math.cos((retning + grad)*(math.pi/180)))
    senter12_7Y = int(PosY + 28*math.sin((retning + grad)*(math.pi/180)))


    if verdi == 1:
        #FramLYS
        pygame.draw.circle(win, (255,200,0), (plasseringhjelperXogY(PosX, PosY, 57, 29, retning)), 5, 0)
        pygame.draw.circle(win, (255,200,0), (plasseringhjelperXogY(PosX, PosY, 57, -29, retning)), 5, 0)

    if verdi == -1:

        #BAKVOGN
        pygame.draw.polygon(win, (0,157,87), ((plasseringhjelperXogY(PrikkBakX, PrikkBakY, 0, -(breddeV/2), retning)), (PrikkHForanX, PrikkHForanY), (PrikkVForanX, PrikkVForanY), (plasseringhjelperXogY(PrikkBakX, PrikkBakY, 0, (breddeV/2), retning))),0)
        pygame.draw.polygon(win, (30,30,30), ((plasseringhjelperXogY(PrikkBakX, PrikkBakY, 0, -(breddeV/2), retning)), (PrikkHForanX, PrikkHForanY), (PrikkVForanX, PrikkVForanY), (plasseringhjelperXogY(PrikkBakX, PrikkBakY, 0, (breddeV/2), retning))),3)

        #ryggelys
        if fart < -0.1:
            pygame.draw.circle(win, (255,240,200), (plasseringhjelperXogY(PosX, PosY, -57, 0, retning)), 5, 0)

        #BAKLYS
        pygame.draw.circle(win, (255,0,0), (plasseringhjelperXogY(PosX, PosY, -55, 29, retning)), 4, 0)
        pygame.draw.circle(win, (255,0,0), (plasseringhjelperXogY(PosX, PosY, -55, -29, retning)), 4, 0)

    if verdi == 1:
        #FRAMvogn
        pygame.draw.polygon(win, (0,157,87), ((plasseringhjelperXogY(PrikkBakX, PrikkBakY, 0, -(breddeV/2), retning)), (PrikkVForanX, PrikkVForanY), (PrikkHForanX, PrikkHForanY), (plasseringhjelperXogY(PrikkBakX, PrikkBakY, 0, (breddeV/2), retning))),0)
        pygame.draw.polygon(win, (30,30,30), ((plasseringhjelperXogY(PrikkBakX, PrikkBakY, 0, -(breddeV/2), retning)), (PrikkVForanX, PrikkVForanY), (PrikkHForanX, PrikkHForanY), (plasseringhjelperXogY(PrikkBakX, PrikkBakY, 0, (breddeV/2), retning))),3)

        tolvSjuGrad = vridning_12_7(senter12_7X, senter12_7Y) - grad

        #panser
        pygame.draw.line(win, (0,0,0), (plasseringhjelperXogY(PrikkVForanX, PrikkVForanY, -12, -1, retning)), (plasseringhjelperXogY(PrikkHForanX, PrikkHForanY, -12, 1, retning)), 3)
        pygame.draw.polygon(win, (60,60,60), ((plasseringhjelperXogY(PrikkVForanX, PrikkVForanY, -11, 15, retning)),(plasseringhjelperXogY(PrikkVForanX, PrikkVForanY, 1, 15, retning)), (plasseringhjelperXogY(PrikkHForanX, PrikkHForanY, 1, -15, retning)), (plasseringhjelperXogY(PrikkHForanX, PrikkHForanY, -11, -15, retning))))
        pygame.draw.polygon(win, (20,20,20), ((plasseringhjelperXogY(PrikkVForanX, PrikkVForanY, -11, 15, retning)),(plasseringhjelperXogY(PrikkVForanX, PrikkVForanY, 1, 15, retning)), (plasseringhjelperXogY(PrikkHForanX, PrikkHForanY, 1, -15, retning)), (plasseringhjelperXogY(PrikkHForanX, PrikkHForanY, -11, -15, retning))),1)


        PrikkX = int(PosX - avstand*math.cos((retning + grad)*(math.pi/180)))
        PrikkY = int(PosY + avstand*math.sin((retning + grad)*(math.pi/180)))
        hjelpeprikker((255,255,0), (PrikkX, PrikkY))

        #Antenne
        pygame.draw.circle(win, (0,0,0), (plasseringhjelperXogY(PrikkBakX, PrikkBakY, 10, 30, retning)), 2, 0)
        pygame.draw.circle(win, (0,0,0), (plasseringhjelperXogY(PrikkBakX, PrikkBakY, 10, -30, retning)), 2, 0)

        #ledd
        pygame.draw.circle(win, (30,30,30), (PrikkX, PrikkY), 7, 6)

        #Ledd
        pygame.draw.polygon(win, (30,30,30), ((plasseringhjelperXogY(PrikkBakX, PrikkBakY, -avstand/5, -5, retning)),(plasseringhjelperXogY(PrikkBakX, PrikkBakY, 0, -5, retning)), (plasseringhjelperXogY(PrikkBakX, PrikkBakY, 0, -1, retning)), (plasseringhjelperXogY(PrikkBakX, PrikkBakY, -avstand/5, -1, retning))))
        pygame.draw.polygon(win, (30,30,30), ((plasseringhjelperXogY(PrikkBakX, PrikkBakY, -avstand/5, 1, retning)),(plasseringhjelperXogY(PrikkBakX, PrikkBakY, 0, 1, retning)), (plasseringhjelperXogY(PrikkBakX, PrikkBakY, 0, 5, retning)), (plasseringhjelperXogY(PrikkBakX, PrikkBakY, -avstand/5, 5, retning))))

        #Luke
        pygame.draw.polygon(win, (0,90,0), ((plasseringhjelperXogY(PrikkHForanX, PrikkHForanY, -39, -27, retning)), (plasseringhjelperXogY(PrikkHForanX, PrikkHForanY, -19, -27, retning)), (plasseringhjelperXogY(PrikkHForanX, PrikkHForanY, -19, -5, retning)), (plasseringhjelperXogY(PrikkHForanX, PrikkHForanY, -39, -5, retning))),0)
        pygame.draw.polygon(win, (0,0,0), ((plasseringhjelperXogY(PrikkHForanX, PrikkHForanY, -39, -27, retning)), (plasseringhjelperXogY(PrikkHForanX, PrikkHForanY, -19, -27, retning)), (plasseringhjelperXogY(PrikkHForanX, PrikkHForanY, -19, -5, retning)), (plasseringhjelperXogY(PrikkHForanX, PrikkHForanY, -39, -5, retning))),2)

        #12,7 ring
        pygame.draw.circle(win, (0,0,0), (plasseringhjelperX(PosX, PosY, -28)), 21, 2)
        #12,7 luke
        pygame.draw.polygon(win, (90,90,90), ((plasseringhjelperXogY(senter12_7X, senter12_7Y, -11, -11, retning)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 10, -11, retning)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 10, 11, retning)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, -11, 11, retning))),2)

        #12,7 stavtiv

        #VENSTRE
        pygame.draw.line(win, (0,70,0), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 26, 0, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 23, -10, tolvSjuGrad)), 3)
        pygame.draw.line(win, (0,70,0), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 23, -10, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 14, -14, tolvSjuGrad)), 3)
        pygame.draw.line(win, (0,70,0), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 14, -14, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 0, -16, tolvSjuGrad)), 3)
        pygame.draw.line(win, (0,70,0), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 0, -16, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, -15, -14, tolvSjuGrad)), 3)
        #HØYRE
        pygame.draw.line(win, (0,70,0), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 26, 0, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 23, 10, tolvSjuGrad)), 3)
        pygame.draw.line(win, (0,70,0), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 23, 10, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 14, 14, tolvSjuGrad)), 3)
        pygame.draw.line(win, (0,70,0), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 14, 14, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 0, 16, tolvSjuGrad)), 3)
        pygame.draw.line(win, (0,70,0), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 0, 16, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, -15, 14, tolvSjuGrad)), 3)
        #bak
        pygame.draw.line(win, (0,70,0), (plasseringhjelperXogY(senter12_7X, senter12_7Y, -15, -14, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, -15, 14, tolvSjuGrad)), 3)
        pygame.draw.circle(win, (0,70,0), (plasseringhjelperXogY(senter12_7X, senter12_7Y, -15, -14, tolvSjuGrad)), 3, 0)
        pygame.draw.circle(win, (0,70,0), (plasseringhjelperXogY(senter12_7X, senter12_7Y, -15, 14, tolvSjuGrad)), 3, 0)


        #ÅpenLuke
        pygame.draw.polygon(win, (30,30,30), ((plasseringhjelperXogY(senter12_7X, senter12_7Y, -20, -11, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, -11, -11, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, -11, 11, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, -20, 11, tolvSjuGrad))))

        #Underlavett
        pygame.draw.polygon(win, (60,100,60), ((plasseringhjelperXogY(senter12_7X, senter12_7Y, 4, -5, tolvSjuGrad)),(plasseringhjelperXogY(senter12_7X, senter12_7Y, 39, -5, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 39, 5, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 4, 5, tolvSjuGrad))))
        pygame.draw.polygon(win, (50,50,50), ((plasseringhjelperXogY(senter12_7X, senter12_7Y, 4, -5, tolvSjuGrad)),(plasseringhjelperXogY(senter12_7X, senter12_7Y, 39, -5, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 39, 5, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 4, 5, tolvSjuGrad))),1)

        #12,7
        pygame.draw.polygon(win, (0,0,0), ((plasseringhjelperXogY(senter12_7X, senter12_7Y, 8, 3, tolvSjuGrad)),(plasseringhjelperXogY(senter12_7X, senter12_7Y, 37, 3, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 37, -3, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 8, -3, tolvSjuGrad))))
        pygame.draw.polygon(win, (0,0,0), ((plasseringhjelperXogY(senter12_7X, senter12_7Y, 8, -8, tolvSjuGrad)),(plasseringhjelperXogY(senter12_7X, senter12_7Y, 11, -8, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 11, 8, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 8, 8, tolvSjuGrad))))

        #ammoBoks
        #boks
        pygame.draw.polygon(win, (60,100,60), ((plasseringhjelperXogY(senter12_7X, senter12_7Y, 27, -4, tolvSjuGrad)),(plasseringhjelperXogY(senter12_7X, senter12_7Y, 27, -15, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 35, -15, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 35, -4, tolvSjuGrad))))
        #kant
        pygame.draw.polygon(win, (0,0,0), ((plasseringhjelperXogY(senter12_7X, senter12_7Y, 27, -4, tolvSjuGrad)),(plasseringhjelperXogY(senter12_7X, senter12_7Y, 27, -15, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 35, -15, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 35, -4, tolvSjuGrad))),1)
        #patron gull
        pygame.draw.polygon(win, (218,165,32), ((plasseringhjelperXogY(senter12_7X, senter12_7Y, 29, -2, tolvSjuGrad)),(plasseringhjelperXogY(senter12_7X, senter12_7Y, 29, -13, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 32, -13, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 32, -2, tolvSjuGrad))))
        #patron sølv
        pygame.draw.polygon(win, (160,160,160), ((plasseringhjelperXogY(senter12_7X, senter12_7Y, 32, -2, tolvSjuGrad)),(plasseringhjelperXogY(senter12_7X, senter12_7Y, 32, -13, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 33, -13, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 33, -2, tolvSjuGrad))))



        #dude
        pygame.draw.polygon(win, (200,200,200), ((plasseringhjelperXogY(senter12_7X, senter12_7Y, -8, -9, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 2, -9, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 2, 0, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, -8, 0, tolvSjuGrad))))
        pygame.draw.polygon(win, (200,200,200), ((plasseringhjelperXogY(senter12_7X, senter12_7Y, -8, 0, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 2, 0, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 2, 9, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, -8, 9, tolvSjuGrad))))
        pygame.draw.line(win, ((180,138,120)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, -1, -6, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 8, -6, tolvSjuGrad)), 5)
        pygame.draw.line(win, ((180,138,120)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, -1, 6, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 8, 6, tolvSjuGrad)), 5)
        pygame.draw.circle(win, (40,100,40), (plasseringhjelperXogY(senter12_7X, senter12_7Y, -2, 0, tolvSjuGrad)), 5, 0)


        #pipe
        pygame.draw.polygon(win, (0,0,0), ((plasseringhjelperXogY(senter12_7X, senter12_7Y, 36, 1, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 58, 1, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 58, -1, tolvSjuGrad)), (plasseringhjelperXogY(senter12_7X, senter12_7Y, 36, -1, tolvSjuGrad))))




        #Speil
        pygame.draw.polygon(win, (0,0,0), ((plasseringhjelperXogY(PrikkVForanX, PrikkVForanY, -14, -8, retning)), (plasseringhjelperXogY(PrikkVForanX, PrikkVForanY, -8, -6, retning)), (plasseringhjelperXogY(PrikkVForanX, PrikkVForanY, -8, 0, retning)), (plasseringhjelperXogY(PrikkVForanX, PrikkVForanY, -12, 0, retning))),0)
        pygame.draw.polygon(win, (0,0,0), ((plasseringhjelperXogY(PrikkHForanX, PrikkHForanY, -14, 8, retning)), (plasseringhjelperXogY(PrikkHForanX, PrikkHForanY, -8, 6, retning)), (plasseringhjelperXogY(PrikkHForanX, PrikkHForanY, -8, 0, retning)), (plasseringhjelperXogY(PrikkHForanX, PrikkHForanY, -12, 0, retning))),0)


        #Skyting
        if keys[pygame.K_SPACE]:
            if len(bullets) < 100:
                KuleBane = []
                for i in range(1900):
                    x = plasseringhjelperXogY(senter12_7X, senter12_7Y, 58, 0, tolvSjuGrad)[0]
                    x += i*math.cos((-tolvSjuGrad)*(math.pi/180))
                    y = plasseringhjelperXogY(senter12_7X, senter12_7Y, 58, 0, tolvSjuGrad)[1]
                    y += i*math.sin((-tolvSjuGrad)*(math.pi/180))
                    if (x < 1900) and (y < 1000) and (x > 0) and (y > 0):
                        KuleBane.append(plasseringhjelperXogY(senter12_7X, senter12_7Y, 58 + i, 0, tolvSjuGrad))
                    else:
                        break

                bullets.append(projoctile((plasseringhjelperXogY(senter12_7X, senter12_7Y, 58, 0, tolvSjuGrad))[0], (plasseringhjelperXogY(senter12_7X, senter12_7Y, 58, 0, tolvSjuGrad))[1], 1, (0,0,0),tolvSjuGrad +grad, KuleBane))
                pygame.draw.circle(win, (250,250,100), plasseringhjelperXogY(senter12_7X, senter12_7Y, 60, 0, tolvSjuGrad),6,0)
                pygame.draw.circle(win, (250,180,20), plasseringhjelperXogY(senter12_7X, senter12_7Y, 59, 0, tolvSjuGrad),4,0)


    if verdi == -1:

        if (keys[pygame.K_DOWN] or keys[pygame.K_UP]) and not(fart == 0) and brems ==True:
            pygame.draw.circle(win, (255,0,0), (plasseringhjelperXogY(PosX, PosY, -57, 29, retning)), 5, 0)
            pygame.draw.circle(win, (255,0,0), (plasseringhjelperXogY(PosX, PosY, -57, -29, retning)), 5, 0)

        #Ledd
        pygame.draw.polygon(win, (30,30,30), ((plasseringhjelperXogY(PrikkBakX, PrikkBakY, 0, -5, retning)),(plasseringhjelperXogY(PrikkBakX, PrikkBakY, avstand/5, -5, retning)), (plasseringhjelperXogY(PrikkBakX, PrikkBakY, avstand/5, -1, retning)), (plasseringhjelperXogY(PrikkBakX, PrikkBakY, 0, -1, retning))))
        pygame.draw.polygon(win, (30,30,30), ((plasseringhjelperXogY(PrikkBakX, PrikkBakY, 0, 1, retning)),(plasseringhjelperXogY(PrikkBakX, PrikkBakY, avstand/5, 1, retning)), (plasseringhjelperXogY(PrikkBakX, PrikkBakY, avstand/5, 5, retning)), (plasseringhjelperXogY(PrikkBakX, PrikkBakY, 0, 5, retning))))

        #boks bak
        pygame.draw.polygon(win, (0,90,0), ((plasseringhjelperXogY(PrikkBakX, PrikkBakY, -20, -25, retning)),(plasseringhjelperXogY(PrikkBakX, PrikkBakY, -7, -25, retning)), (plasseringhjelperXogY(PrikkBakX, PrikkBakY, -7, 25, retning)), (plasseringhjelperXogY(PrikkBakX, PrikkBakY, -20, 25, retning))))
        pygame.draw.polygon(win, (0,0,0), ((plasseringhjelperXogY(PrikkBakX, PrikkBakY, -20, -25, retning)),(plasseringhjelperXogY(PrikkBakX, PrikkBakY, -7, -25, retning)), (plasseringhjelperXogY(PrikkBakX, PrikkBakY, -7, 25, retning)), (plasseringhjelperXogY(PrikkBakX, PrikkBakY, -20, 25, retning))),2)

    treffPunkter = []
    for i in range(10):
        treffPunkter.append(masseproduksjonAvTreffpunkt(PrikkVForanX, PrikkVForanY, verdi, retning, i*10))
        treffPunkter.append(masseproduksjonAvTreffpunkt(PrikkHForanX, PrikkHForanY, verdi, retning, i*10))
        treffPunkter.append(masseproduksjonAvTreffpunktKort(PrikkVBakX, PrikkVBakY, verdi, retning, i*7))
        treffPunkter.append(masseproduksjonAvTreffpunktKort(PrikkVForanX, PrikkVForanY, verdi, retning, i*7))
    if verdi == 1:
        PrikkX = int(PosX - avstand*math.cos((retning + grad)*(math.pi/180)))
        PrikkY = int(PosY + avstand*math.sin((retning + grad)*(math.pi/180)))
        hjelpeprikker((255,255,0), (PrikkX, PrikkY))
    return treffPunkter

#LEVLER
def LeveL1():
    seierPunkt(1250, 580, 100, 300)
    TFF = vogne(posisjon, vogn, grad, -retning, -1, fart)
    TFB = vogne(posisjon, vogn, grad, retning, 1, fart)
    TP = (TFF + TFB)
    KBR = []

    for bullet in bullets:
        if  0 > bullet.x or bullet.x > 2000 or 0 > bullet.y or bullet.y > 1000:
                bullets.pop(bullets.index(bullet))
        KBR.append(bullet.kulebane)
        bullet.x += bullet.vel*math.cos((bullet.grad)*(math.pi/180))
        bullet.y += -bullet.vel*math.sin((bullet.grad)*(math.pi/180))
        bullet.draw(win)
    smell =[]
    #kanter
    krasj(KBR, TP, 0, 0, 1910, 10, (30,30,30))
    krasj(KBR ,TP, 0, 0, 10, 1000, (30,30,30))
    krasj(KBR ,TP, 0, 990, 1910, 10, (30,30,30))
    krasj(KBR ,TP, 1910, 0, 10, 1000,(30,30,30))

    #løp
    krasj(KBR, TP, 200, 150, 10, 800, (30,30,30))
    krasj(KBR, TP, 200, 950, 1510, 10, (30,30,30))
    krasj(KBR, TP, 1700, 150, 10, 800, (30,30,30))

    #hindring
    krasj(KBR, TP, 1250, 200, 100, 300, (70,30,30))
    #print(smell)
    for i in range(len(smell)):
        pygame.draw.circle(win,(200,50,50),smell[i],6,0)
    #plass
    seier(TP, 1250, 580, 100, 300)

def LeveL2():
    seierPunkt(1050, 580, 100, 300)
    TFF = vogne(posisjon, vogn, grad, -retning, -1, fart)
    TFB = vogne(posisjon, vogn, grad, retning, 1, fart)
    TP = (TFF + TFB)
    #kanter
    krasj(TP, 0, 0, 1910, 10, (30,30,30))
    krasj(TP, 0, 0, 10, 1000, (30,30,30))
    krasj(TP, 0, 990, 1910, 10, (30,30,30))
    krasj(TP, 1910, 0, 10, 1000,(30,30,30))

    #løp
    krasj(TP, 200, 150, 10, 800, (30,30,30))
    krasj(TP, 200, 950, 1510, 10, (30,30,30))
    krasj(TP, 1700, 150, 10, 800, (30,30,30))

    #hindring
    krasj(TP, 1250, 200, 100, 300, (70,30,30))

    #plass
    seier(TP, 1050, 580, 100, 300)


running = True
sekunder = 0

while running:
    sekunder += (1/30)
    clock = pygame.time.Clock()
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            sreen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
    keys = pygame.key.get_pressed()


    #SVINGING
    if keys[pygame.K_LEFT] and retning < 20:
        retning += utslag
        yPos += ((utslag/3)*math.cos((grad)*(math.pi/180)))
        xPos += ((utslag/3)*math.sin((grad)*(math.pi/180)))
    if keys[pygame.K_RIGHT] and retning > -20:
        retning -= utslag
        yPos -= ((utslag/3)*math.cos((grad)*(math.pi/180)))
        xPos -= ((utslag/3)*math.sin((grad)*(math.pi/180)))

    #SVINGBREMS
    maksfartF = 16 -(abs(retning/6))
    maksfartB = -12 +(abs(retning/6))
    #brems
    if keys[pygame.K_UP] and fart < 0 and not(keys[pygame.K_DOWN]):
        brems = True
        if fart <= -0.5:
            fart +=0.5
        else:
            fart = 0
    elif keys[pygame.K_DOWN] and fart > 0 and not(keys[pygame.K_UP]):
        brems = True
        if fart >= 0.5:
            fart -=0.5
        else:
            fart = 0


    #GAS
    if brems == False:
        if keys[pygame.K_UP] and fart < maksfartF and not(keys[pygame.K_DOWN]):
            fart += 0.3
    #naturlig brems
        elif fart > 0:
            fart -= 0.15

    #fjerner auto fart
    #elif fart > -0.3 and not(keys[pygame.K_DOWN]):
      #  fart = 0

    if fart == 0:
        tidStoppet += 1/5
    else:
        tidStoppet = 0
    if tidStoppet >= 1 and brems == True:
        brems = False
        tidStoppet = 0

    if (not(keys[pygame.K_DOWN]) and not(keys[pygame.K_UP])):
        brems = False


    #Rygg
    if brems == False:
        if keys[pygame.K_DOWN] and fart > maksfartB and not(keys[pygame.K_UP]):
            fart -= 0.2
        elif fart < 0:
            fart += 0.1

    if 24 > retning > -24 and not(0.2 > retning > -0.2) and (fart > 0.1 or fart < -0.1):
        if 0 > retning > -24:
            retning += abs(fart/40)
        else:
            retning -= abs(fart/40)

    if fart > 0.15 or fart < -0.15:

        grad += retning*(fart/75)
        yPos -= math.sin((grad)*(math.pi/180)) * fart
        xPos += math.cos((grad)*(math.pi/180)) * fart
    posisjon = (int(xPos), int(yPos))
    win.fill((100,100,100))
    #LEVLER
    LeveL1()
    #LeveL2()






    pygame.display.update()
