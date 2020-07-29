#!/usr/bin/env python

try:
    import numpy, random, time
    # scipy.special for the sigmoid function expit()
    import scipy.special
    # library for plotting arrays
    #import matplotlib.pyplot
    # ensure the plots are inside this notebook, not an external window
    import scipy.ndimage

    import random, os.path, sys, math
    import pygame
    from pygame.locals import *
    import pygame.freetype as freetype
    1/0
except:
    try:
        import tkinter
        import tkinter as tk
        from tkinter.commondialog import Dialog
    except:
        import Tkinter
        import Tkinter as tk
        from Tkinter.commondialog import Dialog


    class Message(Dialog):
        "A message box"

        command = "tk_messageBox"

    INFO, OK="info", "ok"
    def _show(title=None, message=None, _icon=None, _type=None, **options):
        if _icon and "icon" not in options:    options["icon"] = _icon
        if _type and "type" not in options:    options["type"] = _type
        if title:   options["title"] = title
        if message: options["message"] = message
        res = Message(**options).show()

    def showinfo(title=None, message=None, **options):
        "Show an info message"
        return _show(title, message, INFO, OK, **options)


    showinfo("Внимание","На вашем компьютере не установлены необходимые библиотеки. Список необходимых библиотек: pygame, numpy, scipy. вы можете установить их через терминал.")
    exit()


class neuralNetwork:

    # initialise the neural network
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        # set number of nodes in each input, hidden, output layer
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes

        # link weight matrices, wih and who
        # weights inside the arrays are w_i_j, where link is from node i to node j in the next layer
        # w11 w21
        # w12 w22 etc
        self.wih = numpy.random.normal(0.0, pow(self.inodes, -0.5), (self.hnodes, self.inodes))
        self.who = numpy.random.normal(0.0, pow(self.hnodes, -0.5), (self.onodes, self.hnodes))

        # learning rate
        self.lr = learningrate

        # activation function is the sigmoid function
        self.activation_function = lambda x: scipy.special.expit(x)

        pass

    # train the neural network
    def train(self, inputs_list, targets_list):
        # convert inputs list to 2d array
        inputs = numpy.array(inputs_list, ndmin=2).T
        targets = numpy.array(targets_list, ndmin=2).T

        # calculate signals into hidden layer
        hidden_inputs = numpy.dot(self.wih, inputs)
        # calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)

        # calculate signals into final output layer
        final_inputs = numpy.dot(self.who, hidden_outputs)
        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)

        # output layer error is the (target - actual)
        output_errors = targets - final_outputs
        # hidden layer error is the output_errors, split by weights, recombined at hidden nodes
        hidden_errors = numpy.dot(self.who.T, output_errors)

        # update the weights for the links between the hidden and output layers
        self.who += self.lr * numpy.dot((output_errors * final_outputs * (1.0 - final_outputs)),
                                        numpy.transpose(hidden_outputs))

        # update the weights for the links between the input and hidden layers
        self.wih += self.lr * numpy.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)),
                                        numpy.transpose(inputs))

        pass

    # query the neural network
    def query(self, inputs_list):
        # convert inputs list to 2d array
        inputs = numpy.array(inputs_list, ndmin=2).T

        # calculate signals into hidden layer
        hidden_inputs = numpy.dot(self.wih, inputs)
        # calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)

        # calculate signals into final output layer
        final_inputs = numpy.dot(self.who, hidden_outputs)
        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)

        return final_outputs


max_ = 0.4

hidden_nodes=69 #hehe
input_nodes = 28*28
output_nodes=3
learning_rate = 0.2

n = neuralNetwork(input_nodes,hidden_nodes,output_nodes, learning_rate)
a=open("wih.txt","r")
wih=numpy.loadtxt('wih.txt', delimiter=',')
a.close()

a=open("who.txt","r")
who=numpy.loadtxt('who.txt', delimiter=',')
a.close()
n.wih=wih
n.who=who



if not pygame.image.get_extended():
    raise SystemExit("Requires the extended image loading from SDL_image")
main_dir = os.path.split(os.path.abspath(__file__))[0]  # Program's diretory

#init debug print
global my_debug_print_var
my_debug_print_var=0
def dprint(content):
    global my_debug_print_var
    my_debug_print_var+=1
    print(content, end=" "+(1-my_debug_print_var%10)*"\n")
