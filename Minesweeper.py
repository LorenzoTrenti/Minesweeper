import pygame as pg
import random

pg.init()

WIDTH = 1300
HEIGHT = 700

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Campo minato")
Clock = pg.time.Clock()

FONT1 = pg.font.SysFont('Comic Sans MS', WIDTH//14, bold=True)
FONT2 = pg.font.SysFont('Comic Sans MS', WIDTH//20, bold=True)

titolo = "CAMPO MINATO"
modalità = "Scegliere difficoltà:"
facile = "Facile"
medio = "Normale"
difficile = "Difficile"
back = "Back to menu"
victory = "Victory!!! :)"
lose = "Che scarso :("

BOMB ='B'
GREEN  = (0, 255, 0)
DARK_GREEN = (150, 255, 100)
GREY = (230, 230, 230)
WHITE = (255, 255, 255)
BLUE = (80, 80, 255)
BLACK = (0, 0, 0)
COLOR_LOSE = "red"
COLOR_WIN = "green"

def crea_campo(x, y, rows, cols, n_bombe):    
    tabella = []
    for i in range(rows):
        riga = []
        for j in range(cols):
            riga.append(0)
        tabella.append(riga)
    
    i=0
    while i<n_bombe:
        flag=True
        asc=random.randint(0, rows-1)
        ord=random.randint(0, cols-1)
        if tabella[asc][ord]==0:
            for k in range(-1, 2, 1):
                for h in range(-1, 2, 1):
                    if asc==x+k and ord==y+h:
                        flag=False
            if flag:
                tabella[asc][ord]=BOMB
                i+=1

    for i in range(0, rows, 1):
        for j in range(cols):
            if tabella[i][j]!=BOMB:
                cont=0
                for k in range(-1, 2, 1):
                    for h in range(-1, 2, 1):
                        if i+k>=0 and i+k<rows and j+h>=0 and j+h<cols:
                            if tabella[i+k][j+h]==BOMB:
                                cont+=1
                tabella[i][j]=cont
    return tabella

def aggiorna():
    pg.display.flip()
    Clock.tick(60)

def centra_testo(text, color, flag, size):
    if flag==1:
        textSurface=FONT1.render(text, True, color)
    elif flag==2:
        textSurface=FONT2.render(text, True, color)
    else:
        FONT = pg.font.SysFont('Comic Sans MS', size-5, bold=True)
        textSurface=FONT.render(text, True, color)

    return textSurface, textSurface.get_rect()

def menu_iniziale():
    global facile_rect
    global medio_rect
    global difficile_rect
    global titolo_sup, titolo_rect

    titolo_sup, titolo_rect = centra_testo(titolo, "green", 1, 0)
    titolo_rect.center=(WIDTH/2, HEIGHT/9)
    screen.blit(titolo_sup, titolo_rect)
    i=0
    for j in range(4):
        if j==0:
            modalità_sup, modalità_rect = centra_testo(modalità, DARK_GREEN, 2, 0)
            modalità_rect.center=(WIDTH/2, HEIGHT/3 + i)
            screen.blit(modalità_sup, modalità_rect)
        elif j==1:
            facile_sup, facile_rect = centra_testo(facile, DARK_GREEN, 2, 0)
            facile_rect.center=(WIDTH/2, HEIGHT/3 + i)
            screen.blit(facile_sup, facile_rect)
        elif j==2:
            medio_sup, medio_rect = centra_testo(medio, DARK_GREEN, 2, 0)
            medio_rect.center=(WIDTH/2, HEIGHT/3 + i)
            screen.blit(medio_sup, medio_rect)
        elif j==3:
            difficile_sup, difficile_rect = centra_testo(difficile, DARK_GREEN, 2, 0)
            difficile_rect.center=(WIDTH/2, HEIGHT/3 + i)
            screen.blit(difficile_sup, difficile_rect)
        i+=WIDTH/18

def inizializza(size, rows, cols):
    global prato
    global controllo
    global tabella
    global bandiera_rect, bandiera
    global bomba_rect, bomba
    global perso, vinto

    perso=False
    vinto=False
    prato=pg.Rect(0, 0, size, size)
    controllo=[]
    tabella = []
    for i in range(rows):
        riga=[]
        for j in range(cols):
            riga.append(0)
        controllo.append(riga)
    bandiera = pg.image.load("Images/flag.png")
    bomba = pg.image.load("Images/bomb.png")
    bandiera = pg.transform.scale(bandiera, ((size-5, (size-5)*(bandiera.get_width()/bandiera.get_height()))))
    bomba = pg.transform.scale(bomba, (size-5, (size-5)*(bomba.get_width()/bomba.get_height())))
    bandiera_rect = bandiera.get_rect()
    bomba_rect=bomba.get_rect()
    return controllo

def stampa_campo(size, rows, cols, controllo, tabella):
    global back_rect
    global distanza_width, distanza_height
    distanza_width=(WIDTH-(cols*size))//2+size/2
    distanza_height=((HEIGHT-(rows*size))//2)+size/2+25
    for i in range(rows):
        for j in range(cols):
            prato.center=(distanza_width+(j*size), distanza_height+(i*size))
            if perso and tabella[i][j]==BOMB:
                controllo[i][j]=1
            if controllo[i][j]==1:
                if (i+j)%2==0:
                    pg.draw.rect(screen, GREY, prato)   
                else:
                    pg.draw.rect(screen, WHITE, prato)
                if tabella[i][j]!=0 and tabella[i][j]!=BOMB:
                    if tabella[i][j]==1:
                        color='red'
                    elif tabella[i][j]==2:
                        color="green"
                    elif tabella[i][j]==3:
                        color="blue"
                    elif tabella[i][j]==4:
                        color="purple"
                    elif tabella[i][j]==5:
                        color="gold"
                    else:
                        color="red"
                    val_sup, val_rect = centra_testo(str(tabella[i][j]), color, 3, size)
                    val_rect.center=prato.center
                    screen.blit(val_sup, val_rect)
                elif tabella[i][j]==BOMB:
                    bomba_rect.center=prato.center
                    screen.blit(bomba, bomba_rect)
            else:
                if (i+j)%2==0:
                    pg.draw.rect(screen, GREEN, prato)
                else:
                    pg.draw.rect(screen, DARK_GREEN, prato)
                if controllo[i][j]==2:
                    bandiera_rect.center=prato.center
                    screen.blit(bandiera, bandiera_rect)

    back_sup, back_rect = centra_testo(back, "white", 2, 0)
    back_rect.center=(WIDTH/2, HEIGHT-40)
    screen.blit(back_sup, back_rect)

def coordinate(x, y, size):
    x=((x-distanza_width+(0*size))//(size/2))
    y=((y-distanza_height+(0*size))//(size/2))
    if x%2==1:
        x+=1
    if y%2==1:
        y+=1
    x=int(x//2)
    y=int(y//2)
    return x, y

def riduci(x, y, tabella, controllo, rows, cols):
    for i in range(x-1, x+2, 1):
        for j in range(y-1, y+2, 1):
            if i>=0 and i<rows and j>=0 and j<cols:
                if tabella[i][j]==0 and controllo[i][j]==0:
                    controllo[i][j]=1
                    riduci(i, j, tabella, controllo, rows, cols)              
                else:
                    controllo[i][j]=1

def controllo_vittoria(controllo, tabella, rows, cols):
    vittoria=True
    for i in range(rows):
        for j in range(cols):
            if (controllo[i][j]==0 or controllo[i][j]==2) and tabella[i][j]!=BOMB:
                vittoria = False
    return vittoria
def hai_perso():
    lose_sup, lose_rect = centra_testo(lose, COLOR_LOSE, 2, 50)
    lose_rect.center=(WIDTH-(distanza_width/2), HEIGHT/2)
    screen.blit(lose_sup, lose_rect)

def hai_vinto():
    victory_sup, victory_rect = centra_testo(victory, COLOR_WIN, 2, 50)
    victory_rect.center=(distanza_width/2, HEIGHT/2)
    screen.blit(victory_sup, victory_rect)

menu=False
while True:
    creato=False
    screen.fill(BLUE)
    menu_iniziale()
    for event in pg.event.get():
        if event.type==pg.QUIT:
            exit()
        elif event.type==pg.MOUSEBUTTONDOWN:
            x, y=pg.mouse.get_pos()
            if x>=facile_rect.left and x<=facile_rect.right and y>=facile_rect.top and y<=facile_rect.bottom:
                ROWS=8
                COLS=10
                n_bombe=10
                menu=True
                SIZE=60
                controllo=inizializza(SIZE, ROWS, COLS)
            elif x>=medio_rect.left and x<=medio_rect.right and y>=medio_rect.top and y<=medio_rect.bottom:
                ROWS=14
                COLS=18
                n_bombe=40
                menu=True
                SIZE=35
                controllo=inizializza(SIZE, ROWS, COLS)
            elif x>=difficile_rect.left and x<=difficile_rect.right and y>=difficile_rect.top and y<=difficile_rect.bottom:
                ROWS=20
                COLS=24
                n_bombe=99
                menu=True
                SIZE=25
                controllo=inizializza(SIZE, ROWS, COLS)
    while menu:
        for event in pg.event.get():
            if event.type==pg.QUIT:
                exit()
            if event.type==pg.MOUSEBUTTONDOWN:
                asc, ord=pg.mouse.get_pos()
                y, x=coordinate(asc, ord, SIZE)
                if asc>=back_rect.left and asc<=back_rect.right and ord>=back_rect.top and ord<=back_rect.bottom:
                    menu=False
                if not perso and not vinto:
                    if x>=0 and x<ROWS and y>=0 and y<COLS:
                        if event.button==1:
                            if not creato:
                                tabella=crea_campo(x, y, ROWS, COLS, n_bombe)
                                creato=True
                            if controllo[x][y]==0 and tabella[x][y]==0:
                                riduci(x, y, tabella, controllo, ROWS, COLS)
                            elif controllo[x][y]==0 and tabella[x][y]!=0 and tabella[x][y]!=BOMB:
                                controllo[x][y]=1
                            elif controllo[x][y]==0 and tabella[x][y]==BOMB:
                                controllo[x][y]=1
                                perso=True
                        elif event.button==3 and creato and controllo[x][y]!=1:
                            if controllo[x][y]==0:
                                controllo[x][y]=2
                            else:
                                controllo[x][y]=0
                        if creato and controllo_vittoria(controllo, tabella, ROWS, COLS):
                            vinto=True
                
        screen.fill(BLUE)
        screen.blit(titolo_sup, titolo_rect)
        stampa_campo(SIZE, ROWS, COLS, controllo, tabella)
        if perso:
            hai_perso()
        if vinto:
            hai_vinto()
        aggiorna()

    aggiorna()