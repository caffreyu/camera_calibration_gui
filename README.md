# camera_calibration_gui

__This repo is subject to tests.__

Desired test enviroment:

Operating System: Ubuntu 18.04, Ubuntu 20.04

Python Version: >= Python 3.6

</br>


__Installation__

Create a new directory and pull this repo. Then, run `pip3 install -r requirements.txt` to download the required packages. 

</br>

__Usage__

```
chmod +x camera_calibration.sh
./camera_calibration.sh
```

Click on "Save Image" if you would like to save an image for later calibration.

Click on "Calibrate Camera" if you think you have collected enough images for calibration.

</br>


__Result__

If calibration was successful, results of calibration will be stored in `cam_calb_result.pickle` as a dictionary. 

Else, a string will be printed to terminal, notifying you the calibration has failed and will require you to restart the program.

</br>

__TODO__

- Add an entry in tkinter to allow users to enter a max value of image collected for calibration.
- Test calibration on a real camera. Check the results with other calibration method, eg. [calibrating camera using ROS](http://wiki.ros.org/camera_calibration).

