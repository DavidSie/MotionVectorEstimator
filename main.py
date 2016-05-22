
import  imageReader
import fullSearch
import logsearch
import time
#import diamondSearch

__name__='MotionVectorEstimator'
__version__='1.0.0rc1'

def raw_input_with_default(text,default):
    input = raw_input(text+'['+default +']'+ chr(8)*4)
    if not input:
        input = default
    return input

current_picture=[]
referenced_picture=[]



print "Welcome to ",__name__," ",__version__

current_picture_path=raw_input_with_default("Path to first(current) picture",'1.jpg')
referenced_picture_path=raw_input_with_default("Path to second(referenced) picture",'2.jpg')
feed_in=raw_input("Choose: Full, Log or Diamond Search")


current_picture=imageReader.loadImage(current_picture_path)
referenced_picture=imageReader.loadImage(referenced_picture_path)
p= 4# len(current_picture)/70 # half of search window
n=4 # size of macroblock

motion_estimation=None
start = time.time()
if "full" in feed_in.lower() :
    full_ = fullSearch.FullSearch(current_picture=current_picture,referenced_picture=referenced_picture,n=n,p=p)
    motion_estimation = full_.motionEstimation()
    print motion_estimation
elif "diamond" in feed_in.lower() :
    # TODO fill me with diamond search code
    print motion_estimation
    exit()
elif "log" in feed_in.lower() :
    log = logsearch.LogSearch(current_picture=current_picture,referenced_picture=referenced_picture,n=n,p=p )
    motion_estimation = log.motionEstimation()
    print motion_estimation
else:
    print "Not found"
    exit()
end = time.time()
running_time=(end - start)
print "it took: ",running_time, "s"


