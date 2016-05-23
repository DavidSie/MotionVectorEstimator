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
            cnt += 1
        
        _sum /= cnt
        #print "Compute SAD for macroblock ({0[0]}, {0[1]}): {1}".format(ref_center, _sum)
        
        return _sum  
    
    def motionVector(self):
        self.first = ( self.x + self.n/2, self.y  + self.n/2)
        ldsp = LDSPGenerator()
        origin = self.first
        while True:
            #print "point ({0[0]}, {0[1]})".format(origin)
            ldsp.setOrigin(origin)
            filtered_pattern = filter(lambda x: self.search_area_filter(x), ldsp.generate())
            mblock_cmp = lambda x: self.blockSAD(x)
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