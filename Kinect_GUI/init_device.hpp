#ifndef INIT_DEVICE
#define INIT_DEVICE
#endif

#include <iostream>

#include <k4a/k4a.hpp>
#include <k4a/k4a.h>
#include <k4arecord/record.h>
#include <k4arecord/record.hpp>

using namespace std;


void init_kinect(k4a::device& device, k4a_device_configuration_t& config);

void init_record(k4a::device& device, k4a_device_configuration_t& config, k4a::record& recording, string output_file);