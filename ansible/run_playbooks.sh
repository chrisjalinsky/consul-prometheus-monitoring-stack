#!/bin/bash

# $1 is playbook to run string
# $2 is inventory string
# $3 is filename string

function run_playbook () {
  echo "Running: ansible-playbook $1 -i $2 at $(date)"
  ansible-playbook $1 -i $2 >> $3 2>&1
  if [ $? -eq 0 ]; then
    echo "Success."
  else
    echo "Unsuccessful playbook. Error Code $?"
    exit 1
  fi
}

echo "Beginning Installation at $(date)."

run_playbook provision_hostsfile.yaml inventory.py install.out
run_playbook provision_bind9_servers.yaml inventory.py install.out
run_playbook provision_resolv_conf.yaml inventory.py install.out
run_playbook provision_prometheus_servers.yaml inventory.py install.out
run_playbook provision_prometheus_alertmanager_servers.yaml inventory.py install.out
run_playbook provision_prometheus_node_exporter_servers.yaml inventory.py install.out
run_playbook provision_prometheus_consul_exporter_servers.yaml inventory.py install.out
run_playbook provision_consul_servers.yaml inventory.py install.out
run_playbook provision_consul_client_servers.yaml inventory.py install.out
run_playbook provision_consul_template_servers.yaml inventory.py install.out

echo "Ending Installation at $(date)."
