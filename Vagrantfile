require 'yaml'

VAGRANTFILE_API_VERSION = "2"

base_dir = File.expand_path(File.dirname(__FILE__))
inventory_file = base_dir + "/ansible/hosts.yaml"

servers = YAML.load_file(inventory_file)
meta = servers["_meta"]

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  
  config.vm.box = "bento/ubuntu-16.04"
  config.ssh.insert_key = false
  
  if Vagrant.has_plugin?("vagrant-vbguest")
    config.vbguest.auto_update = false
  end

  servers.each do |ansible_key,vars|
    vars["hosts"].each_with_index do |host,i|
    
      ip  = meta["hostvars"][host]["vagrant_ip"]  ? meta["hostvars"][host]["vagrant_ip"]  : "10.0.0.#{i + 10}"
      cpu = meta["hostvars"][host]["vagrant_cpu"] ? meta["hostvars"][host]["vagrant_cpu"] : 1
      mem = meta["hostvars"][host]["vagrant_mem"] ? meta["hostvars"][host]["vagrant_mem"] : 2048
      box = meta["hostvars"][host]["vagrant_box"] ? meta["hostvars"][host]["vagrant_box"] : "bento/ubuntu-16.04"
      
      config.vm.define "#{host}" do |node|
        node.vm.network "private_network", ip: "#{ip}"
        #node.vm.network :public_network, ip: "#{ip}", bridge: "br0"
        node.vm.hostname = "#{host}"
        config.vm.provider "virtualbox" do |v, override|
          override.vm.box = "#{box}"
          v.memory = "#{mem}"
          v.cpus = "#{cpu}"
        end
      end
      
    end if vars["hosts"]
  end

end
