#include "pch.h"

#include <k4a/k4a.hpp>
#include <k4a/k4a.h>
#include <k4arecord/playback.h>
#include <k4arecord/playback.hpp>
#include <k4arecord/record.h>
#include <k4arecord/record.hpp>

#include <windows.h>

#include <iostream>
#include <string>
#include <vector>
#include <array>
#include <atomic>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#include "Pixel.h"
#include "DepthPixelColorizer.h"
#include "StaticImageProperties.h"
#include "Util.h"

#include "init_device.hpp"

using namespace std;
using namespace cv;
using namespace sen;

struct kinect_img_container {
	std::vector<Pixel> depthTextureBuffer;
	std::vector<Pixel> irTextureBuffer;
	uint8_t* colorTextureBuffer;

	k4a::image colorImage;
	k4a::image depthImage;
	k4a::image irImage;

	cv::Mat colorFrame;
	cv::Mat depthFrame;
	cv::Mat irFrame;
};

void load_play(string input_video)
{
	k4a_device_configuration_t config;
	config.depth_mode = K4A_DEPTH_MODE_NFOV_UNBINNED;

	cout << "Started opening Video file..." << endl;
	k4a::playback playback = k4a::playback::open(input_video.c_str());
	cout << "Finished opening Video file..." << endl;

	k4a::capture video_capture;
	kinect_img_container im_container;

	while (1)
	{
		if (playback.get_next_capture(&video_capture))
		{
			// TO DO, Video Capture part comes here
			//get image from capture
			//colorImage = capture.get_color_image();
			im_container.depthImage = video_capture.get_depth_image();
			im_container.irImage = video_capture.get_ir_image();

			//colorTextureBuffer = colorImage.get_buffer();
			ColorizeDepthImage(im_container.depthImage, DepthPixelColorizer::ColorizeBlueToRed, GetDepthModeRange(config.depth_mode), &im_container.depthTextureBuffer);
			ColorizeDepthImage(im_container.irImage, DepthPixelColorizer::ColorizeGreyscale, GetIrLevels(K4A_DEPTH_MODE_PASSIVE_IR), &im_container.irTextureBuffer);

			// RGBA 값이기 때문에 이런 거 같다.
			//colorFrame = cv::Mat(colorImage.get_height_pixels(), colorImage.get_width_pixels(), CV_8UC4, colorTextureBuffer);
			im_container.depthFrame = cv::Mat(im_container.depthImage.get_height_pixels(), im_container.depthImage.get_width_pixels(), CV_8UC4, im_container.depthTextureBuffer.data());
			im_container.irFrame = cv::Mat(im_container.irImage.get_height_pixels(), im_container.irImage.get_width_pixels(), CV_8UC4, im_container.irTextureBuffer.data());

			//// can't access to colorFrame, 
			//cvtColor(colorFrame, colorFrame_bgr, COLOR_YCrCb2BGR);
			//cvtColor(colorFrame, colorFrame_bgr, COLOR_YCrCb2BGR);

			//cv::imshow("kinect color frame master", colorFrame);
			cv::imshow("kinect depth map master", im_container.depthFrame);
			cv::imshow("kinect ir frame master", im_container.irFrame);
		}
		else
		{
			std::cout << "End of video" << std::endl;
			
			return;
		}
		if (waitKey(30) == 27 || waitKey(30) == 'q')
		{
			cout << "Stop Playing" << endl;
			break;
		}
	}
	return;
}

/*
int main(void)
{
	string input_video = "output\\module_check.mkv";
	load_play(input_video);

	return 0;
}
*/