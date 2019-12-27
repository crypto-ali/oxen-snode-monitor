# Loki Service Node Monitor and Email Alert

import os
import sys
import requests
import time
from dotenv import load_dotenv
import logging
import status_logger
import yagmail

load_dotenv()

# ENV VARS

SNODE_PUBKEY = os.getenv('SNODE_PUBKEY')
FROM = os.getenv('FROM_ADDRESS')
FROM_PASS = os.getenv('FROM_PASS')
TO = os.getenv('TO_ADDRESS')
NODE_1 = os.getenv('NODE_1')
Node_2 = os.getenv('Node_2')

yag = yagmail.SMTP(FROM, FROM_PASS)

node_list = [
    NODE_1 + '/json_rpc',
    Node_2 + '/json_rpc'
    ]

def node_selector(node_list):
    for x in node_list:
        r = requests.get(x, timeout=10)
        if r.status_code == 200:
            node = x
            return node
            pass
        else:
            node = None


if __name__ == "__main__":

  try:
    url = node_selector(node_list)
    if url == None:
      status_logger.logger.warning("Unable to connect to a Loki remote node.")
      no_node_subj = "Unable to connect to a Loki remote node."
      no_node_body = "Unable to connect to a Loki remote node. No nodes in your node list were available. Your service node monitor has stopped. Please investigate the issue."
      yag.send(TO, no_node_subj, no_node_body)
      raise ValueError("Unable to connect to a Loki remote node. Remote node cannot be 'None'.")
    else:
      pass
  except KeyboardInterrupt:
    sys.exit()
  except ValueError as error:
    status_logger.logger.exception("Exception occured\n")
    sys.exit()
  except (Timeout, ConnectTimeout, ReadTimeout) as e:
    status_logger.logger.exception("Exception occured\n")
    time.sleep(60)
    status_logger.logger.info("Reconnecting...")
    url = node_selector(node_list)
  except Exception as e:
    status_logger.logger.exception("Exception occured\n")

  while True:
    status_logger.logger.info(f"Connected to: {url}")
    status_logger.logger.info("Getting your Loki Service Node last uptime proof.")
    try:    
      sns = requests.post(url, json={"jsonrpc":"2.0","id":"0","method":"get_service_nodes", "params": {"service_node_pubkeys": [SNODE_PUBKEY]}}, timeout=10).json()

      snlup = sns['result']['service_node_states'][0]['last_uptime_proof']
      snlup_time = time.strftime('%b %d, %Y - %I:%M:%S %p', time.localtime(snlup))
    	
      status_logger.logger.info(f"Your Loki Service Node's last uptime proof was received at: {snlup_time}")
    	
      current_timestamp = int(time.time())
      current_time = time.strftime('%b %d, %Y - %I:%M:%S %p', time.localtime(current_timestamp))

      status_logger.logger.info(f"The monitor server's current time is: {current_time}")

      # Compute time delta between current time and last uptime
      uptime_proof_age = current_timestamp - snlup
      if uptime_proof_age > 3960:
        status_logger.logger.warning(f"Service Node uptime proof is over one hour and six minutes old. Check on Service Node immediately.")
        uptime_warning_subject = "URGENT: Loki Service Node Uptime Proof not received"
        uptime_warning_body = f"Your Loki Service Node uptime proof was last accepted by the network at {snlup_time}, over {uptime_proof_age} seconds ago. Check on your Service Node immediately."
        yag.send(TO, uptime_warning_subject, uptime_warning_body)
        time.sleep(300)
      else:
        status_logger.logger.info(f"Loki service node operational. Last uptime proof accepted at: {snlup_time}. Last uptime proof accepted {uptime_proof_age} seconds ago.")
        time.sleep(300)
    except KeyboardInterrupt:
      sys.exit()
    except (Timeout, ConnectTimeout, ReadTimeout) as e:
      status_logger.logger.exception("Exception occured\n")
      time.sleep(60)
      try:
        status_logger.logger.info("Reconnecting...")
        url = node_selector(node_list)
        if url == None:
          status_logger.logger.warning("Unable to connect to a Loki remote node.")
          no_node_subj = "Unable to connect to a Loki remote node."
          no_node_body = "Unable to connect to a Loki remote node. No nodes in your node list were available. Your service node monitor has stopped. Please investigate the issue."
          yag.send(TO, no_node_subj, no_node_body)
          raise ValueError("Unable to connect to a Loki remote node. Remote node cannot be 'None'.")
        else:
          status_logger.logger.info(f"Connected to: {url}")
      except ValueError as error:
        status_logger.logger.exception("Exception occured\n")
        sys.exit()
    except Exception as e:
      status_logger.logger.exception("Exception occured\n")