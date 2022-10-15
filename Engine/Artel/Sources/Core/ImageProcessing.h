#pragma once
#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>

using namespace cv;
class ImageProcessing
{
public:
	Mat image;
	void Read(std::string filename);
	void Process(Mat img, Size size, int color_n);
	void Cluster(Mat img);
};

