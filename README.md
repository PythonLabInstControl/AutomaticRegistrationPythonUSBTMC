AutomaticRegistrationPythonUSBTMC
=================================

This program helps to automatically register USB-Devices in Linux in the ```/etc/udev/rules.d/usbtmc.rules```-file to be able to use them with [python-usbtmc](https://github.com/python-ivi/python-usbtmc).

###Usage

When starting the program wait until a messagebox(or a command line output) tells you to connect your new USB-device. Connect your new device and then click 'OK'. The program can be started within a console. When [zenity](https://readthedocs.org/projects/python-zenity/) is installed the program still interacts with the user due to messageboxes, otherwise command line outputs are being used.

If you want to know how to work with Github [click here](https://github.com/PythonLabInstControl/SR830_LockInAmplifier#how-to-work-with-github).
