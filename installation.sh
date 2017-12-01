sudo apt-get install -y build-essential cmake pkg-config libjpeg8-dev libtiff5-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev libatlas-base-dev gfortran python2.7-dev qt5-default
cd ~
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.2.0.zip
sudo unzip opencv.zip
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
rm get-pip.py
sudo pip install numpy
cd opencv-3.2.0
mkdir build
cd build/    
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D FORCE_VTK=ON -D WITH_TBB=ON -D WITH_V4L=ON -D WITH_QT=ON -D WITH_OPENGL=ON -D WITH_CUBLAS=ON -D CUDA_NVCC_FLAGS="-D_FORCE_INLINES" -D WITH_GDAL=ON -D WITH_XINE=ON -D BUILD_EXAMPLES=ON ..
make -j $(($(nproc) + 1))
sudo make install
sudo /bin/bash -c 'echo "/usr/local/lib" > /etc/ld.so.conf.d/opencv.conf'
sudo ldconfig
