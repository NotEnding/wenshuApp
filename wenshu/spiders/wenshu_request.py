import json
import pandas as pd


class RequestGenerator:

  def __init__(self, court_file='court.json'):
    with open(court_file, encoding='utf8') as fp:
      # self.courts = json.load(fp)
      self.courts = [x for x in json.load(fp) if x['province'] == '江苏']
    self.current_index = 0

    self.conditions = []
    for year in range(1996, 2007):
      self.conditions.append(
        {
          'court': '',
          'start': '{}-01-01'.format(year),
          'end': '{}-12-31'.format(year)
        }
      )

    for year in ('2007', '2008', '2009'):
      for month in range(1, 13):
        self.conditions.append(
          {
            'court': '',
            'start': '{0}-{1:02d}-01'.format(year, month),
            'end': '{0}-{1:02d}-31'.format(year, month)
          }
        )

    for court in self.courts:
      for year in range(2010, 2021):
        for month in range(1, 13):
          self.conditions.append(
            {
              'court': court['court'],
              'start': '{0}-{1:02d}-01'.format(year, month),
              'end': '{0}-{1:02d}-31'.format(year, month)
            }
          )



  def __iter__(self):
    return self


  def __next__(self):
    if self.current_index < len(self.conditions):
      self.current_index += 1
      return self.conditions[self.current_index - 1]
    else:
      raise StopIteration()
# #

# 将数据库中的数据导出作为一张表，读取表中的docId，获取详情
# class RequestGenerator:
#
#   def __init__(self):
#     self.w_ids = pd.read_excel('E:\wenshu\wenshu_cases_hubei.xlsx')['wenshu_id']
#     self.current_index = 0
#
#
#
#
#   def __iter__(self):
#     return self
#
#
#   def __next__(self):
#     if self.current_index < len(self.w_ids):
#       self.current_index += 1
#       return self.w_ids[self.current_index - 1]
#     else:
#       raise StopIteration()


if __name__ == '__main__':
  cond_gen = RequestGenerator()
  for condition in cond_gen:
    print(condition)
