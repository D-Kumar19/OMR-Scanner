# OMR-Scanner
In this repository I have made a program using OpenCV and C++ which will read an OMR sheet and will give you number of correct answers in the end.

This is how the program works: 
   * First we will get the Bird Eye View of the Image which will remove the unwanted parts and will give us just the rectangle of information that we need to asses.
   * We will use threshold() and medianblur() to convert this image to grayscale and find contours.
   * Then we will approximate the coordinates of the contour and we also need to sort them to find which one is first coordinate and whicb one is next.
   * Later we will use erode() function which will  erode the boundaries of foreground object and will give us the Boxes that are filled.
   * Now after applying threshold using threshold() function and getting Mask of the Image we will again use getStructuringElement() but now we will not be using it to Erode using erode() function but we will use dilate() function for Dilation. Dilation increases the size of the foreground object. Hence, we will get all correct objects or Boxes that were correctly filled by the Student.
   * Then we will compare the answer of sutdent with the answer sheet that will be provided to program. 
   * In, the ned it will show the whole result like total number of questions, correct qustions and the percentage the student got.
