from numpy.distutils.system_info import f2py_info

__author__ = 'davidsiecinski'
from abc import ABCMeta, abstractmethod
from scipy import interpolate
from scipy import ndimage
import numpy


class Search:
    __metaclass__ = ABCMeta

    def __init__(self, current_picture, referenced_picture, n=2, p=2,useIntrpolation=True):
        self.current_picture = current_picture
        self.referenced_picture = referenced_picture
        self.n = n  # size of macroblock
        self.p = p  # defines searched area [-p,p]
        self.x = 0  # curent coordinate of bottom left corner of macroblock
        self.y = 0  # curent coordinate of bottom left corner of macroblock
        self.useIntrpolation=useIntrpolation
        if useIntrpolation:
            self.current_picture_interpolated = self.imageInterpolation(self.current_picture)
            self.referenced_picture_interpolated = self.imageInterpolation(self.referenced_picture)
            self.p = p*2
            self.n = n*2
        self.numOfcomparedMacroblocks=0

    def setCurrentPicture(self, current_picture):
        self.picture = current_picture

    def setReferencedPicture(self, referenced_picture):
        self.referenced_picture = referenced_picture


        # remember that y is reversed

    # use __makroBlock__ to get value
    def __position___(self, i, j,):
        y = self.y + i
        x = self.x + j
        return y, x

    # macroblock is defined by top left corner and size self.N
    # returns a cut part of picture
    def __makroBlock__(self, i, j, isCurrent=True, isInterpolated=False):
        y, x = self.__position___(i, j)
        if isCurrent:
            # print "ref_pict[",y,"]","[",x,"]= ",list(reversed(self.current_picture))[y][x]
            # print "row",list(reversed(self.current_picture))[y]
            if isInterpolated:
                return list(reversed(self.current_picture_interpolated))[y][x]
            else:
                return list(reversed(self.current_picture))[y][x]
        else:
            if isInterpolated:
                return list(reversed(self.referenced_picture_interpolated))[y][x]
            else:
                return list(reversed(self.referenced_picture))[y][x]

    @abstractmethod
    def motionVector(self):
        print "Vector motion"

    def motionEstimation(self):

        current_picture=None
        if self.useIntrpolation:
            current_picture=self.current_picture_interpolated
        else :
            current_picture=self.current_picture

        num_of_macroblocs_in_y = len(current_picture) / self.n
        num_of_macroblocs_in_x = len(current_picture[0]) / self.n
        result = []
        for y in range(num_of_macroblocs_in_y):
            row = []
            for x in range(num_of_macroblocs_in_x):
                self.x = x * self.n
                self.y = y * self.n
                row.append(self.motionVector( self.useIntrpolation))
            result.append(row)
        return result

    def imageInterpolation(self,image):
        y=range(len(image))
        x=range(len(image[0]))
        f = interpolate.interp2d(x, y, image)
        xx= [x * 0.5 for x in range(2*len(image[0]))]
        yy=[x * 0.5 for x in range(2*len(image))]
        interpolated_image=f(xx,yy).tolist()
        return interpolated_image

    def imageDownScaling(self,interpolated_image):
        np_array=numpy.array(interpolated_image)
        np_array_small=ndimage.interpolation.zoom(np_array,.5,order=5)
        return np_array_small.tolist()


    def createCompressedImage(self):
        current_picture=None
        if self.useIntrpolation:
            current_picture=self.current_picture_interpolated
        else :
            current_picture=self.current_picture
        num_of_macroblocs_in_y = len(current_picture) / self.n
        num_of_macroblocs_in_x = len(current_picture[0]) / self.n

        mE = self.motionEstimation()
        compressedImage = [0] * len(current_picture)
        for i in range(len(compressedImage)):
            compressedImage[i] = [0] * len(current_picture[0])
        try:
            for y_ in range(num_of_macroblocs_in_y):
                for x_ in range(num_of_macroblocs_in_x):
                    x = x_ * self.n
                    y = y_ * self.n
                    for n1 in range(self.n):
                        for m1 in range(self.n):
                            offset_y = mE[y_][x_][0]
                            offset_x = mE[y_][x_][1]
                            ey = y + n1 + offset_y
                            ex = x + m1 + offset_x
                            if ey < 0 or len(current_picture) <= ey or ex < 0 or len(current_picture[0]) <= ex:
                                print "skipped: ey= ",ey," ex= ",ex," len(current_picture) ",len(current_picture)," len(current_picture[0])",len(current_picture[0])
                                continue
                            cy = y + n1
                            cx = x + m1
                            compressedImage[ey][ex] = current_picture[cy][cx]
        except IndexError as e:
            print "Error: ", e.message, e.args
            print "compressedImage size: [", len(compressedImage), "][", y + n1 + offset_y * self.n, "]"
            print "value: [", y + n1 + offset_y * self.n, "][", x + m1 + offset_x * self.n, "]"
            print "y=", y, " n1=", n1, " offset_y", offset_y, " n=", self.n, " x=", x, " m1=", m1, " offset_x=", offset_x
            print "current_picture[", y + n1, "][", x + m1, "]= ", current_picture[y + n1][x + m1]
            raise e
            exit()
        except TypeError as e:
            print e.message
        if self.useIntrpolation:
            return self.imageDownScaling(compressedImage)
        else:
            return compressedImage