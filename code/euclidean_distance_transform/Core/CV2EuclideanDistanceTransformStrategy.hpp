#pragma once

#include <opencv2/opencv.hpp>
#include "DistanceTransformStrategy.hpp"

namespace DistanceTransform {

	class CV2EuclideanDistanceTransformStrategy : public DistanceTransformStrategy {
	public:
		cv::Mat transform(const cv::Mat& input) override {
			cv::Mat output;
			cv::distanceTransform(input, output, cv::DIST_L2, cv::DIST_MASK_PRECISE);
			return output;
		}
	};
}
