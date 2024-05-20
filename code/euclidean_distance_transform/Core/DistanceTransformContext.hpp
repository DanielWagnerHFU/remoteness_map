#pragma once

#include <memory>
#include "DistanceTransformStrategy.hpp"

namespace DistanceTransform {

	class DistanceTransformContext {
	private:
		std::unique_ptr<DistanceTransformStrategy> distanceTransformStrategy_;

	public:
		explicit DistanceTransformContext(std::unique_ptr<DistanceTransformStrategy>&& distanceTransformStrategy = {}) 
			: distanceTransformStrategy_(std::move(distanceTransformStrategy)) {
		}

		void set_strategy(std::unique_ptr<DistanceTransformStrategy>&& distanceTransformStrategy) {
			distanceTransformStrategy_ = std::move(distanceTransformStrategy);
		}

		cv::Mat execute(const cv::Mat& input) {
			return distanceTransformStrategy_->transform(input);
		}
	};
}
