import math
from PIL import Image
import  imageReader
import fullSearch
import logsearch
import time
import diamondSearch

__name__='MotionVectorEstimator'
__version__='1.1.0'

def raw_input_with_default(text,default):
    input = raw_input(text+'['+default +']'+ chr(8)*4)
    if not input:
        input = default
    return input

def psnr(orignal_picture,compressed_picture):
#     peak signal-to-noise ratio
    mse =0
    #mean squared error
    for i in range(len(orignal_picture)):
        for j in range(len(orignal_picture[i])):
            mse=mse+(orignal_picture[i][j]-compressed_picture[i][j])*(orignal_picture[i][j]-compressed_picture[i][j])
    mse=mse/(len(orignal_picture)*len(orignal_picture[i]))
    mx_value=0
    for lst in orignal_picture:
        value=max(lst)
        if value > mx_value:
            mx_value=value
    psnr_=10*math.log( mx_value*mx_value/ mse, 10)
    return psnr_

current_picture=[]
referenced_picture=[]



print "Welcome to ",__name__," ",__version__

current_picture_path=raw_input_with_default("Path to first(current) picture",'1.jpg')
referenced_picture_path=raw_input_with_default("Path to second(referenced) picture",'2.jpg')
feed_in=raw_input("Choose: Full, Log or Diamond Search")


current_picture=imageReader.loadImage(current_picture_path)
referenced_picture=imageReader.loadImage(referenced_picture_path)
p = 4# len(current_picture)/70 # half of search window
n = 4 # size of macroblock

motion_estimation=None
comparations=None
start = time.time()
end = time.time()
useIntrpolation=False


if "full" in feed_in.lower() :
    full_ = fullSearch.FullSearch(current_picture=current_picture,referenced_picture=referenced_picture,n=n,p=p,useIntrpolation=useIntrpolation)
    compressedImage = full_.createCompressedImage()
    end = time.time()

    print full_.motionEstimation()
    comparations=full_.numOfcomparedMacroblocks
elif "diamond" in feed_in.lower():
    ds = diamondSearch.DiamondSearch(current_picture, referenced_picture, n, p)
    compressedImage = ds.createCompressedImage()
    end = time.time()
    print ds.motionEstimation()
    comparations=ds.numOfcomparedMacroblocks
elif "log" in feed_in.lower() :
    log = logsearch.LogSearch(current_picture=current_picture,referenced_picture=referenced_picture,n=n,p=p )
    compressedImage = log.createCompressedImage()
    end = time.time()

    print log.motionEstimation()
    comparations=log.numOfcomparedMacroblocks
else:
    print "Not found"
    exit()

running_time=(end - start)
print "it took: ",running_time, "s"," Number of comparitions: ",comparations
if useIntrpolation:
    # Only to get intepolated picture
    full_ = fullSearch.FullSearch(current_picture=current_picture,referenced_picture=referenced_picture,n=n,p=p,useIntrpolation=useIntrpolation)
    print psnr(full_.referenced_picture_interpolated,compressedImage),"[dB] - bigger value is better"
else:
    print psnr(referenced_picture,compressedImage),"[dB] - bigger value is better"

im = Image.new("L", (len(compressedImage[0]), len(compressedImage)), "white")
img_list=[]
for lst in compressedImage:
    img_list=img_list+lst
im.putdata(img_list)
im.show()