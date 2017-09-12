# Consul Prometheus Monitoring Stack

### Goals:
* Create [Bind9](https://wiki.debian.org/Bind9) DNS environment
* Create [Consul](https://github.com/hashicorp/consul) cluster used for service discovery
* Create [Prometheus](https://github.com/prometheus) Server cluster
* Create [Prometheus AlertManager](https://github.com/prometheus/alertmanager) service on defined nodes
* Create [Prometheus NodeExporter](https://github.com/prometheus/node_exporter) service on defined nodes
* Create Prometheus [Rules](https://prometheus.io/docs/querying/rules/)/[Alerts](https://prometheus.io/docs/alerting/rules/)
* Create [Third Party Exporter](https://github.com/prometheus/consul_exporter)
* Create [Grafana](https://github.com/grafana/grafana) service
* Create [Haproxy](http://www.haproxy.org/) load balancer
* Create [Consul Template](https://github.com/hashicorp/consul-template) service

## Network Environment
**GOAL:** Install Bind9 DNS master into the private network to resolve hostname A records and reverse DNS.

## Consul Cluster
**GOAL:** Install a 3 mode Consul cluster for service discovery and DNS

## HA Prometheus Cluster
**GOAL:** Install a HA Prometheus cluster for monitoring, metrics, alerting, and consul forwarding

## Haproxy load balancing
**GOAL:** Install Haproxy to verify consul template functionality

### Vagrantfile

The Vagrantfile reads the ```./ansible/hosts.yaml``` to create the machines. This also serves as the inventory file for the plays listed below. You might want to use the great plugin [Vagrant HostsUpdater](https://github.com/cogitatio/vagrant-hostsupdater) to update your hypervisor's hostsfile:
```
vagrant plugin install vagrant-hostsupdater
```

Spin up the infrastructure:
```
vagrant up
```

This will, by default, create:
* core1.lan - bind9 DNS server, Consul Client
* prometheus1.lan - Prometheus server, Prometheus AlertManager, Grafana server
* prometheus2.lan - Prometheus server, Prometheus AlertManager, Grafana server
* consul1.lan - Consul Server, Consul Client, Prometheus node exporter
* consul2.lan - Consul Server, Consul Client, Prometheus node exporter
* consul3.lan - Consul Server, Consul Client, Prometheus node exporter
* client1.lan - Consul Client, Prometheus node exporter, Consul Template service with Haproxy cfg template

### Ansible playbooks

The ansible playbooks provision the nodes listed above. The Ansible roles have been created to work on Ubuntu 14 and Ubuntu 16 nodes, but the playbooks will need updated to use the correct network interface names, as well as changing the Vagrant box in the ```./ansible/hosts.yaml``` file.

Run all playbooks in order:
```
cd ansible
./run_playbooks.sh
```

Or manually run to playbooks:
```
cd ansible
ansible-playbook provision_bind9_servers.yaml -i inventory.py -u vagrant -k -b
ansible-playbook provision_prometheus_servers.yaml -i inventory.py -u vagrant -k -b
ansible-playbook provision_prometheus_alertmanager_servers.yaml -i inventory.py -u vagrant -k -b
ansible-playbook provision_prometheus_node_exporter_servers.yaml -i inventory.py -u vagrant -k -b
ansible-playbook provision_prometheus_consul_exporter_servers.yaml -i inventory.py -u vagrant -k -b
ansible-playbook provision_consul_servers.yaml inventory.py -i inventory.py -u vagrant -k -b
ansible-playbook provision_consul_client_servers.yaml -i inventory.py -u vagrant -k -b
ansible-playbook provision_consul_template_servers.yaml -i inventory.py -u vagrant -k -b
```

### Notable UIs

**Prometheus Server UIs:**
* prometheus1.lan:9090
* prometheus2.lan:9090

**Grafana UIs:**
* prometheus1.lan:3000 admin:admin
* prometheus2.lan:3000 admin:admin

**Consul UIs:**
* consul1.lan:8500
* consul2.lan:8500
* consul3.lan:8500

**Haproxy Admin:**
* client1.lan:8888 admin:adminpw
