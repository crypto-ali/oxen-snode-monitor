## Changelog:

### 0.1.1 - 2022-7-19:

**Changed**
- Bumped `lxml` from `4.6.5` to `4.9.1`. [PR 11](https://github.com/crypto-ali/oxen-snode-monitor/pull/11)
- Bumped all the other out-of-date dependencies. [PR 12](https://github.com/crypto-ali/oxen-snode-monitor/pull/12)

### 0.1.0 - 2021-10-4:

**Changed**
- Updated README to include info on the new [node finder](node_finder.py) script.
- Updated README to replace mentions of Loki with Oxen. (Finally catching up with the rebranding.)
- Updated name of repo to `oxen-snode-monitor`
- Updated `sample_node_list.py` to include `explorer.oxen.aussie-pools.com` as a remote node.

**Added**
- Node Finder: Script that scans open nodes for contribution amounts within your desired range. See the README file for
more info.

### 0.0.9 - 2021-9-6:

**Changed**
- Bumped urllib3 from 1.25.10 to 1.26.5. [PR 7](https://github.com/crypto-ali/oxen-snode-monitor/pull/7)
- Updated Requests and Yagmail, along with their dependencies. [PR 8](https://github.com/crypto-ali/oxen-snode-monitor/pull/8)
- Removed changelog section from README. [PR 8](https://github.com/crypto-ali/oxen-snode-monitor/pull/8)

**Added**
- Changelog file. [PR 8](https://github.com/crypto-ali/oxen-snode-monitor/pull/8)

### 0.0.8 - 2021-4-9:

**Changed**
- Bump lxml from 4.6.2 to 4.6.3. [PR 5](https://github.com/crypto-ali/oxen-snode-monitor/pull/5)
- Updated `sample_node_list.py` to include `oxen.observer` block explorer in list of remote nodes. [PR 6](https://github.com/crypto-ali/oxen-snode-monitor/pull/6)

### 0.0.7 - 2021-1-8:

**Changed**
- Bump lxml from 4.5.2 to 4.6.2. [PR 4](https://github.com/crypto-ali/oxen-snode-monitor/pull/4)

### 0.0.6 - 2020-10-14:

**Added**
 - Convert function: Convert time delta of uptime proof age from seconds to HH:MM:SS to make INFO level logs a bit more readable.
 - No Node Alert function: Rolled code block used twice into a function that logs warning when no remote node connection can be made. Function also raises Type Error and exits.

**Changed**
 - Updated `node_selector` function to use a POST request. GET requests started returning 404 after Salty Saga hardfork.
 - General code refactor.
 - Corrected 'occurred' typo.  
 - Cleaned up unused, commented out code from `status_logger`.

### 0.0.5 - 2020-3-25:

**Changed**
 - Updated ***remote_node_list*** in `sample_node_list` to include additional remote nodes for getting uptime proofs.

### 0.0.4 - 2020-2-12:

**Added**
 - Added ability to monitor more than one Loki Service Node.
 - Added this changelog section to README.
 
**Changed** 
 - Fixed error/exception handling.
 - Refactored code.
 - Moved Service Nodes and Remote Nodes from .env file to separate Python file to import as module.
 - Updated dependencies and requirements file.


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