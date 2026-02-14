# `dz_zenoh_interop_example`

Project inspired by [Letting Python Be Python: Should ROS 2 be less strict with the Python ecosystem? Notably pip, conda, venv](https://discourse.openrobotics.org/t/letting-python-be-python-should-ros-2-be-less-strict-with-the-python-ecosystem-notably-pip-conda-venv/52385)

There are two Pixi projects here:

- `bare_zenoh_interop_pixi` - A simple Python listener that doesn't use ROS, running with Python 3.14
- `ros_jazzy_core_pixi` - A basic Robostack ROS 2 Jazzy core, running with Python 3.12

## Instructions - Running

I'm assuming you've cloned the repo to your home directory. If not, adjust the paths.

Run the normal talker using Zenoh RMW, following https://github.com/ros2/rmw_zenoh?tab=readme-ov-file. Activate two terminals with the `ros_jazzy_core_pixi` shell from inside that directory.

In one, run:

```
# terminal 1 ros_jazzy_core_pixi
cd ~/dz_zenoh_interop_example/ros_jazzy_core_pixi
pixi shell
```

Then run 

```
ros2 run rmw_zenoh_cpp rmw_zenohd -c router_config.json5
```

In another, run:

```
# terminal 2 ros_jazzy_core_pixi
cd ~/dz_zenoh_interop_example/ros_jazzy_core_pixi
pixi shell
```

Then run 

```
ros2 run demo_nodes_cpp talker
```

💡 Note that I set the env variable `RMW_IMPLEMENTATION` to `rmw_zenoh_cpp` using the `[activation.env]` section in `pixi.toml`. 

Just to make sure things are running right in a basic way in ROS 2, get a third terminal with the `ros_jazzy_core_pixi` env and run:

```
# terminal 3 ros_jazzy_core_pixi
cd ~/dz_zenoh_interop_example/ros_jazzy_core_pixi
pixi shell
```

Then run

```
ros2 run demo_nodes_cpp listener
```

Now run the listener.

In a fourth terminal, 

```
cd ~/dz_zenoh_interop_example/bare_zenoh_interop_pixi
pixi shell
```

Then run:

```
python standalone_zenoh_listener.py
```

## Expected Output

In the router terminal, you should see something like:

```bash
(ros_jazzy_core_pixi) dan@computer:~/dz_zenoh_interop_example/ros_jazzy_core_pixi$ ros2 run rmw_zenoh_cpp rmw_zenohd -c router_config.json5 
2026-02-08T21:44:06.888275Z  INFO ThreadId(02) zenoh::net::runtime: Using ZID: 1211239493be77c1f82ea0a23a8e3b72
2026-02-08T21:44:06.888638Z  INFO ThreadId(02) zenoh::net::runtime::orchestrator: Zenoh can be reached at: tcp/[fe80::1192:20bf:ff05:52d2]:7447
2026-02-08T21:44:06.888647Z  INFO ThreadId(02) zenoh::net::runtime::orchestrator: Zenoh can be reached at: tcp/192.168.1.45:7447
Started Zenoh router with id 1211239493be77c1f82ea0a23a8e3b72

```

In the talker terminal, you should see:

```bash
(ros_jazzy_core_pixi) dan@computer:~/dz_zenoh_interop_example/ros_jazzy_core_pixi$ ros2 run demo_nodes_cpp talker
[INFO] [1770589218.288734705] [talker]: Publishing: 'Hello World: 1'
[INFO] [1770589219.288629702] [talker]: Publishing: 'Hello World: 2'
[INFO] [1770589220.288787972] [talker]: Publishing: 'Hello World: 3'
[INFO] [1770589221.288783403] [talker]: Publishing: 'Hello World: 4'
[INFO] [1770589222.288772009] [talker]: Publishing: 'Hello World: 5'
[INFO] [1770589223.288781210] [talker]: Publishing: 'Hello World: 6'
[INFO] [1770589224.288648208] [talker]: Publishing: 'Hello World: 7'
```

In the listener terminal, you should see something like:

```bash
(bare_zenoh_interop_pixi) dan@computer:~/dz_zenoh_interop_example/bare_zenoh_interop_pixi$ python standalone_zenoh_listener.py
Opening Zenoh session
Zenoh session info:
  - Routers zids:[1211239493be77c1f82ea0a23a8e3b72]


Declaring subscriber for arbitrary key expressions
17/chatter/std_msgs::msg::dds_::String_/RIHS01_df668c740482bbd48fb39d76a70dfd4bd59db1288021743503259e948f6b1a18 => Hello World: 1
17/chatter/std_msgs::msg::dds_::String_/RIHS01_df668c740482bbd48fb39d76a70dfd4bd59db1288021743503259e948f6b1a18 => Hello World: 2
17/chatter/std_msgs::msg::dds_::String_/RIHS01_df668c740482bbd48fb39d76a70dfd4bd59db1288021743503259e948f6b1a18 => Hello World: 3
17/chatter/std_msgs::msg::dds_::String_/RIHS01_df668c740482bbd48fb39d76a70dfd4bd59db1288021743503259e948f6b1a18 => Hello World: 4
17/chatter/std_msgs::msg::dds_::String_/RIHS01_df668c740482bbd48fb39d76a70dfd4bd59db1288021743503259e948f6b1a18 => Hello World: 5
17/chatter/std_msgs::msg::dds_::String_/RIHS01_df668c740482bbd48fb39d76a70dfd4bd59db1288021743503259e948f6b1a18 => Hello World: 6
17/chatter/std_msgs::msg::dds_::String_/RIHS01_df668c740482bbd48fb39d76a70dfd4bd59db1288021743503259e948f6b1a18 => Hello World: 7

```

💡 Note that 17 is my `ROS_DOMAIN_ID` so it looks like that should be predictable even if the message hash is verbose and obscure.
