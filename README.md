# Oxen Service Node Monitor and Email Alert Script

The service node [monitor script](monitor.py) is a simple script to easily monitor your Oxen Service Nodes. If your
service node's last accepted uptime proof becomes older than 66 minutes, the script will email you an alert. The script
is currently set to check your node's uptime proof age every five minutes.

## Oxen Open Service Node Finder

I recently built a [node finder script](node_finder.py) to help me find open nodes to contribute to when I have only a
small amount of Oxen to contribute. When you run the script it will ask you for the minimum and maximum you are looking
to contribute. The script will then scan the service nodes every five minutes looking for ones that aren't yet active
due to not having 15,000 Oxen contributed. If it finds a match, it will email you a notification containing all
matching nodes.

As an example, let's say you have an extra 1,255 Oxen sitting in a wallet. Most open nodes will have a minimum
contribution of 3,750 Oxen (15,000 * 0.25). With the node finder script you could set it to a minimum of 1,000 Oxen and
a maximum of 1,250. If it finds a node with open contribution or minimum contribution within that range (both inclusive)
it will email you a notification.

Please use these scripts at your own risk. I provide no guarantees of accuracy or functionality.


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
 - Add your Oxen Snode PubKey(s) to the `snode_list` in your `node_list.py` file. You can also add or change the remote nodes in the `remote_node_list`. The remote nodes included in the sample file should work out of the box.   
 - Run script in detached screen: `python monitor.py`

### Run Node Finder
 - After completing the install steps above, start a screen, activate the virtual environment, and run: `python node_finder.py`.
 - Input the minimum amount you are looking to stake.
 - Input the maximum amount that you can stake.
 - Detach screen and let it run.

### Run as a system service:
 - `cd /etc/systemd/system`
 - Create a new file with .service file extension and open it to edit. ex. `sudo vi snodemonit.service`
 - Paste the contents of the included sample-service-file.txt into the new file.
 - Update the ExecStart line to include the actual paths to your virtual environment Python and your monitor.py script.
   - Example virtual environment path: `/home/$USER/oxen-snode-monitor/venv/bin/python`
   - Example path to monitor script: `/home/$USER/oxen-snode-monitor/venv/monitor.py`
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
 - [x] Find more reliable remote Oxen nodes to add to default list.
 - [x] Add ability to monitor more than one Oxen Service Node.
 - [x] Ability to run as a system service.

## Changelog:

The changelog has been moved to its own file: [changelog.md](changelog.md)

## Bug reporting:

If you find a bug while using this script, please open an issue to report it.

## Contributing:

If you'd like to contribute to this script:
 1. Fork the repo
 1. Open an issue and include info about what improvements you want to add
 1. Submit a PR

### Tips:

If you use and like this Oxen Service Node Monitor Script and want to send me a tip as gratitude, you can send Oxen tips here:

`LWwK1wqjC3ecKbxdMz8CVt1MdoEqbDQMiCdjWyWziQ3J9Yyi67w1DVZYXypPVx9uRmUppEAQ8R15ief8mCRMHwWsNsweZGF`
