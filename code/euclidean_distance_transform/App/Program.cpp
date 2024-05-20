#include <iostream>
#include <DistanceTransformContext.hpp>
#include <CV2EuclideanDistanceTransformStrategy.hpp>
#include <DistanceTransformStrategy.hpp>
#include <memory>
#include <opencv2/opencv.hpp>


using namespace DistanceTransform;

int main() {
	std::cout << "euclidean distance transform app running" << std::endl;
	CV2EuclideanDistanceTransformStrategy cv2edt;
	DistanceTransformContext context;
	context.set_strategy(std::make_unique<CV2EuclideanDistanceTransformStrategy>());

    cv::Mat image(400, 400, CV_8UC1, cv::Scalar(0));
    cv::Point center(image.cols / 2, image.rows / 2);
    int radius = 100;
    cv::circle(image, center, radius, cv::Scalar(255), -1);

	cv::Mat distanceTransform = context.execute(image);

    cv::normalize(distanceTransform, distanceTransform, 0, 255, cv::NORM_MINMAX, CV_8UC1);
    cv::imshow("Original Image", image);
    cv::imshow("Distance Transform", distanceTransform);
    cv::waitKey(0);

}