from proxmoxer import ProxmoxAPI
from dotenv.main import load_dotenv
import csv
import os
load_dotenv()

host = os.environ['HOST']
user = os.environ['USER']
passwd = os.environ['PASS']
print(host,user,passwd)
proxmox = ProxmoxAPI(
    host, user=user + '@pam', password=passwd, verify_ssl=False
)
# Get a list of all virtual machines in the Proxmox cluster
vms = proxmox.cluster.resources.get(type='vm')

#Hàm lấy tất cả VM running trong proxmox
def get_all_name_vm(vms):
    arr = []
    for vm in vms:
        if vm['status'] == 'running':
            a = "{0}".format(vm['name'])
            arr.append(a)
    return arr
#Hàm lấy tất cả VM và pool
def get_all_vm_name_pool(vms):
    arr = []
    for vm in vms:
        if vm['status'] == 'running':
            name = vm['name']
            pool = vm['pool']
            status = vm['status']
            arr.append([name, pool,status])
    return arr
# hàm ghi xuống file txt
def write_txt_file(arr,filename):
    with open(filename, 'w') as f:
        for line in arr:
            f.write(line)
            f.write('\n')
# hàm ghi xuống file txt
def write_csv_file(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)


#writetofile(get_all_name_vm(vms))
#writetofile(get_all_vm_name_pool(vms))
#write_csv_file(get_all_vm_name_pool(vms),'readme.csv')