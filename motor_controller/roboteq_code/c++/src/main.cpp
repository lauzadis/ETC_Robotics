#include <iostream>
#include <stdio.h>
#include <string.h>

#include "../include/RoboteqDevice.cpp"
#include "../include/Constants.h"
#include "../include/ErrorCodes.h"


int main() {
    RoboteqDevice device;
    int status = device.Connect("/dev/ttyACM4");
    if(status != RQ_SUCCESS)
    {
        cout << "Error connecting to device: " << status << "." << endl;
        return 1;
    }

    cout << "Connection successful." << endl;
    device.Disconnect();
    return 0;
}