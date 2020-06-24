// function to get skeleton data from loaded file

#include "load_skeleton.hpp"

// Reference: https://github.com/forestsen/KinectAzureDKProgramming

void print_body_information(k4abt_body_t body)
{
    std::cout << "Body ID: " << body.id << std::endl;
    for (int i = 0; i < (int)K4ABT_JOINT_COUNT; i++)
    {
        k4a_float3_t position = body.skeleton.joints[i].position;
        k4a_quaternion_t orientation = body.skeleton.joints[i].orientation;
        k4abt_joint_confidence_level_t confidence_level = body.skeleton.joints[i].confidence_level;
        printf("Joint[%d]: Position[mm] ( %f, %f, %f ); Orientation ( %f, %f, %f, %f); Confidence Level (%d)  \n",
            i, position.v[0], position.v[1], position.v[2], orientation.v[0], orientation.v[1], orientation.v[2], orientation.v[3], confidence_level);
    }
}

void print_body_index_map_middle_line(k4a::image body_index_map)
{
    uint8_t* body_index_map_buffer = body_index_map.get_buffer();

    // Given body_index_map pixel type should be uint8, the stride_byte should be the same as width
    // TODO: Since there is no API to query the byte-per-pixel information, we have to compare the width and stride to
    // know the information. We should replace this assert with proper byte-per-pixel query once the API is provided by
    // K4A SDK.
    assert(body_index_map.get_stride_bytes() == body_index_map.get_width_pixels());

    int middle_line_num = body_index_map.get_height_pixels() / 2;
    body_index_map_buffer = body_index_map_buffer + middle_line_num * body_index_map.get_width_pixels();

    std::cout << "BodyIndexMap at Line " << middle_line_num << ":" << std::endl;
    for (int i = 0; i < body_index_map.get_width_pixels(); i++)
    {
        std::cout << (int)*body_index_map_buffer << ", ";
        body_index_map_buffer++;
    }
    std::cout << std::endl;
}

void export_data(k4abt_body_t body, string output_dir, ofstream& file)
{
    for (int i = 0; i < (int)K4ABT_JOINT_COUNT; i++)
    {
        k4a_float3_t position = body.skeleton.joints[i].position;
        k4a_quaternion_t orientation = body.skeleton.joints[i].orientation;
        k4abt_joint_confidence_level_t confidence_level = body.skeleton.joints[i].confidence_level;
        printf("Joint[%d]: Position[mm] ( %f, %f, %f ); Orientation ( %f, %f, %f, %f); Confidence Level (%d)  \n",
            i, position.v[0], position.v[1], position.v[2], orientation.v[0], orientation.v[1], orientation.v[2], orientation.v[3], confidence_level);
    
        // file write function here
        file << position.v[0] << "," << position.v[1] << "," << position.v[2] << "," <<
            orientation.v[0] << "," << orientation.v[1] << "," << orientation.v[2] << "," << orientation.v[3] << endl;
    }


    return;
}

void load_print_skeleton(string video_input, string output_dir, bool export_flag, ofstream& file)
{
    try
    {        
        /*std::vector<Pixel> depthTextureBuffer;
        std::vector<Pixel> irTextureBuffer;
        uint8_t* colorTextureBuffer;

        k4a::image depthImage;
        k4a::image irImage;

        cv::Mat colorFrame;
        cv::Mat depthFrame;
        cv::Mat irFrame;*/

        // Init configurations
        //k4a_device_configuration_t device_config = K4A_DEVICE_CONFIG_INIT_DISABLE_ALL;
        //device_config.depth_mode = K4A_DEPTH_MODE_NFOV_UNBINNED;
        
        cout << "Started opening Video file..." << endl;
        k4a::playback playback = k4a::playback::open(video_input.c_str());
        cout << "Finished opening Video file..." << endl;

        /*
        cout << "Started opening K4A device..." << endl;
        k4a::device device = k4a::device::open(K4A_DEVICE_DEFAULT);
        device.start_cameras(&device_config);
        cout << "Finished opening K4A device." << endl;
        */


        //k4a::calibration sensor_calibration = device.get_calibration(device_config.depth_mode, device_config.color_resolution);
        k4a::calibration sensor_calibration = playback.get_calibration();
        k4abt::tracker tracker = k4abt::tracker::create(sensor_calibration);

        k4a::capture video_capture;

        int frame_count = 0;

        while (1)
        {
            if (playback.get_next_capture(&video_capture))
            {
                frame_count++;
                std::cout << "Start processing frame " << frame_count << std::endl;

                if (!tracker.enqueue_capture(video_capture))
                {
                    std::cout << "Error! Add capture to tracker process queue timeout!" << std::endl;
                    break;
                }

                k4abt::frame body_frame = tracker.pop_result();
                if (body_frame != nullptr)
                {
                    uint32_t num_bodies = body_frame.get_num_bodies();
                    std::cout << num_bodies << " bodies are detected!" << std::endl;

                    for (uint32_t i = 0; i < num_bodies; i++)
                    {
                        k4abt_body_t body = body_frame.get_body(i);
                        print_body_information(body);
                        if (export_flag == true) {
                            // Timestamp section
                            file << frame_count << endl;
                            export_data(body, output_dir, file);
                        }
                    }
                    std::cout << std::endl << std::endl;

                    /*k4a::image body_index_map = body_frame.get_body_index_map();
                    if (body_index_map != nullptr)
                    {
                        print_body_index_map_middle_line(body_index_map);
                    }
                    else
                    {
                        std::cout << "Error: Failed to generate bodyindex map!" << std::endl;
                    }*/
                }
                else
                {
                    //  It should never hit timeout when K4A_WAIT_INFINITE is set.
                    std::cout << "Error! Pop body frame result time out!" << std::endl;
                    break;
                }
            }
            else
            {
                // It should never hit timeout when K4A_WAIT_INFINITE is set.
                std::cout << "Skeleton data Extraction done" << std::endl;
                break;
            }
        }
    }
    catch (const std::exception& e)
    {
        std::cerr << "Failed with exception:" << std::endl
            << "    " << e.what() << std::endl;
        return;
    }

    return;
}

int main(void)
{
    bool export_flag = true;
    
    string input_path = "output\\module_check.mkv";
    string output_dir = "output\\result.csv";

    ofstream file;
    file.open(output_dir, ios::in);
    if (!(file.is_open())) {
        std::cout << "File not opened" << std::endl;

        return -1;
    }

    load_print_skeleton(input_path, output_dir, export_flag, file);

    std::cout << "File closing" << std::endl;
    file.close();

    return 0;
}