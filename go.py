#!/usr/bin/env python
# 
# Computer Ricochet Robots
# Code Under the GPL3
# 

from opencv.highgui import *
from opencv.cv import *
#import pygame.image
execfile("functions.py")

# Start by Sucking in the image
Filename="rr1.jpg"
RawImage = cvLoadImage(Filename)
if not RawImage:
	print "Couldn't load %s" % Filename



#Raw Thumbnail
RawImageThumbnail = cvCreateMat(480, 640, CV_8UC3)
cvResize(RawImage, RawImageThumbnail)
cvNamedWindow("Raw", CV_WINDOW_AUTOSIZE);
cvShowImage("Raw", RawImageThumbnail)
cvMoveWindow("Raw", 0,20);

#Outline Thumbnail
RawThumbnailCopy = cvCloneImage( RawImageThumbnail )
TempImage = cvCreateMat(120, 160, CV_8UC3)
#TempImage = cvCreateMat(240, 320, CV_8UC3)
#TempImage = cvCreateMat(640, 480, CV_8UC3)
cvResize(RawThumbnailCopy, TempImage)
BoardSquare = FindSquare( TempImage )
TempImage=SquaresImage( TempImage, BoardSquare );
cvNamedWindow("Outline", CV_WINDOW_AUTOSIZE);
cvMoveWindow("Outline", 641,20);
cvShowImage("Outline", TempImage)

#Aspect Corrected
CorrectedSize=160
mapMatrix = cvCreateMat(3, 3, CV_32FC1)
Point1=CvPoint2D32f
Point1.x = 0
Point1.y = 0
#SourcePoints = ( cvPoint2D32f(BoardSquare[0].x,BoardSquare[0].y).this, cvPoint2D32f(BoardSquare[1].x,BoardSquare[1].y).this, cvPoint2D32f(BoardSquare[2].x,BoardSquare[2].y).this, cvPoint2D32f(BoardSquare[3].x,BoardSquare[3].y).this)
#SourcePoints = ( Point1, Point1,Point1,Point1)
SourcePoints=[]
SourcePoints.append(Point1)
SourcePoints.append(Point1)
SourcePoints.append(Point1)
SourcePoints.append(Point1)
DestinationPoints = [ cvPoint2D32f(0,0).this, cvPoint2D32f(0, CorrectedSize).this, cvPoint2D32f(CorrectedSize, 0).this, cvPoint2D32f(CorrectedSize, CorrectedSize).this]
print "Our source:"
print SourcePoints
print "Our dst:"
print DestinationPoints

#cvGetPerspectiveTransform(SourcePoints, DestinationPoints, mapMatrix)
cvGetPerspectiveTransform(DestinationPoints, DestinationPoints, mapMatrix)
cvNamedWindow("Aspect Corrected", CV_WINDOW_AUTOSIZE);
cvShowImage("Aspect Corrected", RawImageThumbnail)
cvMoveWindow("Aspect Corrected", 1280,20);

key=cvWaitKey(0);



