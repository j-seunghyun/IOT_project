import binascii
import struct
import time
import json
import asyncio
import requests_async as requests
import base64

postHostUrl = "https://0kyzkkrvkg.execute-api.ap-northeast-1.amazonaws.com/default/post/distance"

async def post_distance(distance):
  #calc 함수에서 계산한 distance를 post
  response = await requests.post(postHostUrl, headers=None)
  data = json.loads(response.content)
  #response = await requests.post(postHostUrl, data=distance, headers=None)
  return data

def main():
  distance = 200
  response = asyncio.run(post(distance))
  print(json.dumps(response, ensure_ascii=False))
