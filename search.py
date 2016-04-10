__author__ = 'davidsiecinski'
from abc import ABCMeta, abstractmethod


class Search:
    __metaclass__ = ABCMeta

    def __init__(self,current_picture,referenced_picture,n=2,p=2):
        self.current_picture=current_picture
        self.referenced_picture=referenced_picture
        self.n=n # size of macroblock
        self.p=p # defines searched area [-p,p]
        self.x=0 #curent coordinate of bottom left corner of macroblock
        self.y=0 #curent coordinate of bottom left corner of macroblock

    def setCurrentPicture(self,current_picture):
        self.picture=current_picture

    def setReferencedPicture(self,referenced_picture):
        self.referenced_picture=referenced_picture


        #remember that y is reversed
    # use __makroBlock__ to get value
    def __position___(self,i,j):
         y=self.y+i
         x=self.x+j
         return y,x

    # macroblock is defined by top left corner and size self.N
    # returns a cut part of picture
    def __makroBlock__(self,i,j,isCurrent=True):
        y, x=self.__position___(i,j)
        if x>=len(self.current_picture[0]) or x<0: # python allows negative index but I don't
             raise IndexError('x out of list')
        if  y>=len(self.current_picture) or  y<0:
             raise IndexError('y out of list')
        if isCurrent:
            # print "ref_pict[",y,"]","[",x,"]= ",list(reversed(self.current_picture))[y][x]
            # print "row",list(reversed(self.current_picture))[y]
            return list(reversed(self.current_picture))[y][x]
        else:
            return list(reversed(self.referenced_picture))[y][x]

    @abstractmethod
    def motionVector(self):
        print "Vector motion"

    def motionEstimation(self):
        num_of_macroblocs_in_y=len(self.current_picture)/self.n
        num_of_macroblocs_in_x=len(self.current_picture[0])/self.n
        result=[]
        for y in range(num_of_macroblocs_in_y):
            row=[]
            for x in range(num_of_macroblocs_in_x):
                self.x=x*self.n
                self.y=y*self.n
                row.append(self.motionVector())
            result.append(row)
        return result