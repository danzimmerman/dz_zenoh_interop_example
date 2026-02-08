# Kind of following https://zenoh.io/blog/2021-04-28-ros2-integration/
# But trying rosbags.serde instead of yanked pycdr
import zenoh

config = zenoh.Config.from_file("config.json5")
print("Opening zenoh session")


def sample_callback(sample):
    print(f"{sample.key_expr} => {sample.payload.to_string()}")


session = zenoh.open(config)
session_info = session.info
print(f"Session info:\n  - Routers zids:{[zid for zid in session_info.routers_zid()]}")
print("Declaring subscriber for chatter")
subscriber = session.declare_subscriber("chatter", sample_callback)
