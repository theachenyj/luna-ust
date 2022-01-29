import requests
import json
import math
import csv

# 存储上一次数据变量，计算环比
LAST_SUPPLY_UST = 0.0 # 上一次 UST 的供应量
LAST_SUPPLY_LUNA = 0.0 # 上一次 LUNA 的供应量
LAST_RATE = 0.0 #上一次安全市值比

luna = "4172"
ust ="7129"


# 存上一次文件路径
csv_path = '/root/luna-ust/last_data.csv'
# csv_path = '/Users/theachen/Dropbox/PY/LAB/git/luna-ust/last_data.csv' #本地


def get_data(target,index):

  url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?id="

  headers = {
  'X-CMC_PRO_API_KEY': 'a9588b20-50b9-49d7-8a00-54caef62beb9',
  'Accepts': 'application/json'
  }

  target_url = url + target

  req = requests.get(url=target_url, headers=headers)
  if req.status_code == 200:
    data = json.loads(req.text)
    if index =='circulating_supply':
      return data['data'][target]['circulating_supply']
    elif index == 'price':
      return data['data'][target]['quote']['USD']['price']
    elif index == 'market_cap':
      return data['data'][target]['quote']['USD']['market_cap']
  else:
    print("请求码为{}, 获取数据失败".format(req.status_code))
    return 0.0


# 获取上一次数据
with open(csv_path) as f:
    for line in f:
        row = line.split(',')
        LAST_SUPPLY_UST = float(row[0])
        LAST_SUPPLY_LUNA = float(row[1])
        LAST_RATE = float(row[2])


# supply of UST，昨天供应量，环比变化，环比变化%
ust_spp = get_data(target=ust, index='circulating_supply')
diff_ust_spp_rate = (ust_spp - LAST_SUPPLY_UST) / LAST_SUPPLY_UST
diff_ust_spp_rate_dsp = '{:.4%}'.format(diff_ust_spp_rate)
ust_spp_dsp = '{:.4f}'.format(ust_spp/1000000000)
last_ust_spp_dsp = '{:.4f}'.format(LAST_SUPPLY_UST/1000000000)
messege_1 = f'昨日 {ust_spp_dsp}B，前日 {last_ust_spp_dsp}B，环比 ({diff_ust_spp_rate_dsp})'

# supply of Luna，昨天供应量，环比变化，环比变化%
luna_spp = get_data(target=luna, index='circulating_supply')
diff_luna_spp_rate = (luna_spp - LAST_SUPPLY_LUNA) / LAST_SUPPLY_LUNA
diff_luna_spp_rate_dsp = '{:.4%}'.format(diff_luna_spp_rate)
luna_spp_dsp = '{:.4f}'.format(luna_spp/1000000000)
last_luna_spp_dsp = '{:.4f}'.format(LAST_SUPPLY_LUNA/1000000000)
messege_2 = f'昨日 {luna_spp_dsp}B，前日 {last_luna_spp_dsp}B，环比({diff_luna_spp_rate_dsp})'

# 安全指标，昨天的值，前天的值
luna_cap = get_data(target=luna,index='market_cap')
ust_cap = get_data(target=ust,index='market_cap')
rate =  luna_cap/ust_cap
diff_rate = rate - LAST_RATE
rate_dsp = '{:.4f}'.format(rate)
diff_rate_dsp = '{:.4f}'.format(diff_rate)
messege_3 = f'昨日 {rate_dsp}({diff_rate_dsp})'


# 更新上一次数据
row = [ust_spp,luna_spp,rate]
# 以写模式打开文件
with open(csv_path, 'w', encoding='UTF8', newline='') as f:
    # 创建CSV写入器
    writer = csv.writer(f)

    # 向CSV文件写内容
    writer.writerow(row)

print(f'messege1: {messege_1}')
print(f'messege2: {messege_2}')
print(f'messege3: {messege_3}')

payload = {
    "value1": messege_1,
    "value2": messege_2,
    "value3": messege_3
}

ifttt_url = 'https://maker.ifttt.com/trigger/luna_ust/with/key/bVGEDkrCumRST4bL2kYcoC'

# 推送ifttt
requests.post(ifttt_url, params=payload)
