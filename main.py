
import  imageReader
import fullSearch
import logsearch
#import diamondSearch

def raw_input_with_default(text,default):
    input = raw_input(text+'['+default +']'+ chr(8)*4)
    if not input:
        input = default
    return input

__name__='MotionVectorEstimator'
__version__='1.0.0rc1'


current_picture=[]
referenced_picture=[]



print "Welcome to ",__name__," ",__version__

current_picture_path=raw_input_with_default("Path to first(current) picture",'1.jpg')
referenced_picture_path=raw_input_with_default("Path to second(referenced) picture",'2.jpg')
feed_in=raw_input("Choose: Full, Log or Diamond Search")


current_picture=imageReader.loadImage(current_picture_path)
referenced_picture=imageReader.loadImage(referenced_picture_path)
p=len(current_picture)/20 # half of search window
n=5 # size of macroblock



if "full" in feed_in.lower() :
    full_=fullSearch.FullSearch(current_picture=current_picture,referenced_picture=referenced_picture,n=n,p=p)
    print full_.motionVector()
if "diamond" in feed_in.lower() :
    # TODO fill me with diamond search code
    exit()
if "log" in feed_in.lower() :
    # TODO fill me with log search code
    log = logsearch.LogSearch(current_picture=current_picture,referenced_picture=referenced_picture,n=n,p=p )
    print log.motionVector()
    #exit()
else:
    print "Not found"
    exit()



