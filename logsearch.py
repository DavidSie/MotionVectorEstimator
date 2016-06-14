__author__ = 'davidsiecinski'
import sys
import search

class LogSearch(search.Search):
    def placeholder(self):
        return None



    # def __init__(self,current_picture, referenced_picture,n=2,p=2):
    #     self.current_picture = current_picture
    #     self.referenced_picture = referenced_picture
    #     self.n = n
    #     self.p = p
    #     self.x = 0
    #     self.y = 0
    #     self.numOfcomparedMacroblocks=0


    def __sumOfAbsoluteDifferences__(self,n,m,isInterpolated):
        sum=0.0
        current_picture=None
        if isInterpolated:
            current_picture=self.current_picture_interpolated
        else:
            current_picture=self.current_picture

        for i in range(self.n):
            for j in range(self.n):
                y_n, x_m = self.__position___(i+n,j+m)
                y, x = self.__position___(i,j)
                if x_m>=len(current_picture[0]) or x_m<0 or y_n>=len(current_picture) or  y_n<0:
                    sum =sum + sys.float_info.max/10
                elif x>=len(current_picture[0]) or x<0 or y>=len(current_picture) or  y<0:
                    sum =sum + sys.float_info.max/10
                else:
                    # print "makroblok(",i,",",j,")=",self.__makroBlock__(i,j),"makroblok(",i+n,",",j+m,")=",self.__makroBlock__(i+n,j+m,isCurrent=False)
                    sum = sum + (self.__makroBlock__(i,j,isInterpolated=isInterpolated)-self.__makroBlock__(i+n,j+m,isCurrent=False,isInterpolated=isInterpolated))*(self.__makroBlock__(i,j,isInterpolated=isInterpolated)-self.__makroBlock__(i+n,j+m,isCurrent=False,isInterpolated=isInterpolated))
                    self.numOfcomparedMacroblocks=self.numOfcomparedMacroblocks+1
        # print "macroblock",self.__position___(0,0),"for vector[",n,",",m,"] sum=",sum
        return sum

    def motionVector(self,isInterpolated=False):
        p_range=range(-self.p,self.p+1)

        n_start = 0
        m_start = 0
        min_value = sys.float_info.max
        iteration = 0

        stop=0
        n = n_start
        m = m_start
        step = 8
        while(stop==0):
            #print "WHILE LOOP STARTS HERE ------------"
            #print "Step size = ",step

            min_value = self.__sumOfAbsoluteDifferences__(n,m, isInterpolated)
            iteration=iteration+1
            #print 'Set min value for center point [',n,',',m,'] = ', min_value


            for i in range(n-step,n+step+1,step):
                if(i==n):
                    for j in range(m-step,m+step+1,step):
                        value = self.__sumOfAbsoluteDifferences__(i,j,isInterpolated)
                        #print 'value[',i,',',j,']= ', value
                        [n,m,value,min_value]=self.findMinLocation(n,m,i,j,value,min_value)
                        #print [n,m,value,min_value]
                else:
                    value = self.__sumOfAbsoluteDifferences__(i,m,isInterpolated)
                    #print 'value[',i,',',m,']= ', value
                    temp=m
                    [n,m,value,min_value]=self.findMinLocation(n,m,i,temp,value,min_value)

            #foud new min poit
            #print "New center point is: ",[n,m,value,min_value]

            if([n,m] == [n_start,m_start]):
                step=step/2
            if([n,m]!=[n_start,m_start]):
                n_start=n
                m_start=m
            if(step ==1):
                 stop=1
            #print "STEP ====== " ,step



        #print "Step = 1 ---> find min from 8 points around center point"
        min_value = self.__sumOfAbsoluteDifferences__(n,m,isInterpolated)
        iteration=iteration+1
        #print 'inicial min value[',n,',',m,']= ', min_value
        for i in range(n-step,n+step+1,step):
            for j in range(m-step,m+step+1,step):
                value = self.__sumOfAbsoluteDifferences__(i,j,isInterpolated)
                #print 'value[',i,',',j,']= ', value
                [n,m,value,min_value]=self.findMinLocation(n,m,i,j,value,min_value)
        #print [n,m,value,min_value]



        return [n,m]

    def findMinLocation(self,n,m,i,j,value,min_value):
        if value<min_value:
            min_value=value
            n=i
            m=j
        #print [n,m,value,min_value]
        return [n,m,value,min_value]