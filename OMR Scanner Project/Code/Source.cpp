#include<iostream>
#include<opencv2/core.hpp>
#include<opencv2/highgui.hpp>
#include<opencv2/imgproc.hpp>

using namespace cv;
using namespace std;

void Img_Bird_Eye_View(const Mat Src_Img, Mat& Dest_Img) {

	Mat Src_Img_Copy, Src_Img_Gray, Src_Img_Thresh, Src_Img_Blur, Matrix;
	Src_Img_Copy = Src_Img.clone();

	cvtColor(Src_Img_Copy, Src_Img_Gray, COLOR_BGR2GRAY);
	threshold(Src_Img_Gray, Src_Img_Thresh, 130, 255, THRESH_BINARY_INV);
	medianBlur(Src_Img_Thresh, Src_Img_Blur, 3);

	// imshow("Source Image", Src_Img);
	// imshow("Source Image Gray Scale", Src_Img_Gray);
	// imshow("Source Image Threshold", Src_Img_Thresh);
	// imshow("Source image Blur", Src_Img_Blur);
	// waitKey(0);

	vector<vector<Point>> Contours;
	vector<Point2f> Contours_Copy;
	findContours(Src_Img_Blur, Contours, RETR_EXTERNAL, CHAIN_APPROX_NONE);

	for (size_t i = 0; i < Contours.size(); i++) {
		float Perimeter = arcLength(Contours[i], true);
		approxPolyDP(Contours[i], Contours_Copy, 0.02 * Perimeter, true);
	}

	float Coordinates_Of_Rect[4], Temp;
	int Size_Of_Array = sizeof(Coordinates_Of_Rect) / sizeof(Coordinates_Of_Rect[0]);

	// cout << "Un-Ordered Coordinates of Rectangle: " << Contours_Copy[0] << " " << Contours_Copy[1] << " " << Contours_Copy[2] << " " << Contours_Copy[3] << endl;

	// Finding the Sum of Coordinate x and Coordinate y to get the Perspective of the Image.
	// We need to find the exact Coordinate which will be placed on another Coordinate.
	Coordinates_Of_Rect[0] = Contours_Copy[0].x + Contours_Copy[0].y;
	Coordinates_Of_Rect[1] = Contours_Copy[1].x + Contours_Copy[1].y;
	Coordinates_Of_Rect[2] = Contours_Copy[2].x + Contours_Copy[2].y;
	Coordinates_Of_Rect[3] = Contours_Copy[3].x + Contours_Copy[3].y;

	// cout << "Before Sorting: " << Coordinates_Of_Rect[0] << " " << Coordinates_Of_Rect[1] << " " << Coordinates_Of_Rect[2] << " " << Coordinates_Of_Rect[3] << endl;

	// Sorting all the Coordinates. So, the Coordinates are placed in correct order after applying Perspective Transform.
	for (int i = 0; i < Size_Of_Array; i++) {
		for (int j = i + 1; j < Size_Of_Array; j++) {
			if (Coordinates_Of_Rect[i] > Coordinates_Of_Rect[j]) {
				Temp = Coordinates_Of_Rect[i];
				Coordinates_Of_Rect[i] = Coordinates_Of_Rect[j];
				Coordinates_Of_Rect[j] = Temp;
			}
		}
	}

	// cout << "After Sorting: " << Coordinates_Of_Rect[0] << " " << Coordinates_Of_Rect[1] << " " << Coordinates_Of_Rect[2] << " " << Coordinates_Of_Rect[3] << endl;

	// Checking if Sum of the Coordinate matches with the Sum previously stored then we will place them in Order.
	Point2f Source_Coordinates[4], Destination_Coordinates[4];;
	for (int i = 0; i < Size_Of_Array; i++) {
		if (Coordinates_Of_Rect[i] == Contours_Copy[0].x + Contours_Copy[0].y) {
			Source_Coordinates[i] = Contours_Copy[0];
		}
		else if (Coordinates_Of_Rect[i] == Contours_Copy[1].x + Contours_Copy[1].y) {
			Source_Coordinates[i] = Contours_Copy[1];
		}
		else if (Coordinates_Of_Rect[i] == Contours_Copy[2].x + Contours_Copy[2].y) {
			Source_Coordinates[i] = Contours_Copy[2];
		}
		else if (Coordinates_Of_Rect[i] == Contours_Copy[3].x + Contours_Copy[3].y) {
			Source_Coordinates[i] = Contours_Copy[3];
		}
	}

    // cout << "Ordered Coordinates of Rectangle: " << Source_Coordinates[0] << " " << Source_Coordinates[1] << " " << Source_Coordinates[2] << " " << Source_Coordinates[3] << endl;

	float Rows = (float)Src_Img.rows;
	float Column = (float)Src_Img.cols;

	// Getting the Destination Coordinates.
	Destination_Coordinates[0] = { 0.0f, 0.0f };
	Destination_Coordinates[1] = { Column, 0.0f };
	Destination_Coordinates[2] = { 0.0f, Rows };
	Destination_Coordinates[3] = { Column, Rows };

	// Applying Perspective Tranform and Warop Perspective to get the Bird Eye View of Image.
	Matrix = getPerspectiveTransform(Source_Coordinates, Destination_Coordinates);
	warpPerspective(Src_Img, Dest_Img, Matrix, Dest_Img.size());

	// imshow("Original Image", Src_Img);
	// imshow("Bird Eye View of Image", Dest_Img);
	// waitKey(0);
}

