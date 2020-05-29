import os
import json


def add_full_info():
	file = 'sz-100.json'
	with open(file, 'r') as f:
		lines = json.load(f)
	
	lines = lines[:100]
	for line in lines:
		market = '深交所'
		line['fullInfo'] = '%s-%s(%s)' % (market, line['name'], line['code'])
		print(line)
	
	with open(file, 'w') as f:
		lines = json.dump(lines, f, indent=4)

def add_market():
	file = 'sh-100.json'
	with open(file, 'r') as f:
		lines = json.load(f)
	
	for line in lines:
		market = 'sh'
		line['market'] = market
		print(line)
	
	with open(file, 'w') as f:
		lines = json.dump(lines, f, indent=4)

add_market()