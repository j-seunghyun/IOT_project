from bluepy.btle import Scanner, DefaultDelegate


class ScanDelegate(DefaultDelegate):
  def __init__(self):
    DefaultDelegate.__init__(self)

  def handleDiscovery(self, dev, isNewDev, isNewData):
    if isNewDev:
      print ("discovered device", dev.addr)
    elif isNewData:
      print ("Received new data from", dev.addr)

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)

dev_addr_list = []
dev_rssi_list = []
for dev in devices:
  dev_addr_list.append(dev.addr)
  dev_rssi_list.append(dev.rssi)

print(dev_addr_list)
print(dev_rssi_list)