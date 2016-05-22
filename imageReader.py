__author__ = 'davidsiecinski'

from PIL import Image

def loadImage(filepath):
    im = Image.open(filepath)
    # im=im.convert('LA')# convert to Black and White
    image_array=[]

    if list(im.getdata())[0] is list:
        for r, b, g in list(im.getdata()):
           image_array.append(0.2125*r + 0.7154*g + 0.0721*b)
    else:
        image_array=list(im.getdata())
    width, height = im.size
    image_list2d = [image_array[i * width:(i + 1) * width] for i in xrange(height)]
    # im.rotate(45).show()
    return image_list2d



