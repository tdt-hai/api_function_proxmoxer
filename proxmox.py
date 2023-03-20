from proxmoxer import ProxmoxAPI
from dotenv.main import load_dotenv
import csv
import os
load_dotenv()

host = os.environ['HOST']
user = os.environ['USER']
passwd = os.environ['PASS']
proxmox = ProxmoxAPI(
    host, user=user + '@pam', password=passwd, verify_ssl=False
)
# Get a list of all virtual machines in the Proxmox cluster
vms = proxmox.cluster.resources.get(type='vm')
pools = proxmox.pools.get()

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
    for vm in vms:
        if vm['status'] == 'running':
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