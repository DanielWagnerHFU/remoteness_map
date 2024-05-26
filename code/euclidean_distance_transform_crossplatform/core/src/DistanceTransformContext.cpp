#include "DistanceTransformContext.h"

DistanceTransform::DistanceTransformContext::DistanceTransformContext(std::unique_ptr<DistanceTransformStrategy>&& distanceTransformStrategy)
	: distanceTransformStrategy_(std::move(distanceTransformStrategy)) {}

void DistanceTransform::DistanceTransformContext::set_strategy(std::unique_ptr<DistanceTransformStrategy>&& distanceTransformStrategy) {
	distanceTransformStrategy_ = std::move(distanceTransformStrategy);
}

cv::Mat DistanceTransform::DistanceTransformContext::execute(const cv::Mat& input) {
	return distanceTransformStrategy_->transform(input);
}
