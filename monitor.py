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

yag = yagmail.SMTP(FROM, FROM_PASS)

while True:
  # Add your preferred Loki public node URL:
  url = 'http://imaginary.stream:22023'
  while True:	
    try:
      status_logger.logger.info(f"Pinging Loki public node: {url}")	
      r = requests.get(url + '/get_info', timeout=10)
      if r.status_code != 200:
        status_logger.logger.warning(f"Loki public node returned status code {r.status_code}.")
        pnd_subject = "Loki Public Node is down"
        pnd_body = f"Loki public node, {url}, returned status code {r.status_code}. Recommend manually checking your service node status."
        yag.send(TO, pnd_subject, pnd_body)
        time.sleep(300)
      else:
        status_logger.logger.info(f"Loki public node is available. Node returned status code {r.status_code}.")
        break
    except KeyboardInterrupt:
      sys.exit()
    except Exception as e:
      status_logger.logger.exception("Exception occured\n")
    
  status_logger.logger.info("Getting your Loki Service Node last uptime proof.")

  try:    
    sns = requests.post(url + '/json_rpc', json={"jsonrpc":"2.0","id":"0","method":"get_service_nodes", "params": {"service_node_pubkeys": [SNODE_PUBKEY]}}, 
      timeout=10).json()

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
  except Exception as e:
    status_logger.logger.exception("Exception occured\n")