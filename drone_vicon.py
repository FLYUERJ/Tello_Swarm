import pyvicon
import time
from enum import Enum
from pyvicon import StreamMode, Direction



vicon = pyvicon.PyVicon()

vicon.connect("152.92.155.4")
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

counts = vicon.get_subject_count()


while True:
    counts = vicon.get_subject_count()
    print(counts)
    ##print(vicon.get_marker_name("disco",0))
    ##print(vicon.get_subject_count())
    time.sleep(0.03)

    pass
