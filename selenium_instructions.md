The script requires: Selenium: *http://selenium-python.readthedocs.io/installation.html*
                     pyvirtualdisplay:  *https://pypi.python.org/pypi/PyVirtualDisplay*

Now here is the tricky part, the web browser the script uses (Chrome works better), need to be installed in the machone (obviously) and it can be done via apt-get.
Now, after the browser is installed, the corresponding selenium driver (for some reason it does not come with the selenium install) needs to be placed in the folder
*/usr/bin/*. Here are the links to the drivers:

- Firefox: *https://github.com/mozilla/geckodriver/releases*
- Chrome: *https://chromedriver.storage.googleapis.com/index.html?path=2.25/*