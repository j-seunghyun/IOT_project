from bluepy.btle import Scanner, DefaultDelegate
import os

class ScanDelegate(DefaultDelegate):
  def __init__(self):
    self.__scan_data__ = {}
    if(DefaultDelegate!= None):
      DefaultDelegate.__init__(self)

  def handleDiscovery(self, dev, isNewDev, isNewData):
    raw = dev.getScanData()
    mac = dev.addr.upper()
    rssi = dev.rssi

    data = {}
    data['raw'] = raw
    data['mac'] = mac
    data['rssi'] = rssi

    self.__scan_data__ = data

  def getScanData(self):
    return self.__scan_data__

def main():
  duration = 5
  scan_delegate = ScanDelegate()
  scanner = Scanner().withDelegate(scan_delegate)
  scanner.scan(duration)
  adv_data = scan_delegate.getScanData()
  print("Received Data : {}".format(adv_data))
  

if __name__=="__main__":
    main()