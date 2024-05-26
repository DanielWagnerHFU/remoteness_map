#pragma once

#include <memory>
#include "DistanceTransformStrategy.h"

namespace DistanceTransform {

	class DistanceTransformContext {
	private:
		std::unique_ptr<DistanceTransformStrategy> distanceTransformStrategy_;

	public:
		explicit DistanceTransformContext(std::unique_ptr<DistanceTransformStrategy>&& distanceTransformStrategy = {});
		void set_strategy(std::unique_ptr<DistanceTransformStrategy>&& distanceTransformStrategy);
		cv::Mat execute(const cv::Mat& input);
	};
}
