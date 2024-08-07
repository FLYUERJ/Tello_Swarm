import pyvicon
import time

vicon = pyvicon.PyVicon()

vicon.connect("152.92.155.4")
print(vicon.is_connected())

vicon.enable_device_data()
vicon.enable_segment_data()
vicon.enable_marker_data()
vicon.enable_unlabeled_marker_data()

vicon_object = vicon.get_axis_mapping()

while True:
    print(vicon.get_axis_mapping())
    print(vicon.get_marker_name("disco",0))
    print(vicon.get_subject_count())
    time.sleep(0.03)

    pass