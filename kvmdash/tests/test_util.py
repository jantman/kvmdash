"""
Tests for the util module
"""

import pytest

from kvmdash.util import calculate_host_resources

def test_calculate_host_resources():
    hosts = {}
    hosts['foo'] = {"data": {"maxvcpus": 16, "df_bytes": 12345678, "hostname": "foo", "memory_bytes": 1000}, "type": "host", "name": "foo"}
    hosts['bar'] = {"data": {"maxvcpus": 10, "df_bytes": 12345678, "hostname": "bar", "memory_bytes": 100}, "type": "host", "name": "bar"}
    hosts['baz'] = {"data": {"maxvcpus": 10, "df_bytes": 12345678, "hostname": "baz", "memory_bytes": 100}, "type": "host", "name": "baz"}
    guests = {}
    guests['guest1'] = {"data": {"bridges": [{"mac": "52:54:00:a9:93:d5", "model": "virtio"}], "UUID": "786584D0-DD1B-0D0D-8551-63DB7B0D260D", "vcpus": 4, "memory_bytes": 80, "state": "running", "disk_files": ["/var/lib/libvirt/images/guest1-disk0"], "type": "kvm", "ID": 1, "name": "guest1"}, "host": "bar", "type": "guest", "name": "guest1", "uuid": "786584D0-DD1B-0D0D-8551-63DB7B0D260D"}
    guests['guest2'] = {"data": {"bridges": [{"mac": "52:54:00:18:ad:18", "model": "virtio"}], "UUID": "86753771-646C-A7BE-737C-4AE0454E01C9", "vcpus": 2, "memory_bytes": 500, "state": "running", "disk_files": ["/var/lib/libvirt/images/guest2-disk0"], "type": "kvm", "ID": 12, "name": "guest2"}, "host": "foo", "type": "guest", "name": "guest2", "uuid": "86753771-646C-A7BE-737C-4AE0454E01C9"}
    guests['guest3'] = {"data": {"bridges": [{"mac": "00:16:3e:5f:cc:44", "model": "virtio"}], "UUID": "40357270-17EE-F043-8B9A-4AA6BC3AFDB2", "vcpus": 8, "memory_bytes": 320, "state": "running", "disk_files": ["/var/lib/libvirt/images/guest3-disk0"], "type": "kvm", "ID": 18, "name": "guest3"}, "host": "foo", "type": "guest", "name": "guest3", "uuid": "40357270-17EE-F043-8B9A-4AA6BC3AFDB2"}
    desired = {}
    desired['foo'] = {"data": {"maxvcpus": 16, "df_bytes": 12345678, "hostname": "foo", "memory_bytes": 1000, 'allocated_vcpus': 10, 'unallocated_vcpus': 6, 'allocated_memory_bytes': 820, 'unallocated_memory_bytes': 180, 'num_guests': 2}, "type": "host", "name": "foo"}
    desired['bar'] = {"data": {"maxvcpus": 10, "df_bytes": 12345678, "hostname": "bar", "memory_bytes": 100, 'allocated_vcpus': 4, 'unallocated_vcpus': 6, 'allocated_memory_bytes': 80, 'unallocated_memory_bytes': 20, 'num_guests': 1}, "type": "host", "name": "bar"}
    desired['baz'] = {"data": {"maxvcpus": 10, "df_bytes": 12345678, "hostname": "baz", "memory_bytes": 100, 'allocated_vcpus': 0, 'unallocated_vcpus': 10, 'allocated_memory_bytes': 0, 'unallocated_memory_bytes': 100, 'num_guests': 0}, "type": "host", "name": "baz"}

    result = calculate_host_resources(hosts, guests)

    assert result == desired
