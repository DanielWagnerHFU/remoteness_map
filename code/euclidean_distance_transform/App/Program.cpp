#include <iostream>
#include <memory>
#include <opencv2/opencv.hpp>
#include <opencv2/core/utils/logger.hpp>

#include "DistanceTransformContext.hpp"
#include "CV2EuclideanDistanceTransformStrategy.hpp"
#include "DistanceTransformStrategy.hpp"


using namespace DistanceTransform;

void test_01() {
    cv::Mat image = cv::Mat(11, 11, CV_8UC1, cv::Scalar(0));
    cv::circle(image, cv::Point(5, 5), 0, cv::Scalar(255), cv::FILLED);
    cv::bitwise_not(image, image);
    std::cout << image << std::endl;
    cv::namedWindow("Zoomed Image", cv::WINDOW_NORMAL);
    cv::resizeWindow("Zoomed Image", image.cols * 50, image.rows * 50);
    cv::imshow("Zoomed Image", image);
    cv::waitKey(0);

    DistanceTransformContext context;
    context.set_strategy(std::make_unique<CV2EuclideanDistanceTransformStrategy>());
    cv::Mat distanceTransform = context.execute(image);
    cv::normalize(distanceTransform, distanceTransform, 0, 255, cv::NORM_MINMAX, CV_8UC1);
    std::cout << distanceTransform << std::endl;
    cv::namedWindow("Zoomed Image", cv::WINDOW_NORMAL);
    cv::resizeWindow("Zoomed Image", distanceTransform.cols * 50, distanceTransform.rows * 50);
    cv::imshow("Zoomed Image", distanceTransform);
    cv::waitKey(0);

    cv::Mat combined(image.rows, image.cols + distanceTransform.cols, image.type());
    image.copyTo(combined(cv::Rect(0, 0, image.cols, image.rows)));
    distanceTransform.copyTo(combined(cv::Rect(image.cols, 0, distanceTransform.cols, distanceTransform.rows)));

    cv::namedWindow("Zoomed Image", cv::WINDOW_NORMAL);
    cv::resizeWindow("Zoomed Image", combined.cols * 50, combined.rows * 50);
    cv::imshow("Zoomed Image", combined);
    cv::waitKey(0);
}

void test_02() {
    DistanceTransformContext context;
    context.set_strategy(std::make_unique<CV2EuclideanDistanceTransformStrategy>());
    cv::Mat image(400, 400, CV_8UC1, cv::Scalar(0));
    cv::Point center(image.cols / 2, image.rows / 2);
    int radius = 100;
    cv::circle(image, center, radius, cv::Scalar(255), cv::FILLED);
    cv::Mat distanceTransform = context.execute(image);
    cv::imshow("Original Image", image);
    cv::normalize(distanceTransform, distanceTransform, 0, 255, cv::NORM_MINMAX, CV_8UC1);
    cv::imshow("Distance Transform", distanceTransform);
    cv::waitKey(0);
}

int main() {
    cv::utils::logging::setLogLevel(cv::utils::logging::LogLevel::LOG_LEVEL_SILENT);
	std::cout << "euclidean distance transform app running" << std::endl;
    test_01();
}