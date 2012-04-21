def angle( pt1, pt2, pt0 ):
    from math import sqrt
    dx1 = pt1.x - pt0.x;
    dy1 = pt1.y - pt0.y;
    dx2 = pt2.x - pt0.x;
    dy2 = pt2.y - pt0.y;
    return (dx1*dx2 + dy1*dy2)/sqrt((dx1*dx1 + dy1*dy1)*(dx2*dx2 + dy2*dy2) + 1e-10);

def FindSquare( img ):
    storage = cvCreateMemStorage(0);
    N = 11;
    sz = cvSize( img.width & -2, img.height & -2 );
    timg = cvCloneImage( img ); # make a copy of input image
    gray = cvCreateImage( sz, 8, 1 );
    pyr = cvCreateImage( cvSize(sz.width/2, sz.height/2), 8, 3 );
    # create empty sequence that will contain points -
    # 4 points per square (the square's vertices)
    square = cvCreateSeq( 0, sizeof_CvSeq, sizeof_CvPoint, storage );
    square = CvSeq_CvPoint.cast( square )

    # select the maximum ROI in the image
    # with the width and height divisible by 2
    subimage = cvGetSubRect( timg, cvRect( 0, 0, sz.width, sz.height ))

    # down-scale and upscale the image to filter out the noise
   # cvPyrDown( subimage, pyr, 7 );
  #  cvPyrUp( pyr, subimage, 7 );
    cvSaveImage( "../subimage.jpg", subimage);
    tgray = cvCreateImage( sz, 8, 1 );
    cvSaveImage( "../gray.jpg", gray);
    # find squares in every color plane of the image
    BiggestSquareSoFar = 0
    BiggestSquareAreaSoFar = 0
    for c in range(3):
	print "c is now " + str(c)
        # extract the c-th color plane
        channels = [None, None, None]
        channels[c] = tgray
        cvSplit( subimage, channels[0], channels[1], channels[2], None ) 
        for l in range(N):
	    print "l is now " + str(l)
            # hack: use Canny instead of zero threshold level.
            # Canny helps to catch squares with gradient shading
            if( l == 0 ):
                # apply Canny. Take the upper threshold from slider
                # and set the lower to 0 (which forces edges merging)
                cvCanny( tgray, gray, 0, 1000, 5 );
                #cvCanny( tgray, gray, 0, thresh, 5 );
                # dilate canny output to remove potential
                # holes between edge segments
                cvDilate( gray, gray, None, 1 );
            else:
                # apply threshold if l!=0:
                #     tgray(x,y) = gray(x,y) < (l+1)*255/N ? 255 : 0
                cvThreshold( tgray, gray, (l+1)*255/N, 255, CV_THRESH_BINARY );

            # find contours and store them all as a list
            wndnam="preview"
#            cvNamedWindow( wndnam, 1 );
#            cvShowImage(wndnam,gray);
#            c = cvWaitKey(0);
            #count, contours = cvFindContours( img, storage, sizeof_CvContour,
            count, contours = cvFindContours( gray, storage, sizeof_CvContour,
                CV_RETR_LIST, CV_CHAIN_APPROX_SIMPLE, cvPoint(0,0) );

            if not contours:
		print "we have no contours"
                continue
            
	    print "testing contours..." + str(count)
            # test each contour
            for contour in contours.hrange():
                # approximate contour with accuracy proportional
                # to the contour perimeter
                result = cvApproxPoly( contour, sizeof_CvContour, storage,
                    CV_POLY_APPROX_DP, 15, 0 );
                    #CV_POLY_APPROX_DP, cvContourPerimeter(contours)*1.5, 0 );
                # square contours should have 4 vertices after approximation
                # relatively large area (to filter out noisy contours)
                # and be convex.
                # Note: absolute value of an area is used because
                # area may be positive or negative - in accordance with the
                # contour orientation
                if( result.total == 4 and 
#                    abs(cvContourArea(result)) > 2000  and 
                    abs(cvContourArea(result)) > 1000 and 
                    cvCheckContourConvexity(result) ):
                    print "   We have a 4 sided polyline"
                    if abs(cvContourArea(result)) > BiggestSquareAreaSoFar:
			BiggestSquareAreaSoFar =  abs(cvContourArea(result))
			print "We found a square bigger than " + str(BiggestSquareAreaSoFar)
                        #square = cvCreateSeq( 0, sizeof_CvSeq, sizeof_CvPoint, storage );
                        #square = CvSeq_CvPoint.cast( square )
			square = []
                        square.append(result[0])
                        square.append(result[1])
                        square.append(result[2])
                        square.append(result[3])
			print "Biggest square so far:"
        		print square
			print "Area = " + str(abs(cvContourArea(result)))
		
        
    print "We are returning the biggest square: "
    print square
    cvClearMemStorage( storage );
    return square;




# the function draws all the squares in the image
def SquaresImage( img, thesquare ):
    print "Entering Squares Image "
    #print thesquare[0]
    #print pt
    cpy = cvCloneImage( img );
    # read 4 sequence elements at a time (all vertices of a square)
    pt = [ thesquare[0], thesquare[1], thesquare[2], thesquare[3] ]
    print "Debug"
    cvLine( cpy, pt[0], pt[1], CV_RGB(0,255,0));
    cvLine( cpy, pt[1], pt[2], CV_RGB(0,255,0));
    cvLine( cpy, pt[2], pt[3], CV_RGB(0,255,0));
    cvLine( cpy, pt[3], pt[0], CV_RGB(0,255,0));
    # show the resultant image
    return cpy

