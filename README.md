# Consul Prometheus Monitoring Stack

### Goals:
* Create [Bind9](https://wiki.debian.org/Bind9){:target="_blank"} DNS environment
* Create [Consul](https://github.com/hashicorp/consul){:target="_blank"} cluster used for service discovery
* Create [Prometheus](https://github.com/prometheus){:target="_blank"} Server cluster
* Create [Prometheus AlertManager](https://github.com/prometheus/alertmanager){:target="_blank"} service on defined nodes
* Create [Prometheus NodeExporter](https://github.com/prometheus/node_exporter){:target="_blank"} service on defined nodes
* Create Prometheus [Rules](https://prometheus.io/docs/querying/rules/)/[Alerts](https://prometheus.io/docs/alerting/rules/){:target="_blank"}
* Create [Third Party Exporter](https://github.com/prometheus/consul_exporter){:target="_blank"}
* Create [Grafana](https://github.com/grafana/grafana){:target="_blank"} service
* Create [Haproxy](http://www.haproxy.org/){:target="_blank"} load balancer
* Create [Consul Template](https://github.com/hashicorp/consul-template){:target="_blank"} service

## Network Environment
**GOAL:** Install Bind9 DNS master into the private network to resolve hostname A records and reverse DNS.

## Consul Cluster
**GOAL:** Install a 3 mode Consul cluster for service discovery and DNS

## HA Prometheus Cluster
**GOAL:** Install a HA Prometheus cluster for monitoring, metrics, alerting, and consul forwarding

## Haproxy load balancing
**GOAL:** Install Haproxy to verify consul template functionality

### Vagrantfile

The Vagrantfile reads the ```./ansible/hosts.yaml``` to create the machines. This also serves as the inventory file for the plays listed below. You might want to use the great plugin [Vagrant HostsUpdater](https://github.com/cogitatio/vagrant-hostsupdater){:target="_blank"} to update your hypervisor's hostsfile:
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

### Verify Consul DNS:

**Check Forward DNS with nslookup:**

DNS lookup the consul-exporter service:
```
root@client1:~# nslookup prometheus.service.consul
Server:		172.136.1.11
Address:	172.136.1.11#53

Non-authoritative answer:
Name:	prometheus.service.consul
Address: 172.136.2.12
Name:	prometheus.service.consul
Address: 172.136.2.13
Name:	prometheus.service.consul
Address: 172.136.2.11

```
DNS lookup the grafana service:
```
root@client1:~# nslookup bind.service.consul
Server:		172.136.1.11
Address:	172.136.1.11#53

Non-authoritative answer:
Name:	bind.service.consul
Address: 172.136.1.11
```

**Check reverse DNS with dig**

DNS Reverse lookup a node ip address
```
root@client1:~# dig -x 172.136.2.11

; <<>> DiG 9.9.5-3ubuntu0.14-Ubuntu <<>> -x 172.136.2.11
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 17545
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 2, ADDITIONAL: 3

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;11.2.136.172.in-addr.arpa.	IN	PTR

;; ANSWER SECTION:
11.2.136.172.in-addr.arpa. 604800 IN	PTR	consul1.lan.

;; AUTHORITY SECTION:
2.136.172.in-addr.arpa.	604800	IN	NS	core2.lan.
2.136.172.in-addr.arpa.	604800	IN	NS	core1.lan.

;; ADDITIONAL SECTION:
core1.lan.		604800	IN	A	172.136.1.11
core2.lan.		604800	IN	A	172.136.1.12

;; Query time: 4 msec
;; SERVER: 172.136.1.11#53(172.136.1.11)
;; WHEN: Tue Sep 12 03:17:20 UTC 2017
;; MSG SIZE  rcvd: 151
```

### Notable UIs

**Prometheus Server UIs:**
* [Prometheus UI on prometheus1.lan](http://prometheus1.lan:9090){:target="_blank"}
* [Prometheus UI on prometheus2.lan](http://prometheus2.lan:9090){:target="_blank"}
* [Load Balanced Prometheus UI](http://client1.lan:9090){:target="_blank"}

**Grafana UIs:**

Additionally, Create a new prometheus datasource in Grafana.

* [Grafana UI on prometheus1.lan](http://prometheus1.lan:3000){:target="_blank"} admin:admin
* [Grafana UI on prometheus2.lan](http://prometheus2.lan:3000){:target="_blank"} admin:admin
* [Load Balanced Grafana UI](http://client1.lan:3000){:target="_blank"} (Load balanced)

**Consul UIs:**
* [Consul 1 Admin UI](http://consul1.lan:8500/ui/#){:target="_blank"}
* [Consul 2 Admin UI](http://consul2.lan:8500/ui/#){:target="_blank"}
* [Consul 3 Admin UI](http://consul3.lan:8500/ui/#){:target="_blank"}

**Haproxy Admin:**

To illustrate the usage of consul template, Grafana and the Prometheus admin are load balanced:

* [Haproxy Admin UI](http://client1.lan:8888){:target="_blank"} admin:adminpw
