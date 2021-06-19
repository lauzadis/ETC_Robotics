# Configure
Make sure to set the device port in `sample.cpp` to match what your computer sees. It is currently set to `/dev/ttyACM0` but you may need to change it.

# Compile
`gcc -c RoboteqDevice.cpp` (just once)
`g++ RoboteqDevice.o sample.cpp -o sample.o` (every time you make a code change)

# Run
`sudo ./sample.o` (need sudo because it needs to find the /dev/ file)

# Semi-Secrets (shh)
The password to the robonuc user on the NUC is `etcdupage`.
