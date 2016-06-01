__author__ = 'davidsiecinski'

import sys
import search
class FullSearch(search.Search):

    def __sumOfAbsoluteDifferences__(self,n,m,isInterpolated):
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
                    sum = sum + (self.__makroBlock__(i,j,isInterpolated=isInterpolated)-self.__makroBlock__(i+n,j+m,isCurrent=False,isInterpolated=isInterpolated))*(self.__makroBlock__(i,j,isInterpolated=isInterpolated)-self.__makroBlock__(i+n,j+m,isCurrent=False,isInterpolated=isInterpolated))
                    self.numOfcomparedMacroblocks=self.numOfcomparedMacroblocks+1
        # print "macroblock",self.__position___(0,0),"for vector[",n,",",m,"] sum=",sum
        return sum

    # returns movment of 1 macro block
    # returned Motion vector has minimal SAD.
    def motionVector(self):
        p_range=range(-self.p,self.p+1)
        min_n=None
        min_m=None
        min_value=sys.float_info.max

        for n in p_range:
            for m in p_range:
                value=self.__sumOfAbsoluteDifferences__(n,m,False)
                # print 'value[',n,',',m,']= ', value
                if value<min_value:
                    min_value=value
                    min_n=n
                    min_m=m
        if self.useIntrpolation:
            for n in range(min_n-1,min_n+1):
                for m in range(min_m-1,min_m+1):
                    value=self.__sumOfAbsoluteDifferences__(n,m,True)
                    # print 'value[',n,',',m,']= ', value
                    if value<min_value:
                        min_value=value
                        min_n=n
                        min_m=m

        return [min_n,min_m]