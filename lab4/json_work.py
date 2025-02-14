import json

with open("sample-data.json") as file:
    data = json.load(file)

print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20} {'Speed':<10} {'MTU':<5}")
print(f"{'-'*50} {'-'*20} {'-'*10} {'-'*5}")

a = 0
for item in data["imdata"]:
    a+=1
    interface = item["l1PhysIf"]["attributes"]
    print(f"{interface['dn']:<50} {interface.get('descr', ''):<20} {interface['speed']:<10} {interface['mtu']:<10}")
    if a ==4:
        break