void Detect_Non_Gray_Boxes(const Mat& Src_Img, Mat& Dest_Img) {

	Mat Src_Img_Copy, Src_Img_Gray, Src_Img_Gray_Boxes, Src_Img_Blur, Src_Img_Structing_Element, Src_Img_Erode;
	Src_Img_Copy = Src_Img.clone();

	cvtColor(Src_Img_Copy, Src_Img_Gray, COLOR_BGR2GRAY);
	inRange(Src_Img_Gray, 100, 200, Src_Img_Gray_Boxes);
	medianBlur(Src_Img_Gray_Boxes, Src_Img_Blur, 5);

	// imshow("Source Image Original", Src_Img);
	// imshow("Source Image Gray", Src_Img_Gray);
	// imshow("Source Image Gray Boxes Detected", Src_Img_Gray_Boxes);
	// imshow("Source Image Blurred", Src_Img_Blur);
	// waitKey(0);

	Src_Img_Structing_Element = getStructuringElement(MORPH_ELLIPSE, Size(9, 9));
	erode(Src_Img_Blur, Src_Img_Erode, Src_Img_Structing_Element);
	Dest_Img = 255 - Src_Img_Erode;

	// imshow("Source Image Original", Src_Img);
	// imshow("Source Image Eroded", Src_Img_Erode);
	// imshow("Final Image", Dest_Img);
	// waitKey(0);
}

