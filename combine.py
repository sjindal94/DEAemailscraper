#Combine all email files into one big json chunk

import json
combo = open('data/combo.txt','w')

with open('data/Names3.txt') as f: 
    content = f.readlines() 
names = [x.strip() for x in content]

allMails = {}
for name in names:
	allMails[name] = []

count=0
for i in range(1,7):
	with open('data/mails'+str(i)+'.txt','r') as f:
		data = json.load(f)
		for mailbox in data:
			for mail in data[mailbox]:
				allMails[mailbox].append(mail)
				count+=1

for i in range(1,18):
	with open('data/mailx'+str(i)+'.txt','r') as f:
		data = json.load(f)
		for mailbox in data:
			for mail in data[mailbox]:
				allMails[mailbox].append(mail)
				count+=1

combo.write(json.dumps(allMails,sort_keys=True, indent=4))
print(count)
