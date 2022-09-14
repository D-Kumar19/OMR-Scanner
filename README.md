# OMR-Scanner
In this repository I have made a program using OpenCV, C++ and Python which will read an OMR sheet and will give you number of correct answers in the end.

***
The directory OMR Scanner Project has program in C++ and this is how it works:
   * First we will get the Bird Eye View and later we will find the Contours.
   * Then we will approximate the coordinates of the contour and we also need to sort them to find which one is first coordinate and which one is next.
   * Later we will use erode() function which will  erode the boundaries of foreground object and will give us the Boxes that are filled.
   * Now after applying threshold using threshold() function and getting Mask of the Image we will use getStructuringElement() to dilate the image using dilate(). Dilation increases the size of the foreground object. Hence, we will get all correct objects or Boxes that were correctly filled by the Student.
   * Then we will compare the answer of sutdent with the answer sheet that will be provided to program. 
   * In, the end it will show the result on terminal which will consist of total number of questions, correct qustions and the percentage the student got.
   * I have provided some test Images for others to see how it works and what kind of pictures it takes.
***

*** 
The directory OMR Scanner in Python has project in Python and this is how it works:
  * There are two options either to check the images live using the webcam or you already have stored the scanned images in a directory.
  * After choosing the options first you need to add the **Solution Image** and later you can add the question image. Program will confirm if there file exists or not.
  * Using the solution image it will first generate the answer key. Later, it will get the bird eye view of the image.
  * Then we will divide the image in number of rows and columns and then we will check which box is filled and which isn't. After that we will compare the chosen options with the answer key. If answer is correct user will get one point either not. 
  * Everytime program checks an Image it will store the result image with score written in the main directory so we can check it later. It also used time-stamp so there is no chance of the file being over-written. 
  * There are test images in the **Images** directory and you check the program using these images.
  * There are also result images in the **Result Images** directory you can check them also to see the results.
***

Thanks for visiting. 
If you have any issue then please create an issue on GitHub so we can fix it. Thanks!
