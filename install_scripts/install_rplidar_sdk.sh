mkdir -p Installers
cd Installers
git clone https://github.com/Slamtec/rplidar_sdk.git
cd rplidar_sdk/
make -j4
sudo cp output/Linux/Release/libsl_lidar_sdk.a /usr/local/lib/
sudo mkdir -p /usr/local/include/rplidar
sudo cp sdk/include/* /usr/local/include/rplidar/