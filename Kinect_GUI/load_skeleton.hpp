#ifndef LOAD_SKELETON
#define LOAD_SKELETON
#endif

#include <k4a/k4a.hpp>
#include <k4abt.hpp>
#include <k4arecord/playback.hpp>
#include <k4arecord/record.hpp>

#include <windows.h>

#include <iostream>
#include <string>
#include <vector>
#include <array>
#include <atomic>
#include <assert.h>

#include <fstream>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#include "Pixel.h"
#include "DepthPixelColorizer.h"
#include "StaticImageProperties.h"
#include "Util.h"

using namespace std;
using namespace cv;
using namespace sen;


void print_body_information(k4abt_body_t body);

void print_body_index_map_middle_line(k4a::image body_index_map);

void export_data(k4abt_body_t body, string output_dir, ofstream& file);

void load_print_skeleton(string video_input, string output_dir, bool export_flag, ofstream& file);

