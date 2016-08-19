def hash_to_tuples(h):
    return h.items()

def hash_keys(h):
    return h.keys()

def hash_values(h):
    return h.values()

def zipped_hash(h, key, item):
    ret = []
    for el in h:
        if h[el].has_key(item):
            for subel in h[el][item]:
                ret.append({"key" : h[el][key], "value" : subel })
    return ret

def server_group_filter(d,l,i):
    result = []
    if len(l) > 0:
        for item in l:
            if item != i:
                try:
                    ip_addr = d[item]['ansible_eth1']['ipv4']['address']
                    if ip_addr:
                        result.append(ip_addr)
                except:
                    pass
    return result

def server_group_filter_v2(d,l,i,iface='ansible_eth1'):
    result = []
    if len(l) > 0:
        for item in l:
            if item != i:
                try:
                    ip_addr = d[item][iface]['ipv4']['address']
                    if ip_addr:
                        result.append(ip_addr)
                except:
                    pass
    return result

def server_group_ip_map(d,l):
    result = []
    if len(l) > 0:
        for item in l:
            try:
                ip_addr = d[item]['ansible_eth1']['ipv4']['address']
                if ip_addr:
                    result.append(ip_addr)
            except:
                pass
    return result

def server_group_ip_map_v2(d,l,iface='ansible_eth1'):
    result = []
    if len(l) > 0:
        for item in l:
            try:
                ip_addr = d[item][iface]['ipv4']['address']
                if ip_addr:
                    result.append(ip_addr)
            except:
                pass
    return result

def user_at_ip_map_v2(d,l,iface='ansible_eth1',user='root'):
    result = []
    if len(l) > 0:
        for item in l:
            try:
                ip_addr = d[item][iface]['ipv4']['address']
                if ip_addr:
                    user_at_str = "%s@%s" % (user, ip_addr)
                    result.append(user_at_str)
            except:
                pass
    return result

def server_group_ip_port_map_v2(d,l,iface,port):
    result = []
    if len(l) > 0:
        for item in l:
            try:
                ip_addr = d[item][iface]['ipv4']['address']
                if ip_addr:
                    ip_port_string = ip_addr + " port " + port
                    result.append(ip_port_string)
            except:
                pass
    return result


def etcd_inventory_list(d,name,iface,port,local="no"):
    result = []
    if d[name]:
        if local != "no":
            local_str = "http://" + local + ":" + port
            result.append(local_str)
        try:
            ip_addr = d[name][iface]['ipv4']['address']
            if ip_addr:
                ip_port_string = "http://" + ip_addr + ":" + port
                result.append(ip_port_string)
        except:
            pass
    return result

def etcd_masters_list(d,l,iface,port1):
    result = []
    if len(l) > 0:
        for item in l:
            try:
                ip_addr = d[item][iface]['ipv4']['address']
                
                if ip_addr:
                    string1 = "http://" + ip_addr + ":" + port1
                    result.append(string1)
            except:
                pass
    return result


def etcd_cluster_list(d,l,iface,port1):
    result = []
    if len(l) > 0:
        for item in l:
            try:
                ip_addr = d[item][iface]['ipv4']['address']
                
                if ip_addr:
                    string1 = item + "=http://" + ip_addr + ":" + port1
                    result.append(string1)
            except:
                pass
    return result

def server_group_consul_map_v2(d,l,iface='eth1'):
    result = []
    if len(l) > 0:
        for item in l:
            try:
                ip_addr = d[item]['ansible_'+iface]['ipv4']['address']
                if ip_addr:
                    new_ip_port = ip_addr + ":4647"
                    result.append(new_ip_port)
            except:
                pass
    return result

def init_list(name):
    newlist = []
    newlist.append(name)
    return newlist

def convert_to_ip(name):
    ip_addr = hostvars['ansible_eth2']['ipv4']['address']
    if ip_addr:
        return ip_addr

class FilterModule(object):
    ''' utility filters for operating on hashes '''

    def filters(self):
        return {
            'hash_to_tuples' : hash_to_tuples
            ,'hash_keys'     : hash_keys
            ,'hash_values'   : hash_values
            ,'zipped_hash'   : zipped_hash
            ,'server_group_filter'  : server_group_filter
            ,'server_group_ip_map'  : server_group_ip_map
            ,'server_group_filter_v2'  : server_group_filter_v2
            ,'server_group_ip_map_v2'  : server_group_ip_map_v2
            ,'server_group_consul_map_v2' : server_group_consul_map_v2
            ,'server_group_ip_port_map_v2' : server_group_ip_port_map_v2
            ,'user_at_ip_map_v2' : user_at_ip_map_v2
            ,'etcd_inventory_list' : etcd_inventory_list
            ,'etcd_masters_list' : etcd_masters_list
            ,'etcd_cluster_list' : etcd_cluster_list
            ,'init_list'     : init_list
        }
