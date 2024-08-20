import pyvicon
import time
from enum import Enum
from pyvicon import StreamMode, Direction



vicon = pyvicon.PyVicon()

vicon.connect("152.92.155.19")
print(vicon.is_connected())

vicon.enable_device_data()
vicon.enable_segment_data()
vicon.enable_marker_data()
vicon.enable_unlabeled_marker_data()

#MyClient.SetStreamMode( ViconDataStreamSDK::CPP::StreamMode::ClientPull ); Client pull is 0 on enum
vicon.set_stream_mode(StreamMode.ClientPull)

#MyClient.SetAxisMapping( Direction::Forward,
#Direction::Left,
#Direction::Up )
vicon.set_axis_mapping(Direction.Forward,Direction.Left,Direction.Up)

isenabled = vicon.is_device_data_enabled()

subject_name = "Tello1"
segment_name = subject_name

while True:

    vicon.get_frame()

    translation = vicon.get_segment_global_translation(subject_name,segment_name)

    if(translation.any() != None):
        print(f"""X:{translation[0]}\nY:{translation[1]}Z:{translation[2]}""")
    else:
        print("Failed get translation")
    time.sleep(0.5)

