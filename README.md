# `dz_zenoh_interop_example`

Project inspired by [Letting Python Be Python: Should ROS 2 be less strict with the Python ecosystem? Notably pip, conda, venv](https://discourse.openrobotics.org/t/letting-python-be-python-should-ros-2-be-less-strict-with-the-python-ecosystem-notably-pip-conda-venv/52385)

There are two Pixi projects here:

- `bare_zenoh_interop_pixi` - A simple Python listener that doesn't use ROS
- `ros_jazzy_core_pixi` - A basic Robostack ROS 2 Jazzy core 

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
export RMW_IMPLEMENTATION=rmw_zenoh_cpp
ros2 run demo_nodes_cpp talker
```

Just to make sure things are running right in a basic way in ROS 2, get a third terminal with the `ros_jazzy_core_pixi` env and run:

```
# terminal 3 ros_jazzy_core_pixi
cd ~/dz_zenoh_interop_example/ros_jazzy_core_pixi
pixi shell
```

Then run

```
export RMW_IMPLEMENTATION=rmw_zenoh_cpp
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