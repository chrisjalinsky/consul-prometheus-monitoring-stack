##Network Environment
We install Bind9 DNS into the private network to resolve hostname A records and reverse DNS.



##Consul Cluster
We install a Consul cluster for service discovery and DNS

##HA Prometheus Cluster

###Overview
* Create a superset DNS environment
* Create [Consul](https://github.com/hashicorp/consul) cluster used for service discovery
* Create [Prometheus](https://github.com/prometheus) Server cluster
* Create [Prometheus AlertManager](https://github.com/prometheus/alertmanager) service on defined nodes
* Create [Prometheus NodeExporter](https://github.com/prometheus/node_exporter) service on defined nodes
* Create Prometheus [Rules](https://prometheus.io/docs/querying/rules/)/[Alerts](https://prometheus.io/docs/alerting/rules/)
* Create [Third Party Exporter](https://github.com/prometheus/consul_exporter)
* Create [Grafana](https://github.com/grafana/grafana) service

###Prometheus Servers

####Starting the prometheus binary
```
prometheus -config.file=/etc/prometheus/config.yml
```

###Prometheus Clients

####Node Exporter on everything

####Starting the node_exporter binary
```
node_exporter
```

####Consul Exporter on consul server nodes

####Starting the consul_exporter binary
```
consul_exporter
```