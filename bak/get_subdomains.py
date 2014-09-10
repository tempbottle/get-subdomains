# *-* coding: utf8 *-*
import sys
import time
import json
import hashlib
import requests
import torndb

#-------------------------------------------------------------------------
# get authenticity_token
def get_authenticity_token(url):
	s = requests.Session()
	r = s.get(url)
	

#-------------------------------------------------------------------------
# 获取子域名及网段信息
def get_sub_domain(domain, authenticity_token=""):
	url = "http://fofa.so/lab/ips"
	payload = dict(
		all = True,
		domain = domain,
		authenticity_token = authenticity_token
		)

	r = s.post(url, data=json.dumps(payload))
	print r.text


#-------------------------------------------------------------------------
# 获取公司所有域名信息
def get_all_domain():
	#key配置，需要与服务器端的统一
	payload = dict(
		sec_key = "dd65bdaf72657d5429b740811be1b551",
		is_cn = 0
		)
	url = "http://10.13.8.90/api/get_domain/"
	response = requests.get(url, params=payload)
	domains = json.loads(response.text).get('data', [])
	return domains


#-------------------------------------------------------------------------
# 主函数
if __name__ == '__main__':
	get_sub_domain("weibo.com", "QyMoWlya0hdf2hc08l30Mcgbx7Ghh6fHE2TSbUOAy28=")