global room
# constants
FRAMES_PER_SEC = 120
PLAYER_SPEED = 12
MAX_SHOTS = 2
SHOT_SPEED = 10
ALIEN_SPEED = 12
ALIEN_ODDS = 45
EXPLODE_TIME = 6
SCREENRECT = Rect(0, 0, 800, 450)
SANS = os.path.join(main_dir, "fonts", "sans.ttf")
BETHOVEN = os.path.join(main_dir, "fonts", "bethoven.ttf")

# some globals for friendly access
dirtyrects = []  # list of update_rects
next_tick = 0  # used for timing


class Img: pass  # container for images

uis=os.listdir(main_dir+"/ui")
bgs=os.listdir(main_dir+"/bgs")
spr=os.listdir(main_dir+"/spr")

def quit():
    exit()

def clear_start():
    global main_title, buttons, screen, dirtyrects
    del main_title
    buttons=[]
    dirtyrects=[SCREENRECT]
    screen.fill(pygame.Color(0, 0, 0))

def goto_test():
    global room
    room="intro"

def draw_info():
    color = pygame.Color(255, 255, 255)

    text = "Игра 'Гарри Поттер и ИИ'"
    font = freetype.Font(SANS, 40)
    trender = font.render(text, color, )
    twidth, theight = trender[1][2], trender[1][3]
    font.render_to(screen,
                   (0, 0),
                   text,
                   pygame.Color(255, 255, 255),
                   None,
                   style=pygame.freetype.STYLE_STRONG
                   )

    text = "Разрабатывалась учеником лицея №1"
    trender = font.render(text, color, )
    twidth, theight = trender[1][2], trender[1][3]
    font.render_to(screen,
                   (0, 100),
                   text,
                   pygame.Color(255, 255, 255),
                   None,
                   style=pygame.freetype.STYLE_STRONG
                   )

    text = "В одиночку. в игре задействован"
    trender = font.render(text, color, )
    twidth, theight = trender[1][2], trender[1][3]
    font.render_to(screen,
                   (0, 300),
                   text,
                   pygame.Color(255, 255, 255),
                   None,
                   style=pygame.freetype.STYLE_STRONG
                   )

    text = "Базовый пример обучаемой нейросети."
    trender = font.render(text, color, )
    twidth, theight = trender[1][2], trender[1][3]
    font.render_to(screen,
                   (0, 400),
                   text,
                   pygame.Color(255, 255, 255),
                   None,
                   style=pygame.freetype.STYLE_STRONG
                   )

    text = "Берсенёвым Ильёй Ивановичем"
    trender = font.render(text, color, )
    twidth, theight = trender[1][2], trender[1][3]
    font.render_to(screen,
                   (0, 200),
                   text,
                   pygame.Color(255, 255, 255),
                   None,
                   style=pygame.freetype.STYLE_STRONG
                   )



# first, we define some utility functions

def load_image(file, transparent):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' %
                         (file, pygame.get_error()))
    if transparent:
        corner = surface.get_at((0, 0))
        surface.set_colorkey(corner, RLEACCEL)
    return surface.convert()


# The logic for all the different sprite types

