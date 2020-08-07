from scrapy import Spider
from scrapy.http import FormRequest
from .wenshu_request import RequestGenerator
from .utils import gen_form_data_1, BASE_URL, gen_form_data
import json
from .encrypt import Encrypt
import requests
import pymysql

# 获取文书ID
class WenshuSpider(Spider):
  name = 'wenshu'

  # handle_httpstatus_list = [403, 200]

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.cond_gen = RequestGenerator()
    self.connection = pymysql.connect(
      host='localhost',
      user='root',
      password='xxxxx',
      db='wenshu',
      cursorclass=pymysql.cursors.DictCursor
    )

  def start_requests(self):
    for condition in self.cond_gen:
      print(f"condition:{condition}")
      meta = None
      try:
        res = requests.get(
          '代理地址')
        if res.ok:
          meta = {"proxy": "http://{}:{}".format(res.json()['data'][0]['ip'], res.json()['data'][0]['port'])}
          print(meta)
      except:
        try:
          res = requests.get('http://127.0.0.1:5010/get/')
          if res.ok:
            meta = {"proxy": "http://{}".format(res.json()['proxy'])}
        except:
          pass
      yield FormRequest(
        url=BASE_URL,
        headers={
          "User-Agent": 'Mozilla/5.0 (Linux; U; Android 2.2) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'},
        formdata=gen_form_data(condition),
        meta=meta
      )

  # noinspection PyBroadException
  def parse(self, response):
    try:
      result = json.loads(response.text)
      if result['ret']['code'] == 1:
        decrypt_result = json.loads(
          Encrypt.des_decrypt(result['data']['content'], result['data']['secretKey']).decode())
        for record in decrypt_result['queryResult']['resultList']:
          self._save2database(record)
          yield record
    except:
      return

  def _save2database(self, record):
    try:
      with self.connection.cursor() as cursor:
        sql = "INSERT INTO `wenshu_cases_jiangsu` (`case_name`, `court_name`, `case_no`, `procedure`, `reason`, `date_`, `open_type`, `wenshu_id`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data = (
        record['1'], record['2'], record['7'], ', '.join([x for x in [record['9'], record['10']] if x]), record['26'],
        record['31'], record['43'], record['rowkey'])
        cursor.execute(sql, data)
      self.connection.commit()
    except:
      print('failed')





# 获取文书详情
# class WenshuSpider(Spider):
#   name = 'wenshu'
#
#   # handle_httpstatus_list = [403, 200]
#
#   def __init__(self, **kwargs):
#     super().__init__(**kwargs)
#     self.cond_gen = RequestGenerator()
#     self.connection = pymysql.connect(
#       host='localhost',
#       user='root',
#       password='xxxx',
#       db='wenshu',
#       cursorclass=pymysql.cursors.DictCursor
#     )
#
#   def start_requests(self):
#     for wenshu_id in self.cond_gen:
#       meta = None
#       try:
#         res = requests.get(
#           '代理地址')
#         if res.ok:
#           meta = {"proxy": "http://{}:{}".format(res.json()['data'][0]['ip'], res.json()['data'][0]['port'])}
#           print(meta)
#       except:
#         try:
#           res = requests.get('http://127.0.0.1:5010/get/')
#           if res.ok:
#             meta = {"proxy": "http://{}".format(res.json()['proxy'])}
#         except:
#           pass
#       yield FormRequest(
#         url=BASE_URL,
#         headers={
#           "User-Agent": 'Mozilla/5.0 (Linux; U; Android 2.2) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'},
#         formdata=gen_form_data_1(wenshu_id),
#         meta=meta,
#         cb_kwargs={'wenshu_id': wenshu_id}
#       )
#
#   # noinspection PyBroadException
#   def parse(self, response, **cb_kwargs):
#     try:
#       result = json.loads(response.text)
#       if result['ret']['code'] == 1:
#         decrypt_result = json.loads(
#           Encrypt.des_decrypt(result['data']['content'], result['data']['secretKey']).decode())
#         yield decrypt_result
#         self._save2database(cb_kwargs['wenshu_id'], decrypt_result)
#     except:
#       return
#
#   def _save2database(self, wenshu_id, record):
#     try:
#       with self.connection.cursor() as cursor:
#         sql = "UPDATE `wenshu_cases_hubei` SET `detail` = %s WHERE `wenshu_id` = %s"
#         data = (record['DocInfoVo']['qwContent'], wenshu_id)
#         cursor.execute(sql, data)
#       self.connection.commit()
#     except:
#       print('failed')
