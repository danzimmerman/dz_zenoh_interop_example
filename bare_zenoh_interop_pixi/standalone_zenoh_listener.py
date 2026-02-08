# Kind of following https://zenoh.io/blog/2021-04-28-ros2-integration/
# But trying rosbags.serde instead of yanked pycdr
import zenoh
from rosbags.typesys import Stores, get_typestore

jazzy_typestore = get_typestore(Stores.ROS2_JAZZY)

def sample_callback(sample):
    if str(sample.key_expr).count("String"):
        received_msg = jazzy_typestore.deserialize_cdr(
            sample.payload.to_bytes(), "std_msgs/msg/String"
        )
        print(f"{sample.key_expr} => {str(received_msg.data)}")
    else:
        pass
        #print(f"Received sample on {sample.key_expr}, but don't know how to deserialize it.")


config = zenoh.Config.from_file("config.json5")
print("Opening zenoh session")

session = zenoh.open(config)
session_info = session.info
print(f"Session info:\n  - Routers zids:{[zid for zid in session_info.routers_zid()]}")
print("Declaring subscriber for any sample")
subscriber = session.declare_subscriber("**", sample_callback)
