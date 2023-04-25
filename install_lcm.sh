mkdir -p Installers
cd Installers
wget https://github.com/lcm-proj/lcm/archive/refs/tags/v1.5.0.tar.gz
tar -xzvf v1.5.0.tar.gz
rm v1.5.0.tar.gz
cd lcm-1.5.0
mkdir build
cd build
cmake ..
make -j4
sudo make install