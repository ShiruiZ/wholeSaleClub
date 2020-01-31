# wholeSaleClub
## General:
Used python 3.6, selenium and sqlite.
This program fetches information of the water products sold by the Wholesale Club.
## How to run and what will it do:
Use `$ python main.py` to run the program. A Wholesale Club website will be opened. After a few moments, all the information are saved in the `water.db`.
## How to install Selenium
`$ sudo pip3.6 install selenium`<br />
However for me it didn't work. I used `$ sudo easy_install selenium` instead but it is Mac only.
## Where to download ChromeDriver
To run this program, a chromedriver is necessary. Here is the [chromedriver](https://chromedriver.chromium.org/downloads). <br />Moreover, make sure to put it in the `/usr/local/bin/chromedriver` directory since in my code, the variable `executable_path` stated that it is in this location.
## How to install webdriver_manager
 `$ sudo easy_install webdriver_manager` (Mac only)
