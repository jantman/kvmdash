kvmdash
=======

**Note this code is VERY alpha right now. Expect it to change a lot and maybe
  not work.**

kvmdash is a simple Python daemon and web app to collect information about libvirt-controlled qemu/kvm guest VMs running on standalone hosts, ans present the information on a single web page (with a simple API). It will also include a companion Puppet module for installation, and Facter facts that make use of the data.

kvmdash is made up of two parts:
* a python client script (kvmdash-client.py) that queries information on local
and/or remote libvirt hosts and libvirt-managed qemu-kvm VMs, and reports it
back to the web API.
* a web application that receives and stores information from clients, and
presents it to users (as HTML) and over an API.

In addition, the project will include some supplemental parts such as:
* puppet module to install and run the web app and client
* puppet/facter facts to leverage the web app API to determine a guest's
current physical host