class Actor:
    "An enhanced sort of sprite class"

    def __init__(self, image, x, y, xscale, yscale, text, font_type=SANS):
        if image is not None:
            self.image = image
            self.rect = image.get_rect()
            self.rect[0]=x
            self.rect[1]=y
            self.rect[2] *= xscale
            self.rect[3] *= yscale
            self.rect[0] -= int(self.rect[2] / 2)
            self.rect[1] -= int(self.rect[3] / 2)
        else:
            self.image=None
            self.rect = pygame.Rect(x,y,100,100)
        self.font_size=40
        self.text=text
        self.foname=font_type
        self.font = freetype.Font(self.foname, self.font_size)

        self.color=pygame.Color(0, 0, 0, 0)




    def update(self):
        "update the sprite state for this frame"
        pass

    def draw(self, screen):
        "draws the sprite into the screen"
        self.transformed_image=pygame.transform.scale(self.image, (self.rect[2],self.rect[3])) #scale img
        if self.color[3]!=0:
            self.transformed_image.fill(self.color, None, BLEND_RGBA_ADD)
        r = screen.blit(self.transformed_image, (self.rect[0],self.rect[1]))
        dirtyrects.append(r)

    def erase(self, screen, background):
        "gets the sprite off of the screen"
        r = screen.blit(background, self.rect, self.rect)
        dirtyrects.append(r)

    def draw_text(self, screen, color1=pygame.Color(100, 10, 30, 255), color2=pygame.Color(40, 10, 40, 255), style=pygame.freetype.STYLE_STRONG):


        color1[3] = 255 - self.color[3]
        color2[3] = 255 - self.color[3]

        "draws the text into the screen"
        self.font = freetype.Font(self.foname, self.font_size)

        self.font.underline_adjustment = 0
        self.font.pad = False
        self.trender=self.font.render(self.text,  self.color, )
        self.twidth, self.theight = self.trender[1][2], self.trender[1][3]
        if self.image==None:
            dprint("yeet.")

        d=self.font.render_to(screen,
                            (self.rect[0] + self.rect[2] / 2 - self.twidth / 2-3,
                             self.rect[1] + self.rect[3] / 2 - self.theight / 2),
                            self.text,
                            color1,
                            None,
                            style=style
                            )

        self.font.render_to(screen,
                            (self.rect[0]+self.rect[2]/2-self.twidth/2,
                             self.rect[1]+self.rect[3]/2-self.theight/2),
                            self.text,
                            color2,
                            None,
                            style=style
                            )
        if self.image==None and self.text!="Гарри Поттер И ИИ":
            self.rect[2]=d.width
            self.rect[3]=d.height
        #dirtyrects.append(pygame.Rect(self.rect[0], self.rect[1], self.trender[1][2], self.trender[1][3]))
        dirtyrects.append(pygame.Rect(0,0,800,450))

