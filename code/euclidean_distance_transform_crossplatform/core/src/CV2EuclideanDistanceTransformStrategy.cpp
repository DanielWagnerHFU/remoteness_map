#include "CV2EuclideanDistanceTransformStrategy.h"

cv::Mat DistanceTransform::CV2EuclideanDistanceTransformStrategy::transform(const cv::Mat& input) {
	cv::Mat output;
	cv::distanceTransform(input, output, cv::DIST_L2, cv::DIST_MASK_PRECISE);
	return output;
}
