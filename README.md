# Carla Apollo Bridge

This python package provides a bridge for communicating between Apollo's Python API and Carla.  Besides the source code, a Dockerfile and scripts are provided for getting setup quickly and easily.  This package was tested with Carla version 0.9.12, and Apollo v5.0.0.

Apollo runs on the [Cyber RT](https://medium.com/@apollo.baidu/apollo-cyber-rt-the-runtime-framework-youve-been-waiting-for-70cfed04eade) framework. This is a cyber port of the work done here: [https://github.com/carla-simulator/ros-bridge](https://github.com/carla-simulator/ros-bridge)

## Installation

### Pre-requisites

For the simplest setup, we will run Carla in Docker.  You can run Carla from source if you would like, but the setup is more involved: [https://carla.readthedocs.io/en/latest/how_to_build_on_linux/](https://carla.readthedocs.io/en/latest/how_to_build_on_linux/)

#### docker

[https://docs.docker.com/install/linux/docker-ce/ubuntu/](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

#### nvidia-docker

[https://github.com/nvidia/nvidia-docker](https://github.com/nvidia/nvidia-docker)

## Setup / Getting Started

The following commands will be run with 3 containers:

- carla-server: this container will run the Carla simulator
- carla-apollo: bridge between apollo and carla-server containers, has cyber_py and carla python packages installed and unlike apollo container, can easily display gui applications on local machine
- apollo_dev_user: runs the apollo stack

![containers-diagram](https://user-images.githubusercontent.com/3516571/76017110-dea94600-5ed2-11ea-9879-5777eff9f1dd.png)

### Clone and build Apollo

Our fork of Apollo has a few changes that make it work with this Carla bridge.  You can see those changes here: [https://github.com/ApolloAuto/apollo/compare/v5.0.0...AuroAi:carla](https://github.com/ApolloAuto/apollo/compare/v5.0.0...AuroAi:carla)

```
# run on local machine:

git clone https://github.com/auroai/apollo --single-branch -b carla
cd apollo
./docker/scripts/dev_start.sh
./docker/scripts/dev_into.sh
```

Now in the apollo container, build apollo...
```
# run in apollo_dev_user container:

./apollo.sh build_gpu
```

### Run Carla 
```
./CarlaUE4.sh
```

### Build docker image / run container for Carla-Apollo bridge

This container will run the bridge and sim clients.

```
# run on local machine, starting from the root of this repo:

cd docker
./build_docker.sh
./run_docker.sh
```

## Usage

### Run Carla client and bridge

#### Enter carla-apollo docker container

```
# run on local machine:

docker exec -ti carla-apollo bash
```

#### Update /apollo/cyber/setup.bash

Change CYBER_IP in /apollo/cyber/setup.bash to the carla-apollo container IP address

To find out the ip address to use, run this command outside of the container:

```
# run on local machine:

docker inspect carla-apollo | grep IPAddress
```

Then update the file in your preferred editor

```
# run in carla-apollo container:

vim /apollo/cyber/setup.bash
# and so on to edit the text file

# then source your ~/.bashrc file to apply the changes:
source ~/.bashrc
```

#### Create an ego vehicle and client

Run these commands inside the carla-apollo container

```
# run in carla-apollo container:

pip install carla_python/carla/dist/carla-0.9.12-cp27-cp27mu-manylinux_2_27_x86_64.whl 
```
Delete files in docker carla-apollo  /root/.cache/bazel/_bazel_root/install
```
# run in carla-apollo container
cd /apollo
./apollo.sh build_cyber
cd /apollo/cyber/carla_bridge
python carla_cyber_bridge/bridge.py
```

In another terminal...

```
# run in carla-cyber container
cd /apollo/cyber/carla_bridge/carla_spawn_objects
python carla_spawn_objects.py
```


### Run Apollo Dreamview & modules

Now, in the apollo container, run dreamview:

```
# run in apollo_dev_user container:

. /apollo/scripts/dreamview.sh start_fe
```

Then, in a web browser, go to: `localhost:8888`


#### Routing

Click the 'Module Controller' button on the sidebar.  Click the 'Routing' switch to enable Routing.
![routing](https://user-images.githubusercontent.com/3516571/75205804-9303d900-5729-11ea-9d9c-fffc2d847a3b.png)

Click the 'Route Editing' button on the sidebar.  Click on the map to place points.  Place one point to route from the vehicle's current location.  Place two points to route from the first point to the second.  Then, click 'Send Routing Request'.  If routing is successful, a red line appears showing the planned route.
![route_editing](https://user-images.githubusercontent.com/3516571/75205919-f7bf3380-5729-11ea-9c10-1ebc4f7fc3e8.png)

#### Perception

##### Ground truth obstacle sensor

The example scripts use a ground truth obstacle sensor instead of Apollo perception.  This is enable by including object_sensor in [config/settings.yaml](config/settings.yaml).
![groundtruth](https://user-images.githubusercontent.com/3516571/75207429-8b463380-572d-11ea-8179-32603690531c.png)


#### Planning

Once a route has been planned, and prediction output is received you can enable the 'Planning' module.  The bridge will automatically move the vehicle along the planned path unless output from the 'Control' module is received.
![planning](https://user-images.githubusercontent.com/3516571/75208171-ab76f200-572f-11ea-8a58-910659fb6f93.png)

#### Control
If the 'Control' module is enabled, the bridge will apply its output to the ego vehicle, but this feature has not been fully developed yet.  So, the ego's movement may be erratic.  The recommended way to use the bridge is to allow it to use the planner output for moving the vehicle.

