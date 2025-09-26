import os
import sys
import requests
import time
from dotenv import load_dotenv
import status_logger
import yagmail
from node_list import snode_list, remote_node_list

load_dotenv()

# ENV VARS
FROM = os.getenv('FROM_ADDRESS')
FROM_PASS = os.getenv('FROM_PASS')
TO = os.getenv('TO_ADDRESS')

# Initialize Yagmail
yag = yagmail.SMTP(FROM, FROM_PASS)


def convert(seconds):
    """
    Convert an integer of seconds to a human-readable Hour:Minute:Second format.
    :param seconds: Integer of seconds.
    :return: string: Human-readable Hour:Minute:Second format.
    """
    return time.strftime("%H:%M:%S", time.gmtime(seconds))


def calculate_allowed_downtime_remaining(earned_downtime_blocks):
    """
    Calculates the amount of allowed downtime left for a decommissioned node before it is deregistered.
    :param earned_downtime_blocks: Number of blocks of earned downtime left before deregistration.
    :return float: Hours of downtime remaining rounded to two decimal places.
    """
    earned_downtime_hours = round( ( earned_downtime_blocks * 2 ) / 60, 2)
    return earned_downtime_hours


def node_selector(node_list):
    """
    Connect to a Session remote node to get service node uptime data.
    :param node_list: List of Session remote nodes to query for service node data.
    :return: string: URL of the Session remote node that returned a 200 response.
    """
    for x in node_list:
        try:
            payload = {}
            r = requests.post(x, json=payload)
            if r.status_code == 200:
                node = x
                pass
            else:
                node = None
            return node
        except requests.exceptions.Timeout:
            status_logger.logger.exception("Timeout occurred\n")
            time.sleep(60)
            status_logger.logger.info("Reconnecting...")
            continue
        except Exception:
            status_logger.logger.exception("Exception occurred\n")


def no_node_alert():
    """
    If no remote node is available for connection. Call this function to trigger an alert.
    :return: Void.
    :raise: TypeError.
    """
    status_logger.logger.warning("Unable to connect to a Session remote node.")
    no_node_subj = "Unable to connect to a Session remote node."

    no_node_body = 'Unable to connect to a Session remote node. No nodes in your node list were available.' \
                   'Your service node monitor has stopped. Please investigate the issue.'

    yag.send(TO, no_node_subj, no_node_body)

    raise TypeError("Unable to connect to a Session remote node. Remote node cannot be 'None'.")


def get_deregistered_snodes(service_node_list, current_snode_stats):
    """
    This function creates a list of deregistered snode pubkeys by comparing the service_node_list
    and current_snode_stats.
    :param service_node_list: The list of service node pubkeys that we are monitoring.
    :param current_snode_stats: Dictionary of the JSON response we received from the remote node.
    :return list: A list of deregistered service node pubkeys.
    """

    #Get all the ed25519 pubkeys from the current_snode_stats and put into a temporary list.
    active_pubkeys = []
    for i in range(len(current_snode_stats['result']['service_node_states'])):
        active_pubkeys.append(current_snode_stats['result']['service_node_states'][i]['pubkey_ed25519'])

    deregistered_pubkeys = []
    for pubkey in service_node_list:
        if pubkey not in active_pubkeys:
            deregistered_pubkeys.append(pubkey)

    return deregistered_pubkeys


def snode_stats_getter(service_node_list, remote_node_url):
    """
    Retrieves the stats for all the service nodes in the provided list.
    :param service_node_list: List of service node public keys.
    :param remote_node_url: The URL of the remote full node that we get data from.
    :return service_node_stats: A dictionary of the JSON response received from the server.
    """
    try:
        service_node_stats = requests.post(remote_node_url,
                                 json={"jsonrpc": "2.0", "id": "0", "method": "get_service_nodes",
                                 "params": {"service_node_pubkeys": service_node_list}}, timeout=10).json()
    except requests.exceptions.Timeout:
        status_logger.logger.exception("Timeout occurred\n")
        time.sleep(60)
        attempt = 0
        while attempt < 10:
            status_logger.logger.info("Reconnecting...")
            remote_node_url = node_selector(remote_node_list)
            if remote_node_url is None:
                no_node_alert()
                time.sleep(60)
                attempt += 1
            else:
                status_logger.logger.info(f"Connected to: {remote_node_url}")
                return snode_stats_getter(service_node_list, remote_node_url)

    return service_node_stats

