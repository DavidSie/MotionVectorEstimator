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
                try:
                    sum = sum + (self.__makroBlock__(i,j)-self.__makroBlock__(i+n,j+m,isCurrent=False))*(self.__makroBlock__(i,j)-self.__makroBlock__(i+n,j+m,isCurrent=False))
                except IndexError:
                    print "IndexError for n,m=[",n, ",", m, "] i=", i, " j=", j," sum=",sum
                    continue
                # print " n,m=[",n, ",", m, "] i=", i, " j=", j," sum=",sum
        # print 'n=',n,' m=',m,' sum=',sum
        return sum

    # macroblock is defined by top left corner and size self.N
    # returns a cut part of picture
    def __makroBlock__(self,i,j,isCurrent=True):
        y=self.y+i
        x=self.x+j
        if x>=len(self.current_picture[0]) or x<0: # python allows negative index but I dont
             raise IndexError('x out of list')
        if  y>=len(self.current_picture) or  y<0:
             raise IndexError('y out of list')
        if isCurrent:
            # print "ref_pict[",y,"]","[",x,"]= ",list(reversed(self.current_picture))[y][x]
            # print "row",list(reversed(self.current_picture))[y]
            return list(reversed(self.current_picture))[y][x]
        else:
            # print "ref_pict[",y,"]","[",x,"]= ",list(reversed(self.referenced_picture))[y][x]
            # print "row",list(reversed(self.referenced_picture))[y]
            return list(reversed(self.referenced_picture))[y][x]

    # returns movment of 1 macro block
    # returned Motion vector has minimal SAD.
    def motionVector(self):
        p_range=range(-self.p,self.p)
        min_n=None
        min_m=None
        min_value=sys.float_info.max

        for n in p_range:
            for m in p_range:
                value=self.__sumOfAbsoluteDifferences__(n,m)
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
                print 'x=',self.x,' y=',self.y
                row.append(self.motionVector())
            result.append(row)
        return result



    # dla wybranych