int main() {

	// Asking the User for the Number of Papers. 
	int Count = 0;
	cout << "Enter the Number of Pictures to Check: ";
	cin >> Count;

	Mat Sol_Img, Sol_Img_Copy, Sol_Img_Gray, Sol_Img_Bird_View, Sol_Img_Non_Gray_Boxes;
	Sol_Img = imread("Test/Solutions.png", IMREAD_COLOR);

	if (Sol_Img.empty()) {
		cout << "Solution Image cannot be Loaded." << endl;
		exit(-1);
	}

	Sol_Img_Copy = Sol_Img.clone();

	// Getting the Bird Eye View of the Solution Image.
	Img_Bird_Eye_View(Sol_Img_Copy, Sol_Img_Bird_View);
	// imshow("Solution Image Original", Sol_Img);
	// imshow("Solution Image Bird Eye View", Sol_Img_Bird_View);
	// waitKey(0);

	// Detecting all the Boxes that are Non Gray or Filled. 
	Detect_Non_Gray_Boxes(Sol_Img_Bird_View, Sol_Img_Non_Gray_Boxes);
	// imshow("Solution Image Bird Eye View", Sol_Img_Bird_View);
	// imshow("Solution Image Non Gray Boxes Identified", Sol_Img_Non_Gray_Boxes);
	// waitKey(0);

	for (int i = 1; i < Count; ++i) {

		Mat Test_Img, Test_Img_Copy, Test_Img_Bird_View, Test_Img_Bird_View_Copy, Test_Img_Bird_View_Resized,
			Test_Img_Bird_View_Gray, Test_Img_Bird_View_Thresh, Test_Img_Correct_Boxes, Test_Img_Dilate, Test_Img_Correct_Answer_Marked;

		String Test_Paper_Name = "Test/Test_" + to_string(i) + ".png";
		Test_Img = imread(Test_Paper_Name, IMREAD_COLOR);

		if (Test_Img.empty()) {
			cout << "Test Image cannot be Loaded." << endl;
			exit(-1);
		}

		Test_Img_Copy = Test_Img.clone();

		// Getting the Bird Eye View of the Test Image.
		Img_Bird_Eye_View(Test_Img_Copy, Test_Img_Bird_View);
		Test_Img_Bird_View_Copy = Test_Img_Bird_View.clone();
		Test_Img_Correct_Answer_Marked = Test_Img_Bird_View.clone();
	    // imshow("Test Image Original", Test_Img);
		// imshow("Test Image Bird Eye View", Test_Img_Bird_View);
		// waitKey(0);

		// Resizing the Test Image to the Solution Image so it should be Easy to Compare both.
		resize(Test_Img_Bird_View, Test_Img_Bird_View_Resized, Sol_Img_Non_Gray_Boxes.size(), INTER_NEAREST);
		// imshow("Test Image Bird Eye View", Test_Img_Bird_View);
		// imshow("Test Image Resized", Test_Img_Bird_View_Resized);
		// waitKey(0);

		cvtColor(Test_Img_Bird_View_Resized, Test_Img_Bird_View_Gray, COLOR_BGR2GRAY);
		threshold(Test_Img_Bird_View_Gray, Test_Img_Bird_View_Thresh, 150, 250, THRESH_BINARY_INV);
		// imshow("Test Image Bird Eye View", Test_Img_Bird_View);
		// imshow("Test Image Bird Eye View Gray", Test_Img_Bird_View_Gray);
		// imshow("Test Image Bird Eye View Thresh", Test_Img_Bird_View_Thresh);
		// waitKey(0);

		Test_Img_Correct_Boxes = Test_Img_Bird_View_Thresh.clone();
		Test_Img_Correct_Boxes.setTo(0, Sol_Img_Non_Gray_Boxes);
		dilate(Test_Img_Correct_Boxes, Test_Img_Dilate, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
		// imshow("Solution Image", Sol_Img_Bird_View);
		// imshow("Test Image Bird Eye View", Test_Img_Bird_View);
		// imshow("Boxes Filled By Student", Test_Img_Correct_Boxes);
		// imshow("Test Image Dilated", Test_Img_Dilate);
		// waitKey(0);

		vector<vector<Point>> Contours;
		findContours(Test_Img_Dilate, Contours, RETR_EXTERNAL, CHAIN_APPROX_NONE);
		
		// Outputting the Result
		double Percentage = Contours.size() * 100 / 10;
		cout << "Total Number of Questions are: 10!" << endl;
		cout << "The Number of Correct Questions are: " << Contours.size() << endl;
		cout << "The Percentage of " << Test_Paper_Name << " is: " << Percentage << "%." << endl << endl;

		// Marking a Rectangle on each Correct Answer marked by Student.
		for (int j = 0; j < Contours.size(); j++) {

			Rect Rectangle = boundingRect(Contours[j]);
			rectangle(Test_Img_Correct_Answer_Marked, Rectangle, Scalar(0, 0, 255), 3);
		}

		putText(Test_Img_Bird_View, "Result: " + to_string(int(Percentage)) + "%", Point(10, 80), FONT_HERSHEY_COMPLEX, 1, Scalar(0, 255, 0), 3);

		// imshow("Solution Image", Sol_Img_Bird_View);
		// imshow("Test Image", Test_Img_Bird_View_Copy);
		// imshow("Correct Answers Marked", Test_Img_Correct_Answer_Marked);
		// imshow("Result of the Student", Test_Img_Bird_View);
		// waitKey(0);
	}
	return 0;
}