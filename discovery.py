import ssdp3 as ssdp

st = 'urn:rc-freetime-tv:service:freetimerc:1'
print(st)
found = ssdp.discover(st, timeout=10, retries=10, mx=4)
print(found)

for item in found:
    print(item.usn)
    print(item.location)
