import requests
import config
import json
import time

addr = config.BEAM_ADDR

session = requests.Session()

get_msg = session.get(
	addr + '/api/v1/chats/' + str(config.CHANNEL_PARA) + '/message'
)

for msg in get_msg.json():
	#print (msg,"\n")
	for item in msg['message']:
		for i in iter(item.keys()):
			print (i)
			print (item[i])
		#print ('Item:',item)
		# curIter = 0
		# for i in iter(item.keys()):
		# 	print ('item:\t\t',item[i])
		# 	print ('i:\t\t',i)
		# 	print ('curIter:\t',curIter,"\n")
		# 	# if i == 'url':
		# 	# 	print (type(curIter),curIter)
		# 	if i == 'url' and curIter == 2:	# We're parsing a URL
		# 		print (item[i])
		# 	curIter += 1
# input()
# time.sleep(3)