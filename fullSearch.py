__author__ = 'davidsiecinski'

import sys
class FullSearch:
    def __init__(self,current_picture,referenced_picture,n=2,p=2):
        # 2d lists
        self.current_picture=current_picture
        self.referenced_picture=referenced_picture
        self.n=n # size of macroblock
        self.p=p # defines searched area [-p,p]
        self.x=0 #curent coordinate of top left corner of macroblock
        self.y=0 #curent coordinate of top left corner of macroblock

    def setCurrentPicture(self,current_picture):
        self.picture=current_picture

    def setReferencedPicture(self,referenced_picture):
        self.referenced_picture=referenced_picture

    def __sumOfAbsoluteDifferences__(self,n,m):
        sum=0.0
        for i in range(self.n):
            for j in range(self.n):
                y_n, x_m = self.__position___(i+n,j+m)
                y, x = self.__position___(i,j)
                if x_m>=len(self.current_picture[0]) or x_m<0 or y_n>=len(self.current_picture) or  y_n<0:
                    sum =sum + sys.float_info.max/10
                elif x>=len(self.current_picture[0]) or x<0 or y>=len(self.current_picture) or  y<0:
                    sum =sum + sys.float_info.max/10
                else:
                    # print "makroblok(",i,",",j,")=",self.__makroBlock__(i,j),"makroblok(",i+n,",",j+m,")=",self.__makroBlock__(i+n,j+m,isCurrent=False)
                    sum = sum + (self.__makroBlock__(i,j)-self.__makroBlock__(i+n,j+m,isCurrent=False))*(self.__makroBlock__(i,j)-self.__makroBlock__(i+n,j+m,isCurrent=False))
        # print "macroblock",self.__position___(0,0),"for vector[",n,",",m,"] sum=",sum
        return sum

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

    # returns movment of 1 macro block
    # returned Motion vector has minimal SAD.
    def motionVector(self):
        p_range=range(-self.p,self.p+1)
        min_n=None
        min_m=None
        min_value=sys.float_info.max

        for n in p_range:
            for m in p_range:
                value=self.__sumOfAbsoluteDifferences__(n,m)
                # print 'value[',n,',',m,']= ', value
                if value<min_value:
                    min_value=value
                    min_n=n
                    min_m=m
        return [min_n,min_m]

    #   returns matrix of Motion vectors
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



    # dla wybranych