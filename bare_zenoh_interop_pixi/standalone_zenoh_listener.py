# Kind of following https://zenoh.io/blog/2021-04-28-ros2-integration/
# But trying rosbags.serde instead of yanked pycdr
import zenoh
from rosbags.typesys import Stores, get_typestore

jazzy_typestore = get_typestore(Stores.ROS2_JAZZY)

def sample_callback(sample):
    # msg_str = stdMsgString.deserialize(sample.payload)
    received_msg = jazzy_typestore.deserialize_cdr(
        sample.payload.to_bytes(), "std_msgs/msg/String"
    )
    print("Type of received_msg:", type(received_msg))
    print(f"{sample.key_expr} => {str(received_msg.data)}")


config = zenoh.Config.from_file("config.json5")
print("Opening zenoh session")

session = zenoh.open(config)
session_info = session.info
print(f"Session info:\n  - Routers zids:{[zid for zid in session_info.routers_zid()]}")
print("Declaring subscriber for any sample")
subscriber = session.declare_subscriber("**", sample_callback)