class MagicBox(Actor):
    def getdiffs(self, col1, col2):
        diffs = []
        for i in range(3):
            try:
                diffs.append([abs(col1[i] - col2[i]), -int(abs(col1[i] - col2[i]) / (col1[i] - col2[i]))])  # diff, sign
            except:
                diffs.append([abs(col1[i] - col2[i]), 0])  # diff, sign=0
        return diffs

    def __init__(self, x, y, sprite):
        Actor.__init__(self, sprite, x, y, 1, 1, "")
        self.inputs=[0]*28*28
        self.stepvar=0
        self.speed=30
        self.colors=[]
        self.diffs=[]
        for i in range(28*28):
            self.colors.append(random.choice([[219,182,19], [118,66,138]]))
            self.diffs.append(self.getdiffs(self.colors[i],self.colors[i]))

    def tupletoarr(self, tuple_):
        a = []
        for i in tuple_:
            a.append(i)
        return a



    def changecol(self, curcol, speed, diffs):
        curcol[0] += min(round(diffs[0][0] / speed * diffs[0][1]), 255)
        curcol[1] += min(round(diffs[1][0] / speed * diffs[1][1]), 255)
        curcol[2] += min(round(diffs[2][0] / speed * diffs[2][1]), 255)
        retcol=[round(curcol[0]),round(curcol[1]),round(curcol[2])]
        return retcol

    def step(self, screen):
        r = screen.blit(background, self.rect, self.rect)
        dirtyrects.append(r)
        self.stepvar+=1
        if self.rect[1] < mouse_y < self.rect[1] + self.rect[3] and \
                    self.rect[0] < mouse_x < self.rect[0] + self.rect[2]:
            if btnpressing==1:
                tempx=((mouse_x-self.rect[0]-10)//10)
                tempy=((mouse_y-self.rect[1]-10)//10)

                if tempx==-1: tempx=0
                if tempy==-1: tempy=0
                if tempx==28: tempx=27
                if tempy==28: tempy=27
                self.inputs[28*tempy+tempx]=1
                if 28*tempy+tempx<len(self.inputs)-1:

                    if tempx>0:
                        if (tempy*28)//28==(tempy*28+tempx-1)//28:
                            self.inputs[28*tempy+tempx-1]=1
                    if 0<tempx<self.rect[2]:
                        if (tempy*28)//28==(tempy*28+tempx+1)//28:
                            self.inputs[28*tempy+tempx+1]=1
                    if tempy>0:
                        if (tempy*28+tempx)%28==((tempy-1)*28+tempx)%28:
                            self.inputs[28*(tempy-1)+tempx]=1
                    if tempy>0 and tempy*10+20<self.rect[3]   and                      28*(tempy+1)+tempx <  len(self.inputs)-1:
                        if (tempy*28+tempx)%28==((tempy+1)*28+tempx)%28:
                            self.inputs[28*(tempy+1)+tempx]=1
        if eventname=="MouseButtonUp" and eventparams['button']==1 and self.inputs!=[0]*28*28 and max(self.inputs)!=0 and self.inputs.count(1)>10:
            max_=0
            pos=0
            tempmas=n.query(self.inputs)
            for i in range(len(tempmas)):
                if tempmas[i][0]>max_:
                    max_=tempmas[i][0]
                    pos=i
            magic=['silencio','accio','alohomora']
            return magic[pos]



        largpix = pygame.Surface((10, 10))

        yellow, violet=[219,182,19], [118,66,138]


        reload=1
        for i in range(len(self.inputs)):
            if self.inputs[i]==1:
                if self.colors[i]==yellow:
                    self.diffs[i]=self.getdiffs(self.colors[i],violet)
                if self.colors[i]==violet:
                    self.diffs[i]=self.getdiffs(self.colors[i],yellow)
                self.colors[i]=self.changecol(self.colors[i],30,self.diffs[i])

                largpix.fill(( min(abs(round(self.colors[i][0])),255), min(abs(round(self.colors[i][1])),255), min(abs(round(self.colors[i][2])),255) ))
                screen.blit(largpix, ((i%28)*10+self.rect[0]+10, (i//28)*10+self.rect[1]+10))
        return None

class Button(Actor):
    "Destroy him or suffer"
    def __init__(self,text, x, y, xscale, yscale, sprite, function=None):
        Actor.__init__(self, sprite, x, y, xscale, yscale, text)
        #self.pressed = 0
        self.hover = 0
        self.text=text
        self.function=function

    def pressed(self):
        if self.function is not None:
            exec(str(self.function)+"()")

class initializator():

    def init_main_window(self):
        global background, buttons, alpha, screen, main_title, initor
        #darking init
        alpha=1

        #bg init
        background = pygame.Surface(SCREENRECT.size)
        background.blit(Img.bg_main, (0, 0))
        screen.blit(background, (0, 0))
        pygame.display.flip()

        # buttons init
        buttons = [Button("начать", 400, 270, 1, 1, Img.ui_button_long, "goto_test(); clear_start"),
                   Button("инфо", 400, 340, 1, 1, Img.ui_button_long,  "clear_start(); draw_info"),
                   Button("выйти", 400, 410, 1, 1, Img.ui_button_long, "quit")]


        main_title = Actor(None, 320, 10, 1, 1, "Гарри Поттер И ИИ", font_type=BETHOVEN)



def main():
    global background, buttons, alpha, screen, initor, main_title, room,  dirtyrects, mouse_x, mouse_y, eventname, eventparams, screen, block, reload, btnpressing
    room="menu"
    huetic=0
    dialogcounter = 0
    reload=0
    block=0
    temptemp=0
    btnpressing = 0
    thirteencounter=0

    # Initialize SDL components
    pygame.init()
    screen = pygame.display.set_mode(SCREENRECT.size, 0)
    clock = pygame.time.Clock()

    #loadresses
    for pic in uis:
        if pic[0:7]=="ui_help"[0:7] and pic[0:13]!="ui_help_neuro"[0:13]:
            exec("Img." + str(pic[:pic.find(".")]) + "=load_image('" + main_dir.replace("\\", "/") + "/ui/" + str(
                pic) + "' , 1)")
            continue
        elif pic[0:13]=="ui_help_neuro"[0:13]:
            exec("Img." + str(pic[:pic.find(".")]) + "=load_image('" + main_dir.replace("\\", "/") + "/ui/" + str(
                pic) + "' , 0)")
            continue

        exec("Img."+str(pic[:pic.find(".")])+"=load_image('"+main_dir.replace("\\","/")+"/ui/"+str(pic)+"' , 1)" )

    for pic in bgs:
        exec("Img."+str(pic[:pic.find(".")])+"=load_image('"+main_dir.replace("\\","/")+"/bgs/"+str(pic)+"' , 0)" )

    for pic in spr:
        exec("Img."+str(pic[:pic.find(".")])+"=load_image('"+main_dir.replace("\\","/")+"/spr/"+str(pic)+"' , 1)" )

    initor = initializator()
    initor.init_main_window()

    while True:
        #uservars init
        huetic+=2
        if reload>0:
            clock.tick(FRAMES_PER_SEC)
            reload-=1
            continue

        if reload<0: block=0
        mainhue = round(math.cos(huetic/31.4)*70+80)




        dialogs=[ "Гарри, вот ты где!",  #dd                                                          0                                              |
                  "Я тебя повсюду разыскиваю.",  #dd                                                  1                                                      |
                  "Быстрее направляйся в класс заклинаний, Люпин вовсю ведёт урок",  #dd              2                                                                                          |
                  "Люпин в Хогварце?",  #harry                                                        3                                                |
                  "Да, ненадолго. Обучает заклинаниям.",  #dd                                         4                                                               |
                  "Уже иду!",  #harry                                                                 5                                       |
                  "Извините, я опоздал. Можно зайти?",  # harry                                       6                                |
                  "Да, конечно. Сегодня мы изучаем 3 новых заклинания.",  # Lupin                     7                                |
                  "Дети, это заклинание называется алохомора.",  #lupintoclass
                  "чтобы его совершить проведите так палочкой",   #screen.blit ()scheme                                                                       8                          |
                  "это заклинание называется акцио.",  # lupintoclass
                  "Для него нужен лишь короткий взмах",  #screen.blit ()scheme
                  "А это заклинание называется силенцио.",  # lupintoclass
                  "Оно уже посложнее предыдущих", #screen.blit ()scheme
                  "Поттер, попробуй акцио. ", #создать инстанс капчурера
                  ["хорошо, теперь попробуй алохомору  ",  "хорошо, теперь попробуй силенцио "], #l
                  "Но профессор, как вы поняли, какое заклинание я применил?", #g
                  "Вы же всего лишь картинка в программе!", #g
                  "Как и ты. Дело в том, что твоё заклинание обрабатывает нейросеть.", #l блит имэг
                  "Вначале она принимает на вход 784 фрагмента твоего заклинания.", #l
                  "Затем она обрабатывает его и один из 3 выходных нейронов срабатывает.", #l
                  "На обучение этой нейросети потребовалось 150 тестов.", #l
                  "После тестов связи между нейронами корректируются для корректной работы.", #l
                  "Игра окончена. Для большей информации кликните на кнопку в меню 'инфо'", #l
                  ""
                  ]





        faces=[ [Img.potter0, Img.double_door1],
                [Img.potter0, Img.double_door1],
                [Img.potter0, Img.double_door1],
                [Img.potter1, Img.double_door0],
                [Img.potter0, Img.double_door1],
                [Img.potter1, Img.double_door0],
                [Img.potter1, Img.lupin0],
                [Img.potter0, Img.lupin1],
                [Img.lupin1, None],
                [Img.lupin1, None],
                [Img.lupin1, None],
                [Img.lupin1, None],
                [Img.lupin1, None],
                [Img.lupin1, None],
                [Img.lupin1, None],
                [Img.lupin1, None],
                [Img.potter1, Img.lupin0],
                [Img.potter1, Img.lupin0],
                [Img.potter0, Img.lupin1],
                [Img.potter0, Img.lupin1],
                [Img.potter0, Img.lupin1],
                [Img.potter0, Img.lupin1],
                [Img.potter0, Img.lupin1],
                [None,None],
                [None,None]
                ]





        actions=[None,
                 None,
                 None,
                 None,
                 None,
                 None,
                 None,
                 None,
                 "screen.blit(Img.ui_help_alohomora, (400-140,0)); block=1; reload=900",
                 None,
                 "screen.blit(Img.ui_help_accio, (400-140,0)); block=1; reload=900",
                 None,
                 "screen.blit(Img.ui_help_silencio, (400-140,0)); block=1; reload=15000",
                 None,
                 None,
                 None,
                 None,
                 None,
                 "screen.blit(Img.ui_help_neuro_struct, (400-140,0)); block=1; reload=900",
                 None,
                 None,
                 None,
                 None,
                 None,
                 "exit()"
                 ]

        backs=[Img.bg_coridor,
               Img.bg_coridor,
               Img.bg_coridor,
               Img.bg_coridor,
               Img.bg_coridor,
               Img.bg_coridor,
               Img.bg_class_new,
               Img.bg_class_new,]

        for i in range(len(dialogs)):
            if type(dialogs[i]) is not list:
                dialogs[i]=dialogs[i]+" "


        #
        clock.tick(FRAMES_PER_SEC)

        # Gather Events (idk what means gather)
        pygame.event.pump()
        keystate = pygame.key.get_pressed()
        if keystate[K_ESCAPE] or pygame.event.peek(QUIT):
            break
        mouse_x, mouse_y=pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
        #

        # buttons hover
        for btnhover in buttons:
            if btnhover.rect[1] <= mouse_y <= btnhover.rect[1] + btnhover.rect[3] and \
                    btnhover.rect[0] <= mouse_x <= btnhover.rect[0] + btnhover.rect[2]:
                btnhover.color = (230, 230, 230, 128)
            else:
                btnhover.color = (255, 255, 255, 0)
        #

        # geteventinfo
        for e in pygame.event.get():

            eventname, eventparams = 0,0
            if e.type != MOUSEMOTION:
                eventname, eventparams = pygame.event.event_name(e.type), e.dict
            #

            #buttonspressing
            if eventname=="MouseButtonUp" and eventparams['button']==1:
                for chckprss in buttons:
                    if      chckprss.rect[1]<= mouse_y <= chckprss.rect[1]+chckprss.rect[3] and \
                            chckprss.rect[0]<= mouse_x <= chckprss.rect[0]+chckprss.rect[2]:
                        chckprss.pressed()
            if eventname=="MouseButtonDown" and eventparams['button']==1:
                btnpressing=1
            if eventname=="MouseButtonUp" and eventparams['button']==1:
                btnpressing=0
            #

        # dialog draw
        if room == "intro":
            if dialogcounter>15:
                block=0
            try:

                #pygame.display.update(SCREENRECT)
                mbox.update()
                temp=mbox.step(screen)
                mbox.draw(screen)
                pygame.display.update(SCREENRECT)
                block = 1
                if temp == "accio":
                    del mbox
                    print(temp)
                    block=0
                    dialogcounter=15

                if temp == "alohomora" and dialogcounter==15:
                    del mbox
                    print(temp)
                    block = 0
                    thirteencounter=1

                if temp == "silencio" and dialogcounter==15 and thirteencounter==1:
                    del mbox
                    print(temp)
                    block = 0
                    dialogcounter=16



            except Exception as e:

                if dialogcounter == 14 or dialogcounter == 15:
                    print(e)
                    mbox = MagicBox(250+280/2, 10+280/2, Img.ui_capturer)

                    mbox.draw(screen)
                    mbox.step(screen)
                    dirtyrects=[]
                    dirtyrects.append(SCREENRECT)


            try:
                currback = backs[dialogcounter]
            except:
                pass
            background=currback
            if dialogcounter!= 14 and dialogcounter!=15:
                screen.blit(background,(0,0))

            # next text and pictures when press
            if eventname == "MouseButtonDown" and eventparams['button'] == 1 and reload <= 0 and block != 1 and dialogcounter!=15  and dialogcounter!=14 :
                reload = 50
                dialogcounter += 1
                dprint(dialogcounter)
            #


            for btnhover in buttons:
                if btnhover.rect[1] <= mouse_y <= btnhover.rect[1] + btnhover.rect[3] and \
                        btnhover.rect[0] <= mouse_x <= btnhover.rect[0] + btnhover.rect[2]:
                    btnhover.color = (230, 230, 230, 128)
                else:
                    btnhover.color = (255, 255, 255, 0)

            for actor in buttons:
                actor.draw_text(screen)



            LETTERAMOUNT=29

            if dialogcounter != 15:
                diatext = [
                    dialogs[dialogcounter][0
                                           :
                                           dialogs[dialogcounter].rfind(" ",0,LETTERAMOUNT)],

                    dialogs[dialogcounter][dialogs[dialogcounter].rfind(" ",0,LETTERAMOUNT)+1
                                           :
                                           dialogs[dialogcounter].rfind(" ", dialogs[dialogcounter].rfind(" ",0,LETTERAMOUNT),  dialogs[dialogcounter].rfind(" ",0,LETTERAMOUNT)+LETTERAMOUNT)],

                    dialogs[dialogcounter][dialogs[dialogcounter].rfind(" ", dialogs[dialogcounter].rfind(" ",0,LETTERAMOUNT),  dialogs[dialogcounter].rfind(" ",0,LETTERAMOUNT)+LETTERAMOUNT)+1
                                           :
                                           LETTERAMOUNT*4]
                    ]
            else:

                diatext = [
                    dialogs[dialogcounter][thirteencounter][0
                                           :
                                           dialogs[dialogcounter][thirteencounter].rfind(" ", 0, LETTERAMOUNT)],

                    dialogs[dialogcounter][thirteencounter][dialogs[dialogcounter][thirteencounter].rfind(" ", 0, LETTERAMOUNT) + 1
                                           :
                                           dialogs[dialogcounter][thirteencounter].rfind(" ", dialogs[dialogcounter][thirteencounter].rfind(" ", 0,
                                                                                                          LETTERAMOUNT),
                                                                        dialogs[dialogcounter][thirteencounter].rfind(" ", 0,
                                                                                                     LETTERAMOUNT) + LETTERAMOUNT)],

                    dialogs[dialogcounter][thirteencounter][
                    dialogs[dialogcounter][thirteencounter].rfind(" ", dialogs[dialogcounter][thirteencounter].rfind(" ", 0, LETTERAMOUNT),
                                                 dialogs[dialogcounter][thirteencounter].rfind(" ", 0, LETTERAMOUNT) + LETTERAMOUNT) + 1
                    :
                    LETTERAMOUNT * 4]
                ]


            font = freetype.Font(SANS, 40)
            #draw faces
            if faces[dialogcounter][0] is not None :
                screen.blit(pygame.transform.scale(faces[dialogcounter][0], (256,256)), (0,450-150-256+50))
            if faces[dialogcounter][1] is not None :
                mirroredimg=pygame.transform.flip(faces[dialogcounter][1], True, False)
                screen.blit(pygame.transform.scale(mirroredimg,(256,256)), (800-256, 450-150-256+50))
            #
            if True:
                screen.blit(pygame.transform.scale(Img.ui_dialog_bg,(Img.ui_dialog_bg.get_width() * 2, Img.ui_dialog_bg.get_height() * 2)), (0, 450 - 150))  # dialogbg
                dirtyrects.append(SCREENRECT)

            yoffset=5
            for text in diatext:
                #dprint(yoffset)
                font.render_to(screen,
                               (10, 450 - 150 + 10 + yoffset),
                               text, pygame.Color(200, 50, 200, 230),None,style=pygame.freetype.STYLE_STRONG
                               )
                font.render_to(screen,
                               (10, 450 - 150 + 11 + yoffset),
                               text, pygame.Color(200, 0, 50, 150), None, style=pygame.freetype.STYLE_STRONG
                               )
                yoffset += 40
            curraction = actions[dialogcounter]
            if curraction is not None:
                exec(curraction)



        #

        # Clear screen and update actors
        if room != "intro":
            for actor in buttons:
                actor.erase(screen, background)
                actor.update()
            try:
                for actor in [main_title]:
                    actor.erase(screen, background)
                    actor.update()
            except:
                pass
            #
            # Draw everybody

            for actor in buttons:
                actor.draw(screen)
                actor.draw_text(screen)
            try:
                main_title.font_size=100
                main_title.draw_text(screen, color2=pygame.Color(mainhue%255, min((50+mainhue)%255, 255) , min((70+mainhue)%255,255),255), color1=pygame.Color(30,30,30), style=pygame.freetype.STYLE_DEFAULT)
            except:
                pass
        #dirtyrects.append(SCREENRECT)
        pygame.display.update(dirtyrects)
        dirtyrects = []
        #

    pygame.time.wait(50)

    #print(dir(Img))
main()