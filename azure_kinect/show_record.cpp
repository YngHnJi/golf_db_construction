#include <k4a/k4a.hpp>
#include <k4a/k4a.h>
#include <k4arecord/record.h>
#include <k4arecord/record.hpp>

#include <iostream>
#include <cstdio>
#include <vector>
#include <array>
#include <conio.h>
#include <direct.h>

#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#include "init_device.hpp"

#include "Pixel.h"
#include "DepthPixelColorizer.h"
#include "StaticImageProperties.h"

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

void showandrecord(string output_file, bool record_switch)
{
	cv::setBreakOnError(true);

	const uint32_t deviceCount = k4a::device::get_installed_count();
	if (deviceCount == 0)
	{
		cout << "no azure kinect devices detected!" << endl;
	}

	// Device Configuration
	k4a_device_configuration_t config;
	k4a::device device;

	kinect_img_container im_container;

	k4a::capture capture;
	k4a::record recording;

	int flag_record = 0; // 0:  not recording, 1: recording, 2: saving
	char key_input;
	int file_index = 0;
	string filename_prefix = "output\\check\\record_";
	string filename;
	filename.append(filename_prefix);
	filename.append(to_string(file_index));
	filename.append(".mkv");


	cout << "Configuring Kinect Device Started" << endl;
	init_kinect(device, config);
	cout << "Configuring Kinect Device Done" << endl;

	// if record_swich's on, return record instance
	if (record_switch == true)
	{
		init_record(device, config, recording, filename);
	}

	while (1)
	{
		if (device.get_capture(&capture, std::chrono::milliseconds(0)))
		{
			//std::cout << "flag: " << flag_record << std::endl;
			// Activate flag_record to record file
			if (_kbhit())
			{
				key_input = _getch();
				if ((key_input == 82) || (key_input == 114))
				{
					flag_record += 1;
					std::cout << "Recording started" << std::endl;
					//std::cout << "flag: " << flag_record << std::endl;
				}
			}


			//Record file when switch on and record instance on
			// Add one more condition
			if ((record_switch == true) && (recording.is_valid() == true) && (flag_record == 1)) {
				recording.write_capture(capture);
			}

			//get image from capture
			//colorImage = capture.get_color_image();
			im_container.depthImage = capture.get_depth_image();
			im_container.irImage = capture.get_ir_image();

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

		// if-statement, to save recording.
		if (flag_record == 2)
		{
			cout << "Record file saving" << endl;
			//std::cout << "flag: " << flag_record << std::endl;
			recording.close();
			recording.flush();

			flag_record = 0;
			file_index += 1;

			filename.clear();
			if (!filename.empty()) {
				filename.clear();
			}

			filename.append(filename_prefix);
			filename.append(to_string(file_index));
			filename.append(".mkv");

			init_record(device, config, recording, filename);
		}

		if ((waitKey(30) == 27))
		{
			cout << "Stop Recording" << endl;
			if (flag_record == 1)
			{
				recording.close();
				recording.flush();
			}
			else if (flag_record == 0)
			{
				recording.close();
				recording.flush();

				remove(filename.c_str());
			}
			break;
		}
	}
	device.stop_cameras();
	device.close();

	return;
}


int main(void)
{
	string output_file = "output\\module4.mkv"; // video file name
	bool record_switch = true;
	showandrecord(output_file, record_switch);

	return 0;
}

