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

    def createCompressedImage(self):
        num_of_macroblocs_in_y=len(self.current_picture)/self.n
        num_of_macroblocs_in_x=len(self.current_picture[0])/self.n

        mE=self.motionEstimation()
        compressedImage = [0] * len(self.current_picture)
        for i in range(len(compressedImage)):
            compressedImage[i] = [0] * len(self.current_picture[0])
        try :
            for y_ in range(num_of_macroblocs_in_y):
                for x_ in range(num_of_macroblocs_in_x):
                    x = x_*self.n
                    y = y_*self.n
                    for n1 in range(self.n):
                        for m1 in range(self.n):
                            offset_y = mE[y_][x_][0]
                            offset_x = mE[y_][x_][1]
                            ey = y + n1 + offset_y
                            ex = x + m1 + offset_x
                            if ey < 0 or len(self.current_picture) <= ey or  ex < 0 or len(self.current_picture[0]) <= ex:
                                continue
                            cy = y + n1
                            cx = x + m1
                            compressedImage[ey][ex] = self.current_picture[cy][cx]
        except IndexError as e:
            print "Error: ",e.message,e.args
            print "compressedImage size: [",len(compressedImage),"][",y + n1 + offset_y*self.n,"]"
            print "value: [",y + n1 + offset_y*self.n,"][",x + m1 + offset_x*self.n,"]"
            print "y=",y," n1=",n1," offset_y",offset_y," n=",self.n," x=",x," m1=",m1," offset_x=",offset_x
            print "current_picture[",y+n1,"][",x+m1,"]= ",self.current_picture[y+n1][x+m1]
            raise e
            exit()

        return compressedImage