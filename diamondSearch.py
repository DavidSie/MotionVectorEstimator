__author__ = 'Jakub Janeczko <jjaneczk@gmail.com>'

import search

class LDSPGenerator():
    """ Generates LDSP pattern, optimizing it using 1 level search history """
    
    PATTERN = set( [(  2,  0 ),
                    (  1,  1 ),
                    (  0,  2 ),
                    ( -1,  1 ),
                    ( -2,  0 ),
                    ( -1, -1 ),
                    (  0, -2 ),
                    (  1, -1 )] )
      
    def __init__(self):
        self.last = set()      # compared points in last iteration
        self.visited = set()   # all visited points
        self.origin = None
        self.numOfcomparedMacroblocks = 0
      
    def setOrigin(self, point):
        """ set origin point """
        
        if point == self.origin:
            raise ValueError("Can't set the same point as new origin")
        
        if self.last and point not in self.last:
            raise ValueError("Next origin doesn't belong to last pattern")
        
        self.origin = point
        
    def generate(self):
        """ Generate sequence of points to compare """
        
        current = [ (self.origin[0] + x, self.origin[1] + y) for x, y in self.PATTERN ]  

        yield self.origin
        
        for p in current:
            if p not in self.visited:
                yield p
        
        last = set(current) | set([self.origin])
        
        self.visited = self.visited | last
        self.last = last
        
def image_area_filter(picture, x):
    if x[0] < 0 or x[1] < 0:
        return False
    if len(picture) <= x[1] or len(picture[0]) <= x[0]:
        return False
    return True
        
class DiamondSearch(search.Search):

    
    # def __init__(self, current_picture, referenced_picture, n=2, p=2):
    #     super(DiamondSearch, self).__init__(current_picture, referenced_picture, n=2, p=2)
    #     self.numOfcomparedMacroblocks=0

    def image_area_filter2(self, curr, ref):
        return image_area_filter(self.current_picture, curr) and image_area_filter(self.referenced_picture, ref)
    
    def search_area_filter(self, x):
        if not image_area_filter(self.current_picture, x):
            return False
        if abs(self.first[0] - x[0]) > self.p:
            return False 
        if abs(self.first[1] - x[1]) > self.p:
            return False     
        return True
    
    def blockSAD(self, ref_center):
        _sum = 0
        cnt = 0
        for (x, y) in [ (x, y) for x in xrange(self.n) for y in xrange(self.n) ]:
            curr = [self.x + x, self.y + y]
            ref = [ref_center[0] + x - self.n/2, ref_center[1] + y - self.n/2]
            if not self.image_area_filter2(curr, ref):
                continue
            
            
            _sum += abs(self.current_picture[curr[1]][curr[0]] - self.referenced_picture[ref[1]][ref[0]])
            self.numOfcomparedMacroblocks=self.numOfcomparedMacroblocks+1
            cnt += 1

        _sum /= cnt
        #print "Compute SAD for macroblock ({0[0]}, {0[1]}): {1}".format(ref_center, _sum)
        
        return _sum

    def motionVector(self,isInterpolated=False):
        self.first = ( self.x + self.n/2, self.y  + self.n/2)
        ldsp = LDSPGenerator()
        origin = self.first
        while True:
            #print "point ({0[0]}, {0[1]})".format(origin)
            ldsp.setOrigin(origin)
            filtered_pattern = filter(lambda x: self.search_area_filter(x), ldsp.generate())
            mblock_cmp = lambda x: self.blockSAD(x)
            try:
                next_origin = min(filtered_pattern, key=mblock_cmp)
                if next_origin[0] == origin[0] and next_origin[1] == origin[1]:
                    # SDSP
                    sdsp = [(origin[0] + x, origin[1] + y) for x, y in [[0, 0], [1,0], [0, 1], [-1, 0], [0, -1]]]
                    filtered_pattern = filter(lambda x: self.search_area_filter(x), sdsp)
                    last = min(filtered_pattern, key=mblock_cmp)
                    vec = [ -last[0]+self.first[0], last[1]-self.first[1] ]
                    #print "vector ({0[0]}, {0[1]}) macroblock {1[0]}, {1[1]}".format(vec, self.first)
                    return [ vec[1], vec[0] ]
                origin = next_origin
            except ValueError as e:
                print e
                print "filtered_pattern", filtered_pattern
                print "mblock_cmp",mblock_cmp
                # SDSP
                sdsp = [(origin[0] + x, origin[1] + y) for x, y in [[0, 0], [1,0], [0, 1], [-1, 0], [0, -1]]]
                filtered_pattern = filter(lambda x: self.search_area_filter(x), sdsp)
                last = min(filtered_pattern, key=mblock_cmp)
                vec = [ -last[0]+self.first[0], last[1]-self.first[1] ]
                #print "vector ({0[0]}, {0[1]}) macroblock {1[0]}, {1[1]}".format(vec, self.first)
                return [ vec[1], vec[0] ]

    # below we use methods from first version

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
