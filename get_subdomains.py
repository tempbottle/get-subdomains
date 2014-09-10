# *-* coding: utf8 *-*
import sys
import time
import json
import hashlib
import requests
import torndb


#------------------------------------------------------------------------
# 登陆
def login(username, password):
	url = 'http://api.chaxun.la/login/login/'
	payload = {
	'username' 	: username,
	'password' 	: hashlib.md5(password).hexdigest(),
	'ajax'		: 1
	}

	s = requests.Session()
	r = s.get(url, params=payload)
	return r.text

#-------------------------------------------------------------------------
# 获取页码信息
def get_pages(domain, keywordsid):
	url = 'http://api.chaxun.la/toolsAPI/getDomain/'
	payload = {
	'k'				: domain,
	'action'		: 'moreson',
	'page'			: 1,
	'keywordsid'	: keywordsid
	}
	s = requests.Session()
	r = s.get(url, params=payload)
	print r.text, type(r.text)

	count = int(json.loads(r.text).get('count', 0))
	print count
	if count % 100:
		pages = count / 100 + 1
	else:
		pages = count / 100

	return pages

#-------------------------------------------------------------------------
# 获取子域名信息
def get_sub_domain(domain, keywordsid, pages):
	url = 'http://api.chaxun.la/toolsAPI/getDomain/'
	s = requests.Session()
	domains = []
	sub_domains = []

	for x in xrange(1, pages + 1):
		payload = dict(
			k 			= domain,
			action 		= 'moreson',
			page 		= x,
			keywordsid 	= keywordsid
			)
		r = s.get(url, params=payload)
		if r.text:
			data = json.loads(r.text).get('data', [])
			if data:
				domains.extend(data)

		time.sleep(1)

	for item in domains:
		sub_domains.append(item.get('domain'))

	return list(set(sub_domains))


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
	username = 'hartnett'
	password = 'password'

	all_sub_domains = {}
	all_domains = get_all_domain()

	ret = login(username, password)
	if ret:
		result = json.loads(ret)
		keywordsid = result.get('cookie', "")
	else:
		print "login failed"
		sys.exit()

	for item in all_domains:
		domain = item.get('domain')
		pages = get_pages(domain, keywordsid)
		print "start to get %s's sub_domain, have %s sub_domains" % (domain, pages)
		sub_domains = get_sub_domain(domain, keywordsid, pages)
		all_sub_domains[domain] = sub_domains

	print all_sub_domains
		
	