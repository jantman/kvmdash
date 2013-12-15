#!/usr/bin/env python
"""
Test of using the LibVirt Python bindings to gather
information about libvirt (qemu/KVM) guests.

"""

import libvirt
import sys
import libxml2
import subprocess
import time

try:
    import anyjson
    to_json = anyjson.serialize
except ImportError:
    import json
    to_json = json.dumps

if len(sys.argv) > 1:
    hostname = sys.argv[1]
else:
    print("USAGE: test_libvirt.py <hostname> <...>")
    sys.exit(1)

VERBOSE = False

DOM_STATES = {
    libvirt.VIR_DOMAIN_NOSTATE: 'no state',
    libvirt.VIR_DOMAIN_RUNNING: 'running',
    libvirt.VIR_DOMAIN_BLOCKED: 'blocked on resource',
    libvirt.VIR_DOMAIN_PAUSED: 'paused by user',
    libvirt.VIR_DOMAIN_SHUTDOWN: 'being shut down',
    libvirt.VIR_DOMAIN_SHUTOFF: 'shut off',
    libvirt.VIR_DOMAIN_CRASHED: 'crashed',
    libvirt.VIR_DOMAIN_PMSUSPENDED: 'suspended by guest power mgmt',
}

# bitwise or of all possible flags to virConnectListAllDomains
ALL_OPTS = 16383

def bool(a):
    if a == 0:
        return False
    return True

def xml_get(ctx, path):
    res = ctx.xpathEval(path)
    if res is None or len(res) == 0:
        return None
    return res[0].content

def parse_domain_xml(x):
    """
    Parse relevant information from domain XML.
    """
    ret = {}
    doc = libxml2.parseDoc(x)
    ctx = doc.xpathNewContext()

    ret['type'] = xml_get(ctx, "/domain/@type")
    memory = int(xml_get(ctx, "/domain/memory"))
    memory_units = xml_get(ctx, "/domain/memory/@unit")
    if memory_units == 'KiB':
        memory = memory * 1024
    ret['memory_bytes'] = memory
    vcpu = xml_get(ctx, "/domain/vcpu")
    ret['vcpus'] = int(vcpu)

    disk_files = []
    bridges = []

    devs = ctx.xpathEval("/domain/devices/*")
    for d in devs:
        ctx.setContextNode(d)
        type = xml_get(ctx, "@type")
        if type == "file":
            disk_files.append(xml_get(ctx, "source/@file"))
        elif type == "bridge":
            foo = {}
            foo['mac'] = xml_get(ctx, "mac/@address")
            foo['model'] = xml_get(ctx, "model/@type")
            bridges.append(foo)
    ret['bridges'] = bridges
    ret['disk_files'] = disk_files
    return ret

def get_domains(conn):
    """
    Takes a libvirt connection object,
    returns a list of all domains, each element
    being a dict with items "name", "ID", "UUID", "state"

    This method first tries to use the listAllDomains (virConnectListAllDomains)
    method, which was introduced in libvirt 0.9.13, as a workaround to the inherent
    race condition when calling listDefinedDomains (virConnectListDefinedDomains)
    and listDomains (virConnectListDomains) sequentially. If this raises an error,
    we fall back to the potentially racey method.
    """
    try:
        domains = conn.listAllDomains(ALL_OPTS)
    except libvirt.libvirtError:
        # ok, we're < 0.9.13 :(
        # really ugly, we have a function that lists running domains by ID,
        # and a function that lists stopped domains by name. ugh.
        domains = []
        names = conn.listDefinedDomains()
        for n in names:
            foo = conn.lookupByName(n)
            domains.append(foo)
        IDs = conn.listDomainsID()
        for i in IDs:
            foo = conn.lookupByID(i)
            domains.append(foo)
    ret = []
    for d in domains:
        foo = {}
        foo['name'] = d.name()
        foo['ID'] = d.ID()
        foo['UUID'] = d.UUIDString().upper()
        [state, maxmem, mem, ncpu, cputime] = d.info()
        foo['state'] = DOM_STATES.get(state, state)
        x = d.XMLDesc(0)
        foo.update(parse_domain_xml(x))
        ret.append(foo)
    return ret

def get_host_info(conn):
    """
    get info about the VM host
    """
    ret = {}
    ret['hostname'] = conn.getHostname()
    (model, memory, cpus, mhz, nodes, sockets, cores, threads) = conn.getInfo() # http://libvirt.org/html/libvirt-libvirt.html#virNodeInfo
    ret['maxvcpus'] = conn.getMaxVcpus('qemu')
    ret['memory_bytes'] = int(memory) * 1024 * 1024 # want bytes
    return ret

def run_command(cmd):
    """
    run a command via subprocess, return a string
    of the command's STDOUT
    """
    pipe = subprocess.Popen(cmd,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=None)
    output = pipe.communicate()[0]
    status = pipe.returncode
    return output

def get_disk_free(image_paths, hostname=None):
    """
    Given a list of VM image file paths,
    return the total bytes free on all local
    filesystems containing the images.

    if hostname is not None, run command over SSH to hostname.

    :param hostname: hostname of remote host, or None for localhost
    :type hostname: string
    """
    if len(image_paths) == 0:
        image_paths = ['/var/lib/libvirt']
    cmd = "df -lP -B 1 %s | grep -v '^Filesystem' | sort | uniq" % (" ".join(image_paths))
    if VERBOSE:
        print("running command: %s" % cmd)
    if hostname is not None:
        cmd = "ssh %s 'df -lP -B 1 %s' | grep -v '^Filesystem' | sort | uniq" % (hostname, " ".join(image_paths))
    total_avail = 0
    for line in run_command(cmd).split("\n"):
        line = line.strip()
        if not line:
            continue
        fs, size, used, avail, use_percent, mpoint = line.split()
        total_avail += int(avail)
    return total_avail

hosts = sys.argv
hosts.pop(0)

for h in hosts:
    if h == "-v" or h == "--verbose":
        VERBOSE = True
        continue

    uri = "qemu+ssh://%s/system" % h

    try:
        conn = libvirt.openReadOnly(uri)
    except libvirt.libvirtError as e:
        print("ERROR connecting to %s: %s" % (uri, e.message))
        continue

    # some code examples imply that older versions
    # returned None instead of raising an exception
    if conn is None:
        print("ERROR connecting to %s: %s" % (uri, e.message))
        continue

    host_info = get_host_info(conn)

    doms = get_domains(conn)

    image_paths = []
    for d in doms:
        image_paths.extend(d['disk_files'])

    df = get_disk_free(image_paths, h)
    host_info['df_bytes'] = df

    ts = int(time.time())
    foo = {'type': 'host', 'name': host_info['hostname'], 'data': host_info, 'updated_ts': ts}
    print to_json(foo)
    with open("host_%s.json" % host_info['hostname'], 'w') as fh:
        fh.write(to_json(foo))

    for d in doms:
        #print("{host},{name},{ID},{state},{UUID}".format(host=h, name=d['name'], ID=d['ID'], UUID=d['UUID'], state=d['state']))
        foo = {'type': 'guest', 'name': d['name'], 'uuid': d['UUID'], 'data': d, 'host': host_info['hostname'], 'updated_ts': ts}
        print to_json(foo)
        with open("host_%s_guest_%s.json" % (host_info['hostname'], d['name']), 'w') as fh:
            fh.write(to_json(foo))
