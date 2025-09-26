## Changelog:

### 0.2.9 - 2025-09-26:

**Changed**

- `README.md` - Update the readme to reflect the rebrand from Oxen to Session.

### 0.2.8 - 2025-09-25:

**Changed**

- `requirements.txt` - Bump requests from 2.32.3 to 2.32.4 [PR 25](https://github.com/crypto-ali/oxen-snode-monitor/pull/25)
- `requirements.txt` - Bump urllib3 from 1.26.19 to 2.5.0 [PR 26](https://github.com/crypto-ali/oxen-snode-monitor/pull/26)

### 0.2.7 - 2024-08-27:

**Changed**

- `requirements.txt` - Bump certifi from 2023.7.22 to 2024.7.4. [PR 24](https://github.com/crypto-ali/oxen-snode-monitor/pull/24)

### 0.2.6 - 2024-06-25:

**Changed**
- `requirements.txt` - Bump urllib3 from 1.26.18 to 1.26.19 and requests from 2.31.0 to 2.32.3. [PR 23](https://github.com/crypto-ali/oxen-snode-monitor/pull/23)

### 0.2.5 - 2024-04-16:

**Changed**
- `requirements.txt` - Bump idna from 3.3 to 3.7 [PR 20](https://github.com/crypto-ali/oxen-snode-monitor/pull/20)
- `monitor.py` - Update logging of the happy path to improve readability. [PR 21](https://github.com/crypto-ali/oxen-snode-monitor/pull/21)

### 0.2.4 - 2023-11-09:

**Changed**
- `requirements.txt` - Bump urllib3 from 1.26.17 to 1.26.18 [PR 19](https://github.com/crypto-ali/oxen-snode-monitor/pull/19)

### 0.2.3 - 2023-10-08:

**Changed**
- `requirements.txt` - Bump urllib3 from 1.26.10 to 1.26.17 [PR 18](https://github.com/crypto-ali/oxen-snode-monitor/pull/18)

### 0.2.2 - 2023-5-24:

**Changed**
- `requirements.txt` - Bump certifi from 2022.12.7 to 2023.7.22 [PR 16](https://github.com/crypto-ali/oxen-snode-monitor/pull/16)

### 0.2.1 - 2023-7-27:

**Changed**
- `requirements.txt` - Bump requests from 2.28.1 to 2.31.0 [PR 15](https://github.com/crypto-ali/oxen-snode-monitor/pull/15)

### 0.2.0 - 2023-4-3:

**Changed**
- `status_logger.py` - updated logger file handler to be optionally initialized by environment variable. Updated logger file handler to rotating log file handler.
- `sample.env.txt` - Added new `status_logger` related environment variables.
- `sample-service-file.txt` - Updated the name in the unit description.
- `sample_node_list.py` - Updated the remote node list to remove two and add one.
- `monitor.py` - Refactored. Now also checks if a service node is decommissioned or deregistered. 

### 0.1.2 - 2022-12-26:

**Changed**
- Bump `certifi` from 2022.6.15 to 2022.12.7. [PR 13](https://github.com/crypto-ali/oxen-snode-monitor/pull/13)
- Update changelog: replace past tense verbs with present tense (ex. 'Bumped' => 'Bump' ).

### 0.1.1 - 2022-7-19:

**Changed**
- Bump `lxml` from `4.6.5` to `4.9.1`. [PR 11](https://github.com/crypto-ali/oxen-snode-monitor/pull/11)
- Bump all the other out-of-date dependencies. [PR 12](https://github.com/crypto-ali/oxen-snode-monitor/pull/12)

### 0.1.0 - 2021-10-4:

**Changed**
- Update README to include info on the new [node finder](node_finder.py) script.
- Update README to replace mentions of Loki with Oxen. (Finally catching up with the rebranding.)
- Update name of repo to `oxen-snode-monitor`
- Update `sample_node_list.py` to include `explorer.oxen.aussie-pools.com` as a remote node.

**Added**
- Node Finder: Script that scans open nodes for contribution amounts within your desired range. See the README file for
more info.

### 0.0.9 - 2021-9-6:

**Changed**
- Bump urllib3 from 1.25.10 to 1.26.5. [PR 7](https://github.com/crypto-ali/oxen-snode-monitor/pull/7)
- Update Requests and Yagmail, along with their dependencies. [PR 8](https://github.com/crypto-ali/oxen-snode-monitor/pull/8)
- Removed changelog section from README. [PR 8](https://github.com/crypto-ali/oxen-snode-monitor/pull/8)

**Added**
- Changelog file. [PR 8](https://github.com/crypto-ali/oxen-snode-monitor/pull/8)

### 0.0.8 - 2021-4-9:

**Changed**
- Bump lxml from 4.6.2 to 4.6.3. [PR 5](https://github.com/crypto-ali/oxen-snode-monitor/pull/5)
- Update `sample_node_list.py` to include `oxen.observer` block explorer in list of remote nodes. [PR 6](https://github.com/crypto-ali/oxen-snode-monitor/pull/6)

### 0.0.7 - 2021-1-8:

**Changed**
- Bump lxml from 4.5.2 to 4.6.2. [PR 4](https://github.com/crypto-ali/oxen-snode-monitor/pull/4)

### 0.0.6 - 2020-10-14:

**Added**
 - Convert function: Convert time delta of uptime proof age from seconds to HH:MM:SS to make INFO level logs a bit more readable.
 - No Node Alert function: Rolled code block used twice into a function that logs warning when no remote node connection can be made. Function also raises Type Error and exits.

**Changed**
 - Update `node_selector` function to use a POST request. GET requests started returning 404 after Salty Saga hardfork.
 - General code refactor.
 - Corrected 'occurred' typo.  
 - Cleaned up unused, commented out code from `status_logger`.

### 0.0.5 - 2020-3-25:

**Changed**
 - Update ***remote_node_list*** in `sample_node_list` to include additional remote nodes for getting uptime proofs.

### 0.0.4 - 2020-2-12:

**Added**
 - Added ability to monitor more than one Loki Service Node.
 - Added this changelog section to README.
 
**Changed** 
 - Fixed error/exception handling.
 - Refactored code.
 - Moved Service Nodes and Remote Nodes from .env file to separate Python file to import as module.
 - Update dependencies and requirements file.


### 0.0.3 - 2020-1-5:

**Added**
 - Added sample service file.

**Changed**
 - Update README to include running as a service instructions.


### 0.0.2 - 2019-12-28:

**Added**
 - Added ability to use more than one Loki remote node to monitor your service node. Script loops through list of remote nodes.
 - Added additional error handling.
 
**Changed**
 - Update README
 - Update required dependencies


### 0.0.1 - 2019-12-21:

**Added**
 - Loki Service Node Monitor released.