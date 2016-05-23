# MotionVectorEstimator
This repo contains python app to calculate Motion Vector, and to compare methods to achieve that

# Running
To test a program use 2 black and white  frames.
by default program searches for 1.jpg and 2.jpg
(offset [-3, 2] between first and second example picture) 

# Picture Reading
 list ` [[0,0,0,0],[0,1,0,0],[0,3,0,0],[0,0,0,0]]` represent picture
 ```
  y ^
    | 0,0,0,0
    | 0,1,0,0
    | 0,3,0,0
    | 0,0,0,0
    -----------> x
 ```
first list(of y) is reversed to start from the bottom.
Pictures are parsed to monochromatic 

## Literature
  - [ Motion Estimation for Video Coding: Efficient Algorithms and Architectures](https://books.google.pl/books?id=nK0qBgAAQBAJ&pg=PA6&lpg=PA6&dq=Full+Search+video&source=bl&ots=gruM8RHDPw&sig=gQLo3ID_VKI-2xaZqCFobhOHTdA&hl=pl&sa=X&ved=0ahUKEwiEg7PBo-nLAhUmz3IKHU_HAt8Q6AEIKjAD#v=onepage&q=Full%20Search%20video&f=false)
  - M. Jakubowski, G. Pastuszak, "Block-based motion estimation algorithms – a survey", OPTO-ELECTRONICS REVIEW 21(1), 86–102
  - https://en.wikipedia.org/wiki/Sum_of_absolute_differences


Please use git flow !
