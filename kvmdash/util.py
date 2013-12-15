"""
Utility functions for the webapp
"""

def calculate_host_resources(hosts, guests):
    """
    Calculate resource (vcpu and memory) allocation
    and free resources on all hosts in the hosts dict,
    given the guests dict.

    Calculates values for and fills in the following elements
    in each hosts 'data' dict:
    - allocated_vcpus
    - unallocated_vcpus
    - allocated_memory_bytes
    - unallocated_memory_bytes

    :param hosts: get_all_hosts() dict or a subset thereof
    :param guests: get_all_guests() dict or a subset thereof
    :rtype: dict
    """
    for g in guests:
        d = guests[g]
        host = d['host']
        if 'num_guests' not in hosts[host]['data']:
            hosts[host]['data']['num_guests'] = 0
        hosts[host]['data']['num_guests'] += 1
        if 'allocated_memory_bytes' not in hosts[host]['data']:
            hosts[host]['data']['allocated_memory_bytes'] = 0
        hosts[host]['data']['allocated_memory_bytes'] += d['data']['memory_bytes']
        if 'allocated_vcpus' not in hosts[host]['data']:
            hosts[host]['data']['allocated_vcpus'] = 0
        hosts[host]['data']['allocated_vcpus'] += d['data']['vcpus']

    for h in hosts:
        if 'allocated_memory_bytes' not in hosts[h]['data']:
            hosts[h]['data']['allocated_memory_bytes'] = 0
        if 'allocated_vcpus' not in hosts[h]['data']:
            hosts[h]['data']['allocated_vcpus'] = 0
        if 'num_guests' not in hosts[h]['data']:
            hosts[h]['data']['num_guests'] = 0
        hosts[h]['data']['unallocated_vcpus'] = hosts[h]['data']['maxvcpus'] - hosts[h]['data']['allocated_vcpus']
        hosts[h]['data']['unallocated_memory_bytes'] = hosts[h]['data']['memory_bytes'] - hosts[h]['data']['allocated_memory_bytes']
    return hosts
