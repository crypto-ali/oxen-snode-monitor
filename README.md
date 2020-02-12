# Simple Loki Service Node Monitor and Email Alert Script

A simple script to easily monitor your Loki Service Node. If your service node's last accepted uptime proof becomes older than 66 minutes, the script will email you an alert. The script is currently set to check your node's uptime proof age every five minutes.

Please note, this script is in early development, please use at your own risk. I provide no guarantees of accuracy or functionality.


### To install and run:
 - Clone repo
 - CD into repo dir
 - Create virtual environment and activate it. ex. `python -m venv venv`
 - Install required modules: `pip install -r requirements.txt`
 - Create ENV file from sample env file: `cp sample.env.txt .env`
 - Edit ENV file in your preferred text editor and save.
 - Test that you can send email alerts: `python yagmail-setup.py`
 - Create node_list file: `cp sample_node_list.py node_list.py`
   - Note: `node_list.py` is included in the .gitignore file so you can safely add your SNode PubKey(s) without worry of pushing them to a repo.
 - Add your Loki Snode PubKey(s) to the `snode_list` in your `node_list.py` file. You can also add or change the remote nodes in the `remote_node_list`. The remote nodes included in the sample file should work out of the box.   
 - Run script in detached screen: `python monitor.py`


### Run as a system service:
 - `cd /etc/systemd/system`
 - Create a new file with .service file extension and open it to edit. ex. `sudo vi snodemonit.service`
 - Paste the contents of the included sample-service-file.txt into the new file.
 - Update the ExecStart line to include the actual paths to your virtual environment Python and your monitor.py script.
   - Example virtual environment path: `/home/USER/loki-snode-monitor/venv/bin/python`
   - Example path to monitor script: `/home/USER/loki-snode-monitor/venv/monitor.py`
 - Save the file.
 - Run `sudo systemctl daemon-reload` to reload the systemd manager configuration.
 - To start the monitor service, run: `sudo systemctl start snodemonit.service` (This assumes you named your service file *snodemonit.service*)
 - To enable the monitor to start on system boot, run: `sudo systemctl enable snodemonit.service`


### Common systemctl commands:

*All of the following commands assume you named your service file: snodemonit.service*

To check the status of the service, run:

`sudo systemctl status snodemonit.service`

To start the service, run:

`sudo systemctl start snodemonit.service`

To stop the service, run:

`sudo systemctl stop snodemonit.service`

To restart the service, run:

`sudo systemctl restart snodemonit.service`

To disable service autostart on system boot, run: 

`sudo systemctl disable snodemonit.service`

If you make changes to your service monitor files (ex. the .env file), make sure to restart your monitor service file so that those changes are picked up.

If you make changes to the .service file in /etc/systemd/system, make sure to run the daemon-reload command to have your service file changes get picked up by systemd. Then restart the monitor service.

Lastly, to review the logs of your service node monitor when running as a system service, run:

`sudo journalctl --unit=snodemonit.service`


## To Do:
 - [x] General code improvements
 - [ ] General overall improvement completed. Refine code further with later updates.
 - [x] Improve error handling
 - [x] Add ability to cycle through a list of public nodes to find one that is online in case the previous one goes down or is temporarily unavailable.
 - [ ] Find more reliable remote Loki nodes to add to default list in sample.env file.
 - [x] Add ability to monitor more than one Loki Service Node.
 - [x] Ability to run as a system service.


## Changelog:

### 0.0.4 - 2020-2-12:

**Added**
 - Added ability to monitor more than one Loki Service Node.
 - Added this changelog section to README.
 
**Changed** 
 - Fixed error/exception handling.
 - Refactored code.
 - Moved Service Nodes and Remote Nodes from .env file to separate Python file to import as module.


### 0.0.3 - 2020-1-5:

**Added**
 - Added sample service file.

**Changed**
 - Updated README to include running as a service instructions.


### 0.0.2 - 2019-12-28:

**Added**
 - Added ability to use more than one Loki remote node to monitor your service node. Script loops through list of remote nodes.
 - Added additional error handling.
 
**Changed**
 - Updated README
 - Updated required dependencies


### 0.0.1 - 2019-12-21:

**Added**
 - Loki Service Node Monitor released.


## Bug reporting:

If you find a bug while using this script, please open an issue to report it.

## Contributing:

If you'd like to contribute to this script:
 - Fork the repo
 - Open an issue and include info about what improvements you want to add
 - Submit a PR

### Tips:

If you use and like this Loki Service Node Monitor Script and want to send me a tip as gratitude, you can send Loki tips here:

`LWwK1wqjC3ecKbxdMz8CVt1MdoEqbDQMiCdjWyWziQ3J9Yyi67w1DVZYXypPVx9uRmUppEAQ8R15ief8mCRMHwWsNsweZGF`