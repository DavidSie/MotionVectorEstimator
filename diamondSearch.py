__author__ = 'Jakub Janeczko <jjaneczk@gmail.com>'

import search

class LDSPGenerator():
    """ Generates LDSP pattern, optimizing it using 1 level search history """
    
    PATTERN = set(  [  2,  0 ],
                    [  1,  1 ],
                    [  0,  2 ],
                    [ -1,  1 ],
                    [ -2,  0 ],
                    [ -1, -1 ],
                    [  0, -2 ],
                    [  1, -1 ]  )
      
    def __init__(self):
        self.last = []
      
    def setOrigin(self, point):
        """ set origin point """
        
        if point == self.origin:
            raise ValueError("Can't set the same point as new origin")
        
        if point not in self.last:
            raise ValueError("Next origin doesn't belong to last pattern")
        
        self.origin = point
        
    def generate(self):
        """ Generate sequence of points to compare """
        
        current = [ (self.origin[0] + x, self.origin[1] + y) for x, y in self.PATTERN ]  

        yield self.origin
        
        for p in current:
            if p not in self.last:
                yield p
        
        self.last = current + self.origin
        
class DiamondSearch(search.Search):
    
    def motionVector(self):
        self.ldsp_limit = self.n * self.n # LDSP iteration limit
        self.ldsp_iters = 0
        ldsp = LDSPGenerator()
        # SAD function
        comp = lambda x: abs(self.current_picture[x[1]][x[0]] - self.referenced_picture[x[1]][x[0]])
        macroblock_filter = lambda p: self.x <= p[0] and p[0] < self.x + self.n and self.y <= p[1] and p[1] < self.y + self.n 
        first = [ self.x + self.n/2, self.y + self.n/2 ]
        origin = first
        while True:
            self.ldsp_iters += 1
            ldsp.setOrigin(origin)
            next_origin = min(filter(macroblock_filter, ldsp.generate()), key=comp)
            if next_origin == origin:
                # SDSP
                sdsp = [(origin[0] + x, origin[1] + y) for x, y in [[0, 0], [1,0], [0, 1], [-1, 0], [0, -1]]]
                last = min(filter(macroblock_filter, sdsp), key=comp)
                return [ last[0]-first[0], last[0]-first[0] ]
            
            if self.ldsp_limit <= self.ldsp_iters:
                raise RuntimeError("LDSP iteration limit reached")