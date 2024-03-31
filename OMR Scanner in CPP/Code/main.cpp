#include<iostream>
#include<opencv2/core.hpp>
#include<opencv2/highgui.hpp>
#include<opencv2/imgproc.hpp>

using namespace cv;
using namespace std;

void GetBirdEyeViewOfImage(const Mat srcImg, Mat& destImg) {

	Mat srcImgCopy, matrix;
	srcImgCopy = srcImg.clone();

	cvtColor(srcImgCopy, srcImgCopy, COLOR_BGR2GRAY);
	threshold(srcImgCopy, srcImgCopy, 130, 255, THRESH_BINARY_INV);
	medianBlur(srcImgCopy, srcImgCopy, 3);

	vector<vector<Point>> contours;
	vector<Point2f> contoursCopy;
	findContours(srcImgCopy, contours, RETR_EXTERNAL, CHAIN_APPROX_NONE);

	for (size_t i = 0; i < contours.size(); i++) {
		float perimeter = arcLength(contours[i], true);
		approxPolyDP(contours[i], contoursCopy, 0.02 * perimeter, true);
	}

	float coordinatesOfRect[4];
	for (int i = 0; i < 4; i++)
		coordinatesOfRect[i] = contoursCopy[i].x + contoursCopy[i].y;

	sort(coordinatesOfRect, coordinatesOfRect + 4);

	Point2f sourceCoordinates[4], destinationCoordinates[4];
	for (int i = 0; i < 4; i++){
		for (int j = 0; j < 4; j++){
			if (coordinatesOfRect[i] == contoursCopy[j].x + contoursCopy[j].y) {
				sourceCoordinates[i] = contoursCopy[j];
			}
		}
	}
	

	float rows = (float)srcImg.rows;
	float column = (float)srcImg.cols;

	destinationCoordinates[0] = {0.0f, 0.0f};
	destinationCoordinates[1] = {column, 0.0f};
	destinationCoordinates[2] = {0.0f, rows};
	destinationCoordinates[3] = {column, rows};

	matrix = getPerspectiveTransform(sourceCoordinates, destinationCoordinates);
	warpPerspective(srcImg, destImg, matrix, destImg.size());
}

void DetectNonGrayBoxes(const Mat& srcImg, Mat& destImg) {

	Mat srcImgCopy, srcImgStructingElement, srcImgErode;
	srcImgCopy = srcImg.clone();

	cvtColor(srcImgCopy, srcImgCopy, COLOR_BGR2GRAY);
	inRange(srcImgCopy, 100, 200, srcImgCopy);
	medianBlur(srcImgCopy, srcImgCopy, 5);

	srcImgStructingElement = getStructuringElement(MORPH_ELLIPSE, Size(9, 9));
	erode(srcImgCopy, srcImgErode, srcImgStructingElement);
	destImg = 255 - srcImgErode;
}

int main() { 
	int i = 0;
	String solImgLoc;
	Mat solImg;
	
	while (solImg.empty()) {
		// cout << "Enter the Location of the Solution Image: ";
		// cin >> solImgLoc;

		solImgLoc = "Images/Test/Solutions.png";
		solImg = imread(solImgLoc, IMREAD_COLOR);

		if (solImg.empty()) {
			cout << "Solution Image cannot be Loaded." << endl;
		}
	}

	Mat testImg, solImgCopy;
	solImgCopy = solImg.clone();
	GetBirdEyeViewOfImage(solImgCopy, solImgCopy);
	DetectNonGrayBoxes(solImgCopy, solImgCopy);

	do{
		Mat testImgCopy, testImgBirdViewOperations, testImgCorrectAnswerMarked;

		string testImgLoc = "Images/Test/Test_" + to_string(++i) + ".png";
		testImg = imread(testImgLoc, IMREAD_COLOR);

		if (testImg.empty()) {
			cout << "Test Image cannot be Loaded." << endl;
			exit(-1);
		}

		testImgCopy = testImg.clone();
		GetBirdEyeViewOfImage(testImgCopy, testImgCopy);
		testImgCorrectAnswerMarked = testImgCopy.clone();

		resize(testImgCopy, testImgBirdViewOperations, solImgCopy.size(), INTER_NEAREST);
		cvtColor(testImgBirdViewOperations, testImgBirdViewOperations, COLOR_BGR2GRAY);
		threshold(testImgBirdViewOperations, testImgBirdViewOperations, 150, 250, THRESH_BINARY_INV);

		testImgBirdViewOperations.setTo(0, solImgCopy);
		dilate(testImgBirdViewOperations, testImgBirdViewOperations, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));

		vector<vector<Point>> contours;
		findContours(testImgBirdViewOperations, contours, RETR_EXTERNAL, CHAIN_APPROX_NONE);

		double percentage = contours.size() * 100 / 10;
		cout << "Total Number of Questions are: 10!" << endl;
		cout << "The Number of Correct Questions are: " << contours.size() << endl;
		cout << "The Percentage of " << testImgLoc << " is: " << percentage << "%." << endl << endl;

		for (int j = 0; j < contours.size(); j++) {

			Rect rect = boundingRect(contours[j]);
			rectangle(testImgCorrectAnswerMarked, rect, Scalar(0, 0, 255), 3);
		}

		putText(testImgCorrectAnswerMarked, "Result: " + to_string(int(percentage)) + "%", Point(10, 80), FONT_HERSHEY_COMPLEX, 1, Scalar(0, 255, 0), 3);

		imshow("Solution Image", solImg);
		imshow("Test Image", testImg);
		imshow("Correct Answers Marked", testImgCorrectAnswerMarked);
		waitKey(0);
	} while (!testImg.empty());

	return 0;
}