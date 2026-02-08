# Kind of following https://zenoh.io/blog/2021-04-28-ros2-integration/
# But trying rosbags.serde instead of yanked pycdr
import zenoh
import rosbags
from cdr_decoder import CDRStructBase

config = zenoh.Config.from_file("config.json5")
print("Opening zenoh session")
with zenoh.open(config) as session:
    print("Declaring subscriber for chatter")
    with session.declare_subscriber("chatter/**") as subscriber:
        for sample in subscriber:
            print(f"{sample.key_expr} => {sample.payload.to_string()}")
