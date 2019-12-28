# Simple Loki Service Node Monitor and Email Alert Script

A simple script to easily monitor your Loki Service Node. If your service node's last accepted uptime proof becomes older than 66 minutes, the script will email you an alert. The script is currently set to check your node's uptime proof age every five minutes.

Please note, this is very early development for this script, please use at your own risk. I provide no guarantees of accuracy or functionality.

**To install and run:**
 - Clone repo
 - CD into repo dir
 - Create virtual environment and activate it. ex. `python -m venv venv`
 - Install required modules: `pip install -r requirements.txt`
 - Create ENV file from sample env file: `cp sample.env.txt .env`
 - Edit ENV file in your preferred text editor and save.
 - Test that you can send email alerts: `python yagmail-setup.py`
 - Run script in detached screen: `python monitor.py`


**To Do:**
 - [x] General code improvements
 - [ ] General overall improvement completed. Refine code further with later updates.
 - [x] Improve error handling
 - [x] Add ability to cycle through a list of public nodes to find one that is online in case the previous one goes down or is temporarily unavailable.
 - [ ] Find more reliable remote Loki nodes to add to default list in sample.env file.
 - [ ] Add ability to monitor more than one Loki Service Node.
 - [ ] Ability to run as a system service.

**Bug reporting:**
If you find a bug while using this script, please open an issue to report it.

**Contributing:**
If you'd like to contribute to this script:
 - Fork the repo
 - Open an issue and include info about what improvements you want to add
 - Submit a PR

**Tips:**
If you use and like this Loki Service Node Monitor Script and want to send me a tip as gratitude, you can send Loki tips here:

`LWwK1wqjC3ecKbxdMz8CVt1MdoEqbDQMiCdjWyWziQ3J9Yyi67w1DVZYXypPVx9uRmUppEAQ8R15ief8mCRMHwWsNsweZGF`