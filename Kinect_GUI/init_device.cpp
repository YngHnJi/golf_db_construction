#include "pch.h"
#include "init_device.hpp"

void init_kinect(k4a::device& device, k4a_device_configuration_t& config)
{
	config = K4A_DEVICE_CONFIG_INIT_DISABLE_ALL;
	config.camera_fps = K4A_FRAMES_PER_SECOND_30;
	config.depth_mode = K4A_DEPTH_MODE_NFOV_UNBINNED;
	//config.color_format = K4A_IMAGE_FORMAT_COLOR_MJPG; // for recording
	config.color_format = K4A_IMAGE_FORMAT_COLOR_YUY2; //for imshow and recording, 4:2:2 UYVY
	//config.color_format = K4A_IMAGE_FORMAT_COLOR_NV12; //for imshow, recording
	//config.color_format = K4A_IMAGE_FORMAT_COLOR_BGRA32; //for imshow
	config.color_resolution = K4A_COLOR_RESOLUTION_720P;
	config.synchronized_images_only = true;

	cout << "Started opening K4A device..." << endl;
	device = k4a::device::open(K4A_DEVICE_DEFAULT);
	device.start_cameras(&config);
	cout << "Finished opening K4A device." << endl;
}

void init_record(k4a::device& device, k4a_device_configuration_t& config, k4a::record& recording, string output_file)
{
	recording = k4a::record::create(output_file.c_str(), device, config);
	recording.write_header();

	if (recording.is_valid() == false) {
		cout << "Recording not opened" << endl;

		return;
	}
}