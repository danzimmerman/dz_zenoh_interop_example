# `dz_zenoh_interop_example`

Project inspired by [Letting Python Be Python: Should ROS 2 be less strict with the Python ecosystem? Notably pip, conda, venv](https://discourse.openrobotics.org/t/letting-python-be-python-should-ros-2-be-less-strict-with-the-python-ecosystem-notably-pip-conda-venv/52385)

There are two Pixi projects here:

- `bare_zenoh_interop_pixi` - A simple Python listener that doesn't use ROS
- `ros_jazzy_core_pixi` - A basic Robostack ROS 2 Jazzy core 

## Instructions

Run the normal talker using Zenoh RMW, following https://github.com/ros2/rmw_zenoh?tab=readme-ov-file. Activate two terminals with the `ros_jazzy_core_pixi` shell.

In one, run:

```
# terminal 1 ros_jazzy_core_pixi
ros2 run rmw_zenoh_cpp rmw_zenohd
```

In another, run:

```
# terminal 2 ros_jazzy_core_pixi
export RMW_IMPLEMENTATION=rmw_zenoh_cpp
ros2 run demo_nodes_cpp talker
```

Just to make sure things are running right in a basic way, get a third terminal with the `ros_jazzy_core_pixi` env and run:

```
# terminal 3 ros_jazzy_core_pixi
export RMW_IMPLEMENTATION=rmw_zenoh_cpp
ros2 run demo_nodes_cpp listener
```

Now run the listener (TO-DO implementation)