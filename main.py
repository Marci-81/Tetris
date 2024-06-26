from random import *
import threading
from tkinter import *
from PIL import ImageTk , Image
from time import *
from random import *
from keyboard import *

"""
34x34 pixel per block
root.geometry("1366x748")
 
"gold point": referenc point
"""

class tetris:
    def __init__(self):
        self.gamewidht = 680
        self.gamehigh = 748

        self.root = Tk()
        self.root.title("Tetris")
        self.root.iconbitmap("tetris.ico")
        self.root.protocol("WM_DELETE_WINDOW", self.exit)

        self.redsquare = ImageTk.PhotoImage(Image.open("red_block.png"))
        self.bluesquare = ImageTk.PhotoImage(Image.open("blue_block.png"))
        self.greensquare = ImageTk.PhotoImage(Image.open("green_block.png"))
        self.yellowsquare = ImageTk.PhotoImage(Image.open("yellow_block.png"))
        self.orangesquare = ImageTk.PhotoImage(Image.open("orange_block.png"))
        self.border = ImageTk.PhotoImage(Image.open("border.png"))
        self.backround = ImageTk.PhotoImage(Image.open("backround.png"))
        self.title_backround = ImageTk.PhotoImage(Image.open("title_backround.png"))

        self.score = 0
        self.lines = 0
        self.shapes = ["P","L","I","S","Z","O","T"] #T, O, I, L, P
        self.currentshape = None
        self.allcolors = [self.redsquare,self.bluesquare,self.greensquare,self.yellowsquare,self.orangesquare,self.backround]
        self.allcolorsletter = ["r","b","g","y","o","x"]

        self.gameplace = [["+" for _ in range(12)] for _ in range(22)] #x[row;0-10][column;0-20]
        self.startgoldpoint = [1, 6]
        self.goldpoint = self.startgoldpoint.copy()
        self.phase = 0
        self.again = False

        self.nextshape = choice(self.shapes)
        color = randint(0,4)
        self.nextcolor = self.allcolors[color]
        self.nextlettercolor = self.allcolorsletter[color]

        for n_row,row in enumerate(self.gameplace):
            for n_column,column in enumerate(row):
                if (n_row != 0) and (n_row != 21):
                    if (n_column != 0) and (n_column != 11):
                        row.pop(n_column)
                        row.insert(n_column, "x")
                n_column += 1
            n_row += 1

        self.runthreads = "0" # "1" - running ; "0" - not.
        self.run = True

    #buttons:
    def onpress(self,acticity):
        if acticity == "down":
            self.goldpoint[0] += 1
        elif acticity == "left":
            if self.goldpoint[1] != 1:
                self.goldpoint[1] -= 1
        elif acticity == "right":
            if self.goldpoint[1] != 11:
                self.goldpoint[1] += 1
        elif acticity == "l_left":
            if self.phase != 0: self.phase -= 1
            else: self.phase = 3
        elif acticity == "r_right":
            if self.phase != 3: self.phase += 1
            else: self.phase = 0

    def keychecker(self):
        add_hotkey("down_arrow",lambda:self.onpress("down"),suppress=True)
        add_hotkey("left_arrow",lambda:self.onpress("left"),suppress=True,trigger_on_release=True)
        add_hotkey("right_arrow",lambda:self.onpress("right"),suppress=True,trigger_on_release=True)
        add_hotkey("y",lambda:self.onpress("l_left"),suppress=True,trigger_on_release=True)
        add_hotkey("x",lambda:self.onpress("r_right"),suppress=True,trigger_on_release=True)

    def makegameborder(self):
        self.root.minsize(self.gamewidht, self.gamehigh)
        self.root.maxsize(self.gamewidht, self.gamehigh)

        for column in range(12):
            for row in range(22):
                if (column == 0 or column == 11) or (row == 0 or row == 21):
                    Label(self.root,image=self.border,bd=0).grid(row=row, column=column)
                else: Label(self.root,image=self.backround,bd=0).grid(row=row, column=column)

        #GUI
        #title border
        for row in range(4):
            for column in range(8):
                if ((row == 1 or row == 3) and 0<column<7) == False:
                    Label(self.root,image=self.border,bd=0).grid(row=row,column=12+column)

        #title
        Label(self.root,image=self.title_backround,bd=0).grid(row=1,column=13,columnspan=6)
        Label(self.root,text="TETRIS",background="black",foreground="white",font=1,bd=0).grid(row=1,column=13,columnspan=6)

        #shape box border
        def shapeboxborder(inside = 0):
            if inside: square = self.backround
            else: square = self.border
            for row in range(4+inside, 12-inside):  # row
                for column in range(12+inside, 20-inside):  # column
                    if inside: self.root.grid_slaves(row=row,column=column)
                    Label(self.root,image=square, bd=0).grid(row=row, column=column)
        shapeboxborder()
        shapeboxborder(1)

    def nextshapebox(self):
        for row in range(6):
            for column in range(6):
                Label(image=self.backround,bd=0).grid(row=row+5,column=column+13)
                self.root.grid_slaves(row=5+row,column=13+column)[0].configure(image=self.backround,bd=0)

        if self.nextshape == "O":
            for row in range(2):
                for column in range(2):
                    self.root.grid_slaves(row=7+row,column=15+column)[0].configure(image=self.nextcolor,bd=0)
        elif self.nextshape == "T":
            for row in range(0,2):
                for column in range(0,3):
                    if (row == 1) and (column == 0 or column == 2):continue
                    Label(image=self.nextcolor,bd=0).grid(row=row+7,column=14+column,columnspan=2)
        elif self.nextshape == "L" or self.nextshape == "P":
            if self.nextshape == "L": i = -1
            else: i = 1
            for row in range(2):
                for column in range(-1,2):
                    if (row == 1) and (column == 0 or column == -1*i):continue
                    Label(image=self.nextcolor, bd=0).grid(row=row + 7, column=15 + column, columnspan=2)
        elif self.nextshape == "I":
            for column in range(4):
                Label(image=self.nextcolor,bd=0).grid(row=7,rowspan=2,column=14+column)
        elif self.nextshape == "S" or self.nextshape == "Z":
            if self.nextshape == "S": i = -1
            else: i = 1
            for row in range(2):
                for column in range(-1,2):
                    if (row == 0 and column == -1*i) or (row == 1 and column == 1*i): continue
                    Label(image=self.nextcolor,bd=0).grid(row=row+7,column=15+column,columnspan=2)

    def scores(self,first=False):
        #every time its score gets change, that function need to be called
        if first:
            Label(self.root, image=self.title_backround, bd=0).grid(row=3, column=13, columnspan=6)
            Label(self.root,text=f"{self.score} Points, {self.lines} Line",background="black",foreground="white",font=1,bd=0).grid(row=3, column=13,columnspan=6)
        else:
            self.root.grid_slaves(row=3, column=13)[0].destroy()
            Label(self.root, text=f"{self.score} Points, {self.lines} Line", background="black", foreground="white", font=1, bd=0).grid(row=3, column=13, columnspan=6)
            #self.root.grid_slaves(row=3, column=13, columnspan=6)[0].configure(text=f"{self.score} Points",background="black",foreground="white",font=1, bd=0)

    def checklines(self):
        lines = list()
        for i,row in enumerate(self.gameplace):
            if row[1] == "+": continue
            n = 0
            for j,column in enumerate(row):
                if column == "x":
                    n +=1
            if n == 0:
                lines.append(i)
        self.lines += len(lines)

        if len(lines)>0:
            self.score += round((100 * len(lines)) * (0.75+0.25*len(lines)))
            self.scores()
            for line in lines:
                shallow = self.gameplace[:]
                self.gameplace.remove(shallow[line])
                self.gameplace.insert(1,list("x" for _ in range(10)))
                self.gameplace[1].insert(0,"+")
                self.gameplace[1].insert(11, "+")

            for i,row in enumerate(self.gameplace):
                for j,column in enumerate(row):
                    if column != "+":
                        self.root.grid_slaves(row=i,column=j)[0].configure(image=self.allcolors[self.allcolorsletter.index(column)], bd=0)

    def square_manage(self,position,activity=0,color=None):
        #activity: check/place/remove squares from matrix/add place holder in matrix
        #position: [row,cloumn]
        if self.runthreads == "0": return
        if activity == 0: #check for place
            if self.gameplace[position[0]][position[1]] == "x":
                return True
            else:
                return False
        elif activity == 1: #already checked, place the squares
            self.root.grid_slaves(row=position[0], column=position[1])[0].configure(image=color,bd=0)
            for row in range(len(self.gameplace)):
                for column in range(len(self.gameplace[0])):
                    if (row == position[0]) and (column == position[1]):
                        self.gameplace[row].pop(column)
                        self.gameplace[row].insert(column,self.lettercolor)

        elif activity == 2: #delete the painted squares
            self.root.grid_slaves(row=position[0], column=position[1])[0].configure(image=self.backround,bd=0)

        elif activity == 3: #delet from the matrix list
            for row in range(len(self.gameplace)):
                for column in range(len(self.gameplace[0])):
                    if (row == position[0]) and (column == position[1]):
                        self.gameplace[row].pop(column)
                        self.gameplace[row].insert(column,"x")

    def shape_manage(self,gp,activity,rotatecheck=False):
        #activity 0/1/2/3: check/place/remove paint/remove from matrix
        # shape:~ ; color:~ ; goldpoint:already said ;
        # delete:remove previous shape ; phase:rotation phase
        n = 0 #for checking
        shape = self.currentshape
        color = self.currentcolor
        if rotatecheck: phase = self.phase
        else: phase = self.currentphase

        if shape == "O": #["P","L","I","S","Z","O","T"]
            for row in range(2):#row
                for column in range(2):#column
                    if activity == 0:
                        if self.square_manage(position=[gp[0]+row,gp[1]-column],activity=0):
                            n+=1
                    else: self.square_manage([gp[0]+row,gp[1]-column],activity,color)

        elif shape == "T":
            if phase == 0:
                for column in range(-1,2):
                    for row in range(0,2):
                        if (row == 1) and (column == -1 or column == 1): continue
                        if activity == 0:
                            if self.square_manage(position=[gp[0] + row, gp[1] - column], activity=0):
                                n += 1
                        else: self.square_manage([gp[0]+row,gp[1]-column],activity,color)
            elif phase == 1:
                for row in range(-1,2):
                    for column in range(0,2):
                        if (column == 1) and (row == -1 or row == 1): continue
                        if activity == 0:
                            if self.square_manage(position=[gp[0] + row, gp[1] - column], activity=0):
                                n += 1
                        else: self.square_manage([gp[0]+row,gp[1]-column],activity,color)
            elif phase == 2:
                for column in range(-1,2):
                    for row in range(-1,1):
                        if (row == -1) and (column == -1 or column == 1): continue
                        if activity == 0:
                            if self.square_manage(position=[gp[0] + row, gp[1] - column], activity=0):
                                n += 1
                        else: self.square_manage([gp[0]+row,gp[1]-column],activity,color)
            elif phase == 3:
                for row in range(-1, 2):
                    for column in range(-1, 1):
                        if (column == -1) and (row == -1 or row == 1): continue
                        if activity == 0:
                            if self.square_manage(position=[gp[0] + row, gp[1] - column], activity=0):
                                n += 1
                        else: self.square_manage([gp[0] + row, gp[1] - column], activity, color)

        elif shape == "I":
            if phase % 2 == 0:
                for column in range(-1,3):
                    if activity == 0:
                        if self.square_manage(position=[gp[0], gp[1] - column], activity=0):
                            n+=1
                    else: self.square_manage([gp[0], gp[1] - column], activity, color)
            else:
                for row in range(-2,2):
                    if activity == 0:
                        if self.square_manage(position=[gp[0]+row, gp[1]], activity=0):
                            n+= 1
                    else: self.square_manage([gp[0] + row, gp[1]], activity, color)

        elif shape == "L" or shape == "P":
            if shape == "L": i = 1
            else: i = -1
            if phase == 0:
                for column in range(-1, 2):
                    for row in range(0, 2):
                        if (row == 1) and (column == -1*i or column == 0): continue
                        if activity == 0:
                            if self.square_manage(position=[gp[0] + row, gp[1] - column], activity=0):
                                n += 1
                        else:
                            self.square_manage([gp[0] + row, gp[1] - column], activity, color)
            elif phase == 1:
                for row in range(-1, 2):
                    for column in range(0, 2):
                        if (column == 1) and (row == 1*i or row == 0): continue
                        if activity == 0:
                            if self.square_manage(position=[gp[0] + row, gp[1] - column], activity=0):
                                n += 1
                        else:
                            self.square_manage([gp[0] + row, gp[1] - column], activity, color)
            elif phase == 2:
                for column in range(-1, 2):
                    for row in range(-1, 1):
                        if (row == -1) and (column == 0 or column == 1*i): continue
                        if activity == 0:
                            if self.square_manage(position=[gp[0] + row, gp[1] - column], activity=0):
                                n += 1
                        else:
                            self.square_manage([gp[0] + row, gp[1] - column], activity, color)
            elif phase == 3:
                for row in range(-1, 2):
                    for column in range(-1, 1):
                        if (column == -1) and (row == -1*i or row == 0): continue
                        if activity == 0:
                            if self.square_manage(position=[gp[0] + row, gp[1] - column], activity=0):
                                n += 1
                        else:
                            self.square_manage([gp[0] + row, gp[1] - column], activity, color)
        elif shape == "S" or shape == "Z":
            if shape == "S": i = 1
            else: i = -1
            if phase % 2 == 0:
                for row in range(2):
                    for column in range(-1,2):
                        if not ((row == 0 and column == -1*i) or (row == 1 and column == 1*i)):
                            if activity == 0:
                                if self.square_manage(position=[gp[0] + row, gp[1] - column], activity=0):
                                    n += 1
                            else:
                                self.square_manage([gp[0] + row, gp[1] - column], activity, color)
            else:
                for row in range(-1,2):
                    for column in range(0,2):
                        if not ((row == -1*i and column == 1) or (row == 1*i and column == 0)):
                            if activity == 0:
                                if self.square_manage(position=[gp[0] + row, gp[1] - column], activity=0):
                                    n += 1
                            else:
                                self.square_manage([gp[0] + row, gp[1] - column], activity, color)

        if activity == 0:
            if n == 4:
                return True
            else: return False

    def thegame(self):
        sleep(1)
        self.gamespeed = 0.45
        self.round = 0
        self.multiply = 3/1800

        while int(self.runthreads):
            print(self.round,self.gamespeed-self.round*self.multiply)
            self.currentcolor = self.nextcolor
            self.lettercolor = self.nextlettercolor
            color = randint(0,4)
            self.nextcolor = self.allcolors[color]
            self.nextlettercolor = self.allcolorsletter[color]

            self.currentshape = self.nextshape
            self.nextshape = choice(self.shapes)

            self.phase = 0
            self.currentphase = self.phase

            self.startgoldpoint = [1,6]
            self.goldpoint = self.startgoldpoint.copy()
            last_gp = self.startgoldpoint.copy()
            generated = True
            placed = False
            start = time()

            if not self.shape_manage(activity=0,gp=self.startgoldpoint):
                print("lost")
                self.again=True
                Button(text="start new game", command=self.start).grid(row=12, column=12, columnspan=8)
                return

            self.nextshapebox()

            while generated and int(self.runthreads): #object spawn and moving
                if time() - start > self.gamespeed-self.round*self.multiply: #if time is passed
                    start = time()
                    self.shape_manage(activity=2,gp=last_gp)
                    self.shape_manage(activity=3,gp=last_gp)
                    last_gp[0] += 1
                    self.goldpoint[0] += 1
                    placed = False
                else:
                    if self.shape_manage(activity=0,gp=last_gp) or placed:
                        if not placed:
                            self.shape_manage(activity=1,gp=last_gp)
                            placed = True

                        if last_gp != self.goldpoint: #buttons: move
                            if self.goldpoint[0] != last_gp[0]: #down
                                self.shape_manage(activity=3,gp=last_gp) #remove from matrix temporarily
                                last_gp[0] += 1
                                if self.shape_manage(activity=0,gp=last_gp): #check new place
                                    last_gp[0] -= 1
                                    self.shape_manage(activity=2,gp=last_gp) #remove  last painted
                                    last_gp[0] += 1
                                    self.goldpoint = last_gp.copy()
                                    self.shape_manage(activity=1,gp=last_gp) #place new shape
                                else: #if not placeable
                                    last_gp[0] -=1
                                    self.goldpoint = last_gp.copy()
                                    self.shape_manage(activity=1,gp=last_gp)
                                    self.checklines()
                                    generated = False

                            if self.goldpoint[1] != last_gp[1]: #left/right
                                if self.goldpoint[1] < last_gp[1]: #left
                                    self.shape_manage(activity=3,gp=last_gp) #remove from matrix
                                    last_gp[1] -= 1
                                    if self.shape_manage(activity=0,gp=last_gp): #check new place
                                        last_gp[1] += 1
                                        self.shape_manage(activity=2,gp=last_gp) #remove  last painted
                                        last_gp[1] -= 1
                                        self.shape_manage(activity=1,gp=last_gp) #paint new

                                    else:
                                        last_gp[1] += 1
                                        self.shape_manage(activity=1,gp=last_gp)

                                elif self.goldpoint[1] > last_gp[1]: #right
                                    self.shape_manage(activity=3,gp=last_gp) #remove from matrix
                                    last_gp[1] += 1
                                    if self.shape_manage(activity=0,gp=last_gp): #check new place
                                        last_gp[1] -= 1
                                        self.shape_manage(activity=2,gp=last_gp) #remove  last painted
                                        last_gp[1] += 1
                                        self.shape_manage(activity=1,gp=last_gp) #paint new

                                    else:
                                        last_gp[1] -= 1
                                        self.shape_manage(activity=1,gp=last_gp)

                        if self.phase != self.currentphase: #button: rotate
                            self.shape_manage(activity=3,gp=last_gp) #delete from matrix
                            if self.shape_manage(activity=0,gp=last_gp,rotatecheck=True): #check new place
                                self.shape_manage(activity=2,gp=last_gp) #remove  last painted
                                self.currentphase = self.phase
                                self.shape_manage(activity=1,gp=last_gp) #paint new one
                            else:
                                self.shape_manage(activity=1, gp=last_gp)
                                self.phase = self.currentphase
                    else:
                        last_gp[0] -= 1
                        self.shape_manage(activity=1,gp=last_gp)
                        self.checklines()
                        generated = False
                sleep(0.00001)

            self.round += 1
            if self.round > 180:
                self.gamespeed = 0.15
                self.multiply = 0
            #print(self.gamespeed - self.round * self.multiply)

    def start(self):
        self.runthreads = "1"
        if self.again:
            for row in range(1,21):
                for column in range(1,11):
                    self.root.grid_slaves(row=row,column=column)[0].configure(image=self.backround,bd=0)
                    self.gameplace[row].pop(column)
                    self.gameplace[row].insert(column,"x")
            self.score = 0
            self.lines = 0
            self.scores()

        self.t = threading.Thread(target=self.thegame)
        self.t.start()
        sleep(.1)
        self.root.grid_slaves(row=12, column=12)[0].destroy()
        Button(text="gaming...").grid(row=12, column=12, columnspan=8)

    def exit(self):
        self.runthreads = "0"
        try: self.t.join()
        except: pass
        sleep(.1)
        self.root.destroy()
        print("bezárt")

    def main(self):
        self.makegameborder()
        self.scores(first=True)
        self.keychecker()

        Button(text="start game",command=self.start).grid(row=12,column=12,columnspan=8)

        self.root.mainloop()

if __name__ == "__main__":
    tetris().main()