#include <opencv2/opencv.hpp>


int main(void)
{

	cv::Mat img = cv::imread("test.jpg");
	cv::imshow("test", img);
	cv::waitKey(0);

	return 0;
}