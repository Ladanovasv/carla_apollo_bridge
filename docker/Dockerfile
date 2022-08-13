FROM auroai/cyber:v5.0.0
# cyber / bridge requirements
RUN apt update && \
    apt install -y python-pip && \
    pip install --upgrade pip && \
    pip install \
            numpy \
            opencv-python==4.2.0.32 \
            protobuf \
            pygame \
            pyproj \
            pyyaml \
    	    transforms3d

RUN echo "source /apollo/cyber/setup.bash" >> ~/.bashrc && \
    echo "CARLA_PYTHON_ROOT=~/carla_apollo_bridge/carla-python" >> ~/.bashrc && \
    echo "PYTHONPATH=/apollo/py_proto:\$PYTHONPATH" >> ~/.bashrc && \
    echo "PYTHONPATH=\$CARLA_PYTHON_ROOT/carla:\$CARLA_PYTHON_ROOT/carla/dist/carla-0.9.12-py2.7-linux-x86_64.egg:\$PYTHONPATH" >> ~/.bashrc && \
    echo "export PYTHONPATH=\$PYTHONPATH:\$CARLA_PYTHON_ROOT/carla" >> ~/.bashrc && \
    echo "" >> ~/.bashrc
