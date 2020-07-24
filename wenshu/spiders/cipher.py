from datetime import datetime
import random
from .encrypt import Encrypt


class Cipher:

  stamp = ''

  @classmethod
  def binary(cls):
    try:
      date = datetime.now()
      time_stamp = str(int(date.timestamp() * 1000))
      cls.stamp = time_stamp
      date_str = date.strftime('%Y%m%d')
      random24 = cls.random(24)
      origin = random24 + date_str + Encrypt.des_encrypt(time_stamp, random24, date_str).decode()

      return cls.binary_string(origin)
    except Exception as e:
      print(e)
      return ''



  @classmethod
  def random(cls, i):
    str_ = ''
    c_arr = [chr(x) for x in (*range(48, 58), *range(97, 123), *range(65, 91))]
    for i2 in range(i):
      str_ += c_arr[int(random.random() * len(c_arr))]
    return str_



  @classmethod
  def binary_string(cls, text):
    result = ''
    for i, c in enumerate(text):
      if i != 0:
        result += ' '
      result += format(ord(c), 'b')
    return result
