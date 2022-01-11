import requests
import json
import math



def get_data(target):

  url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?id="

  headers = {
  'X-CMC_PRO_API_KEY': 'a9588b20-50b9-49d7-8a00-54caef62beb9',
  'Accepts': 'application/json'
  }

  target_url = url + target

  req = requests.get(url=target_url, headers=headers)
  if req.status_code == 200:
    data = json.loads(req.text)
    return data['data'][target]['quote']['USD']['market_cap']
  else:
    print("请求码为{}, 获取数据失败".format(req.status_code))
    return 0.0


luna = "4172"
ust ="7129"

luna_cap = get_data(target=luna)
ust_cap = get_data(target=ust)
rate =  luna_cap/ust_cap

luna_cap_str = str('{:,}'.format(math.floor(luna_cap)))
ust_cap_str = str('{:,}'.format(math.floor(ust_cap)))
rate_str = str('{:.4f}'.format(rate))


payload = {
    "value1": luna_cap_str,
    "value2": ust_cap_str,
    "value3": rate_str
}

ifttt_url = 'https://maker.ifttt.com/trigger/luna_ust/with/key/bVGEDkrCumRST4bL2kYcoC'

# 推送ifttt
requests.post(ifttt_url, params=payload)
# requests.post(webhook_url_2, json=payload)




