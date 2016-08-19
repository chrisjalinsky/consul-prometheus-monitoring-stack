deps:
	cd /vagrant/consul-template
	wget -q -nc https://releases.hashicorp.com/consul-template/0.14.0/consul-template_0.14.0_linux_amd64.zip
	apt-get update -qq
	apt-get install -y unzip
	unzip -o consul-template_0.14.0_linux_amd64.zip

install:
	cd /vagrant/consul-template

	# Get IP address of the current machine from eth1
	ifconfig eth1 | grep "inet addr" | awk 'BEGIN { FS = "[ :]+" }{print $$4}' > /tmp/self.ip

	# Install consul binaries
	cp /vagrant/consul-template/consul-template /usr/local/bin/consul-template
