import binascii
import struct
import time
import json
import asyncio
import requests_async as requests
import base64

getDistanceUrl = 'https://ljw7pe9yp1.execute-api.ap-northeast-1.amazonaws.com/default/get/distance'

async def req():
  response = await requests.get(getDistanceUrl,params=None)
  distance = json.loads(response.content)
  return distance

def main():
  distance = asyncio.run(req())
  print(distance)

main()