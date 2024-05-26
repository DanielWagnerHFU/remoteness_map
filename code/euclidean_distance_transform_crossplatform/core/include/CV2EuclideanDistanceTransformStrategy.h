#pragma once

#include <opencv2/opencv.hpp>
#include "DistanceTransformStrategy.h"

namespace DistanceTransform {

	class CV2EuclideanDistanceTransformStrategy : public DistanceTransformStrategy {
	public:
		cv::Mat transform(const cv::Mat& input) override;
	};
}
