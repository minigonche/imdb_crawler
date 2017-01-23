
## Selenium Install Instructions

*Works only with Pyhton3*

The script requires: 
- Selenium: *http://selenium-python.readthedocs.io/installation.html*
- pyvirtualdisplay:  *https://pypi.python.org/pypi/PyVirtualDisplay*

Now here is the tricky part, the web browser the script uses (Chrome works better), need to be installed in the machine (obviously) and it can be done via apt-get.
Now, after the browser is installed, the corresponding selenium driver (for some reason it does not come with the selenium install) needs to be placed in the folder
*/usr/bin/*. Here are the links to the drivers:

- Firefox: *https://github.com/mozilla/geckodriver/releases*
- Chrome: *https://chromedriver.storage.googleapis.com/index.html?path=2.25/*

You can install Chromium which is easier: **sudo apt-get install chromium-browser**

----------------------------------------------

Here is a complete list of the necessary installs for the script to work, (at least for cloud9 and AWS),
working on January of 2017

sudo apt-get update
sudo apt-get install python3-pip

sudo pip3 install selenium

sudo apt-get install xvfb xserver-xephyr vnc4server
sudo pip3 install pyvirtualdisplay

sudo apt-get install chromium-browser

sudo apt-get install python-dev libmysqlclient-dev
sudo apt-get install python3-dev
sudo pip3 install mysqlclient

sudo pip3 install numpy

sudo apt-get install unzip
wget https://chromedriver.storage.googleapis.com/2.25/chromedriver_linux64.zip
unzip chromedriver_linux64.zip 
sudo mv chromedriver /usr/bin/
