from proxmoxer import ProxmoxAPI
from dotenv.main import load_dotenv
import csv
import os
load_dotenv()

host = os.environ['HOST']
users = os.environ['USERS']
passwd = os.environ['PASS']
proxmox = ProxmoxAPI(
    host, user= users + '@pam', password=passwd, verify_ssl=False
)
# Get a list of all virtual machines in the Proxmox cluster
vms = proxmox.cluster.resources.get(type='vm')
pools = proxmox.pools.get()
nodes = proxmox.nodes.get()

#Hàm lấy tất cả node name
def get_all_node_name(nodes):
    arr = []
    for node in nodes:
            arr.append(node['node'])
    return arr

#Hàm lấy tất cả vmid running in node
def get_all_vmid_running_in_node(nodes):
    arr = []
    for node in nodes:
        for vmid in proxmox.nodes(node['node']).qemu.get():
            if vmid['status'] == 'running':
                arr.append(vmid['vmid'])
    return arr

#Hàm lấy tất cả firewall 
def get_all_firewall(nodes):
    arr = []
    for node in nodes:
        for vmid in proxmox.nodes(node['node']).qemu.get():
            if vmid['status'] == 'running':
                config = proxmox.nodes(node['node']).qemu(vmid['vmid']).config.get()
                if 'net0' in config:
                    name = config['name']
                    net  = config['net0']
                    if 'firewall' not in net:
                        arr.append([name,net])
    return arr
#Hàm lấy tất cả vm running in node and storage
def get_all_vm_name_pool1():
    arr = []
    for vm in proxmox.cluster.resources.get(type='vm'):
        pool = vm.get('pool')
        if vm['status'] == 'running' and pool is not None:
            name = vm['name']
            pool = vm['pool']
            node = vm['node']
            arr.append([name, pool,node])
    return arr
def get_all_vm_storage(nodes,vm_name_pool):
    arr = []
    for node in nodes:
        for vmid in proxmox.nodes(node['node']).qemu.get():
            if vmid['status'] == 'running':
                config = proxmox.nodes(node['node']).qemu(vmid['vmid']).config.get()
                if 'net0' in config:
                    name = config['name']
                    scsi0 = config.get('scsi0')
                    scsi1 = config.get('scsi1')
                    scsi2 = config.get('scsi2')
                    scsi3 = config.get('scsi3')
                    scsi4 = config.get('scsi4')
                    for vm in vm_name_pool:
                        if vm[0] == name:
                            if scsi0 is not None or scsi1 is not None or scsi2 is not None or scsi3 is not None or scsi4 is not None:
                                arr.append([name,vm[1],vm[2], scsi0,scsi1,scsi2,scsi3,scsi4])
    return arr
vm_name_pool = get_all_vm_name_pool1()
#Hàm lấy tất cả pool in proxmox
def get_all_pools(pools):
    arr = []
    for poolid in pools:
            pool = poolid['poolid']
            arr.append(pool)
    return arr
# Hàm xóa tất cả pool rỗng trong proxmox
def delete_all_pool_null():
    arr = get_all_pools(pools)
    for poolid in arr:
        getpoolid = proxmox.pools(poolid).get()
        if getpoolid['members'] == []:
            delete_pools = proxmox.pools(poolid).delete()
            print(delete_pools)
#Hàm lấy tất cả VM running trong proxmox
def get_all_name_vm(vms):
    arr = []
    for vm in vms:
        if vm['status'] == 'running':
            name = vm['name']
            arr.append([name])
    return arr
#Hàm lấy tất cả VM và pool
def get_all_vm_name_pool(vms):
    arr = []
    pool = vm.get('pool')
        if vm['status'] == 'running' and pool is not None:
            name = vm['name']
            pool = vm['pool']
            arr.append([name, pool])
    return arr
#Hàm lấy tất cả VM,pool,maxcpu,maxmem in node for all cluster
def get_all_vm_name_cpu_mem(vms):
    arr = []
    for vm in vms:
        if vm['status'] == 'running':
            name = vm['name']
            maxcpu = vm['maxcpu']
            maxmem = vm['maxmem']
            node = vm['node']
            pool = vm['pool']
            arr.append([name,maxcpu,maxmem,pool,node])
    return arr
# hàm ghi xuống file csv
def write_csv_file(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)
#writetofile(get_all_name_vm(vms))
#writetofile(get_all_vm_name_pool(vms))
#write_csv_file(get_all_vm_name_cpu_mem(vms),'readme.csv')
#print(delete_all_pool_null())
