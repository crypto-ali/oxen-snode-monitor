# Simple Loki Service Node Monitor and Email Alert Script

A simple script to easily monitor your Loki Service Node. If your service node's last accepted uptime proof becomes older than 66 minutes, the script will email you an alert. The script is currently set to check your node's uptime proof age every five minutes.

Please note, this is very early development for this script, please use at your own risk. I provide no guarentees of accuracy or functionality.

**To install and run:**
 - Clone repo
 - CD into repo dir
 - Install required modules: `pip install -r requirements.txt`
 - Create ENV file from sample env file: `cp sample.env.txt .env`
 - Edit ENV file in your preferred text editor and save.
 - Test that you can send email alerts: `python yagmail-setup.py`
 - Run script in detatched screen: `python monitor.py`


**To Do:**
 - General code improvements
 - Improve error handling
 - Add ability to cycle through a list of public nodes to find one that is online in case the previous one goes down or is temporarily unavailable.
 - Add ability to monitor more than one Loki Service Node.
 - Ability to run as a system service.

