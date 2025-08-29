ip=input("Enter ip address: ")
ip_list=ip.split(".")
x=int(ip_list[0])
y=int(ip_list[1])
z=int(ip_list[2])
w=int(ip_list[3])
size=8
x_bin=dec_bin(x,size)
for i in range (5):
  if x_bin[i]==0:
    break
class_ip = hex(10+i).replace('0x','').upper()
print(class_ip)
mask1=[0]*4
if i<3:
 for j in range (i+1):
  mask1[j]=255
 print("Net Mask=",mask1)
else:
  print("NA")
net_id=[0]*4
if i<3:
 for k in range (i+1):
  net_id[k]=int(ip_list[k])
 print("Net ID=",net_id)
mask2 = [255] * 4
if i < 3:
    for j in range(i + 1):
        mask2[j] = 0
    print("Host Mask =", mask2)


    host_id = [0] * 4
    for k in range(i + 1, 4):
        host_id[k] = int(ip_list[k])
    print("Host ID =", host_id)
