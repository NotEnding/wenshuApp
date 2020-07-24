from .cipher import Cipher
from .encrypt import Encrypt
import requests
import base64
import json
import time


BASE_URL = 'http://wenshuapp.court.gov.cn/appinterface/rest.q4w'


# get proxies
def query_proxies():
  proxies = None
  url = 'http://api.ip.data5u.com/dynamic/get.html'
  params = {
    'order': 'de15a979c3c4c0ab0de6e89f6a37924d',
    'random': 1,
    'json': 1
  }
  while not proxies:
    try:
      res = requests.get(url, params=params)
      if res.ok and res.json()['success']:
        proxies = res.json()['data']
      else:
        time.sleep(.2)
    except:
      time.sleep(.2)

  return proxies

# 获取一组案件的docId----构造请求参数
def gen_form_data(condition):
  query_condition = [
    {"key": "s8", "value": "02"}, #案件类型--刑事案件
    {"key": "cprqStart", "value": condition['start']},  #开始时间
    {"key": "cprqEnd", "value": condition['end']}  #结束时间
  ]
  if condition['court']:
    query_condition.append({"key": "s2", "value": condition['court']})  #法院名称
  params = {
    "pageNum": '1',
    "pageSize": '1000',
    "sortFields": "s50:desc",
    "ciphertext": Cipher.binary(), #加密的随机24-bit秘钥+时间戳+triple DES加密后的二 进制码
    "devid": "23a9c9828da443abbcfa8ab452201faa",
    "devtype": "1",
    "queryCondition": query_condition
  }
  q = {
    "id": Cipher.stamp,
    "command": 'queryDoc',
    "params": params,
    "cfg": "com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@docInfoSearch"
  }
  return {"request": base64.b64encode(json.dumps(q).encode()).decode()}

#根据提供的案件ID返回单个案件详细信息---构造请求参数
def gen_form_data_1(wenshu_id):
  params = {
    "ciphertext": Cipher.binary(),
    "devid": "23a9c9828da443abbcfa8ab452201faa",
    "devtype": "1",
    "docId": wenshu_id
  }
  q = {
    "id": Cipher.stamp,
    "command": 'docInfoSearch',
    "params": params,
    "cfg": "com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@docInfoSearch"
  }
  return {"request": base64.b64encode(json.dumps(q).encode()).decode()}

#获取一组案件的docId
def query_doc_list(page_num, page_size, query_condition, proxies=None):
  params = {
    "pageNum": str(page_num),
    "pageSize": str(page_size),
    "sortFields": "s50:desc",
    "ciphertext": Cipher.binary(),
    "devid": "23a9c9828da443abbcfa8ab452201faa",
    "devtype": "1",
    "queryCondition": query_condition
  }
  return _query_api('queryDoc', params, proxies=proxies)


#根据docId获取案件详情
def query_doc(doc_id, proxies=None):
  params = {
    "ciphertext": Cipher.binary(),
    "devid": "23a9c9828da443abbcfa8ab452201faa",
    "devtype": "1",
    "docId": doc_id
  }
  return _query_api('docInfoSearch', params, proxies=proxies)



# 根据不同的动作--调用对应的接口
def _query_api(action, params, proxies=None):
  q = {
    "id": Cipher.stamp,
    "command": action,
    "params": params,
    "cfg": "com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@docInfoSearch"
  }
  url = 'http://wenshuapp.court.gov.cn/appinterface/rest.q4w'
  data = "request={}".format(base64.b64encode(json.dumps(q).encode()).decode())
  headers = {
    "Content-Type": "application/x-www-form-urlencoded"
  }
  try:
    res = requests.post(url, data=data, headers=headers, proxies=proxies)
    result = json.loads(res.text)
    decrypt_result = json.loads(Encrypt.des_decrypt(result['data']['content'], result['data']['secretKey']).decode())
    return decrypt_result
  except:
    return None




if __name__ == '__main__':
  p = query_proxies()
  print(p)