import json
import asyncio
import requests_async as requests

import base64

forEmployeeParams = {'state' : 'wait'}
getEmployeeStateUrl = 'https://wfnmvsj0rl.execute-api.ap-northeast-1.amazonaws.com/default/get/employee/state'

async def req():
  response = await requests.get(getEmployeeStateUrl, params= forEmployeeParams)
  waitEmployeeList = json.loads(response.content)
  return waitEmployeeList
  #print(json.dumps(waitEmployeeList, ensure_ascii=False, indent =3))


def main():
  employeelist = asyncio.run(req())
  print(employeelist[0]['id'])

main()