def stats_evaluator(sns):
    """
    Evaluates the service node data provided by the snode_stats_getter()
    :param sns: A dictionary of the JSON response received from the server.
    :return:
    """
    if 'service_node_states' not in sns['result']:
        # No nodes known to the network. Alert and bail.
        status_logger.logger.warning('None of the service nodes we are monitoring are known the network.')
        no_service_nodes_subject = 'URGENT: No service nodes known to the network'
        no_service_nodes_body = 'None of the service nodes that are being monitored are known to the network.\n' \
                                'Check on your service nodes immediately. They may be deregistered.\n' \
                                'Sleeping for one hour.'
        yag.send(TO, no_service_nodes_subject, no_service_nodes_body)
        time.sleep(3600)

    # Get the number of service nodes listed in the service_node_stats (sns):
    service_nodes_count = len(sns['result']['service_node_states'])

    # If this is true then one or more of our snodes are no longer known to the network. Send alert.
    if len(snode_list) > service_nodes_count:
        status_logger.logger.warning('One or more of our snodes have been deregistered. Sending alert.')
        deregistered_snodes = get_deregistered_snodes(snode_list, sns)
        deregistered_snodes_subject = f"URGENT: {len(deregistered_snodes)} service node(s) appear to be deregistered."
        deregistered_snodes_body = "The following service node(s) appear to be deregistered. If this is expected, " \
                "the only action required is to remove the below listed key(s) from your service node monitor.\n" \
                "If this is not expected, please check the following service nodes immediately as they are most " \
                "likely deregistered.\n"

        for pubkey in deregistered_snodes:
            deregistered_snodes_body += f"\t- {pubkey}\n"

        yag.send(TO, deregistered_snodes_subject, deregistered_snodes_body)


    # Get the last uptime proof for each snode from the response data:
    for i in range(service_nodes_count):
        current_snode = sns['result']['service_node_states'][i]['pubkey_ed25519']
        status_logger.logger.info(f"Checking service node: {current_snode}")

        snlup = sns['result']['service_node_states'][i]['last_uptime_proof']
        snlup_time = time.strftime('%b %d, %Y - %I:%M:%S %p', time.localtime(snlup))

        # Check if it is decommissioned first:
        if not sns['result']['service_node_states'][i]['active'] and 0 == snlup:
            # Snode is decommissioned. Send alert and include the amount of downtime remaining.
            status_logger.logger.warning(f"{current_snode} is decommissioned. Sending alert.")
            downtime_hours_remaining = calculate_allowed_downtime_remaining(
                sns['result']['service_node_states'][i]['earned_downtime_blocks']
            )
            decommissioned_snode_subject = "URGENT: Service node is decommissioned."
            decommissioned_snode_body = f"The following service node is decommissioned:\n\n" \
                f"{current_snode}\n\n" \
                f"Allowed downtime remaining: {downtime_hours_remaining} hours."
            yag.send(TO, decommissioned_snode_subject, decommissioned_snode_body)
            continue

        status_logger.logger.info(f"Your Session Service Node's last uptime proof was received at: {snlup_time}")

        # Get monitor server's current time.
        current_timestamp = int(time.time())
        current_time = time.strftime('%b %d, %Y - %I:%M:%S %p', time.localtime(current_timestamp))

        status_logger.logger.info(f"The monitor server's current time is: {current_time}")

        # Compute time delta between current time and last uptime
        uptime_proof_age = current_timestamp - snlup

        # Convert uptime_proof_age to Human Readable Uptime Proof Age (hrupa) HH:MM:SS:
        hrupa = convert(uptime_proof_age)

        if uptime_proof_age > 3960:
            status_logger.logger.warning(f"Service Node uptime proof is over one hour and six minutes old. " +
                                            f"Check on the following Service Node immediately: " +
                                            f"{current_snode}")

            uptime_warning_subject = "URGENT: Session Service Node Uptime Proof not received"

            uptime_warning_body = (f"Your Session Service Node uptime proof was last accepted by the network at " 
                                    f"{snlup_time}, over {uptime_proof_age} seconds ago.\n\nCheck on the following "
                                    f"Service Node immediately:\n\n{current_snode}")

            yag.send(TO, uptime_warning_subject, uptime_warning_body)
        else:
            status_logger.logger.info(f"Session service node operational. Last uptime proof accepted at: "
                                          f"{snlup_time}.")
            status_logger.logger.info(f"Last uptime proof accepted {hrupa} ago.")
            status_logger.logger.info('-' * 130)


def main():
    try:
        url = node_selector(remote_node_list)
        if url is None:
            no_node_alert()
        else:
            status_logger.logger.info(f"Connected to: {url}")
            status_logger.logger.info("Getting your Session Service Node last uptime proof.")

        response = snode_stats_getter(snode_list, url)

        stats_evaluator(response)

        time.sleep(300)
    except KeyboardInterrupt:
        sys.exit()
    except TypeError:
        status_logger.logger.exception("Exception occurred\n")
        sys.exit()
    except Exception:
        status_logger.logger.exception("Exception occurred\n")


if __name__ == "__main__":

    while True:
        main()
