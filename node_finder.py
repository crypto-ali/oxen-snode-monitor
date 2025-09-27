import os
import sys
import time
import requests
from dotenv import load_dotenv
import status_logger
import yagmail
from node_list import remote_node_list
from monitor import node_selector

load_dotenv()

# ENV VARS
FROM = os.getenv('FROM_ADDRESS')
FROM_PASS = os.getenv('FROM_PASS')
TO = os.getenv('TO_ADDRESS')

# Initialize Yagmail
yag = yagmail.SMTP(FROM, FROM_PASS)


def open_snode_finder(remote_node_url, min_val, max_val):
    payload = {"jsonrpc": "2.0", "id": "0", "method": "get_service_nodes", "params": {"service_node_pubkeys": []}}
    r = requests.post(remote_node_url, json=payload).json()

    all_snodes = r['result']['service_node_states']

    awaiting_contribution = []

    for index, item in enumerate(all_snodes):
        if all_snodes[index]['active'] is False:
            awaiting_contribution.append(item)

    matching_nodes = []

    for index, item in enumerate(awaiting_contribution):
        open_for_contribution = (item['staking_requirement'] - item['total_contributed']) / 1000000000
        spots_available = 4 - len(item['contributors'])
        minimum_contribution = open_for_contribution / spots_available
        if min_val <= open_for_contribution <= max_val \
                or min_val <= minimum_contribution <= max_val \
                or minimum_contribution < min_val <= open_for_contribution / 2 <= max_val:
            matched_pubkey = item['service_node_pubkey']
            matched_tuple = (matched_pubkey, open_for_contribution, minimum_contribution, spots_available)
            matching_nodes.append(matched_tuple)

    return matching_nodes


if __name__ == '__main__':
    min_amt = input("What is the minimum amount of SESH you are looking to stake?\n>> ")
    max_amt = input("What is the maximum amount of SESH you can stake?\n>> ")
    min_amt = int(min_amt)
    max_amt = int(max_amt)

    while True:
        try:
            url = node_selector(remote_node_list)
            if url is None:
                status_logger.logger.error("Unable to connect to a Session remote node. Please try again later.\n")
                sys.exit()
            else:
                status_logger.logger.info(f"Connected to: {url}")
                status_logger.logger.info("Searching for open service nodes")
        except KeyboardInterrupt:
            sys.exit()
        except TypeError as te:
            status_logger.logger.exception("TypeError occurred\n")
            sys.exit()
        except Exception as e:
            status_logger.logger.exception("Exception occurred\n")

        try:
            open_snodes = open_snode_finder(url, min_amt, max_amt)
            if len(open_snodes) == 0:
                status_logger.logger.info("Found 0 nodes. Sleeping 5 minutes.")
                time.sleep(300)
            else:
                status_logger.logger.info(f"Found {len(open_snodes)} nodes.")
                subject = f"Found {len(open_snodes)} open snodes."
                msg = f""
                for i in open_snodes:
                    msg += f"Service Node PubKey: {i[0]}\n\tOpen for contribution: {i[1]}\n\t" \
                           f"Minimum contribution: {i[2]}\n\t" \
                           f"Spots remaining: {i[3]}\n\n"
                yag.send(TO, subject, msg)
                status_logger.logger.info("Notification sent. Sleeping 5 minutes.")
                time.sleep(300)
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            status_logger.logger.exception("Exception occurred\n")
