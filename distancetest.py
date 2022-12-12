import binascii
import struct
import time
import json
import asyncio
import requests_async as requests
import base64

postHostUrl = "https://0kyzkkrvkg.execute-api.ap-northeast-1.amazonaws.com/default/post/distance"

async def post_distance(distance, current_index):
  #calc 함수에서 계산한 distance를 post
  datas = dict(index=current_index, distance = 200)
  response = await requests.post(postHostUrl,data=datas,headers=None)
  data = json.loads(response.content)
  return data

def main():
  distance = 200
  current_index = 0
  #response = asyncio.run(post_distance(distance))
  #print(json.dumps(response, ensure_ascii=False))

  while True:
    response = asyncio.run(post_distance(distance, current_index))
    current_index = current_index+1
    time.sleep(10)

main()