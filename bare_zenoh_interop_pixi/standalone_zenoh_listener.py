# Kind of following https://zenoh.io/blog/2021-04-28-ros2-integration/
# But trying rosbags.serde instead of yanked pycdr
import zenoh
import rosbags
from cdr_decoder import CDRStructBase


class StdMsgsString(CDRStructBase):
    data: str


def chatter_callback(sample):
    print(StdMsgsString.deserialize(sample.payload))

config = zenoh.Config.from_file("config.json5")
with zenoh.open(config) as session:
    with session.declare_subscriber("demo/example/**") as subscriber:
        for sample in subscriber:
            print(f"{sample.key_expr} => {sample.payload.to_string()}")
