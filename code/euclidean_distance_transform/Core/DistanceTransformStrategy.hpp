#pragma once

#include<opencv2/opencv.hpp>

namespace DistanceTransform {

    class DistanceTransformStrategy {
    public:
        virtual cv::Mat transform(const cv::Mat& input) = 0;
        virtual ~DistanceTransformStrategy() = default;
    };
}