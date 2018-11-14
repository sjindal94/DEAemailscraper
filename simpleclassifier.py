import json
from time import sleep
import re
from collections import Counter

f = open('data/combo.txt')
data = json.load(f) #conatins json of all emails

drugs = open('data/drugs.json','r')
content1 = json.load(drugs)
pharma = content1['drugs'] #contains data of all the available drugs

bad = open('data/bad.txt','r')
content2 = bad.read()
profane = content2.split('\n') #contains data of top Internet bad words  by Google

with open('data/domain.txt') as f: 
    content = f.readlines() 
domains = [x.strip() for x in content]

tmail = 0 #total mails in the collection
profaneMail = 0 #profaneMails in the collection
pharmaMail = 0 #pharmaMails in the collection
deauser = 0 #count of DEA User
deaUsed = [] #list of domain of the DEA user

for mailbox in data:
	for mail in data[mailbox]:
		tmail+=1
		text = mail['msg_body']
		words = re.findall(r'\w+', text)
		twords = len(words)

		sender = mail['senderEmail']
		for domain in domains:
			if domain in sender:
				deaUsed.append(domain)
				deauser+=1
				break

		if(twords==0):
			continue
		

		#find statistics of profane mails
		pwords = sum([text.count(word) for word in profane])
		pwordslist = [word for word in profane if text.count(word)>0]
		if pwords/twords>0.03:
			profaneMail+=1
			print('\ntotal:'+str(twords)+' profane :'+str(pwords) + ' ratio:'+ str(pwords/twords))
			print(pwordslist)

		#find statistics for pharma mails
		pharmawords = sum([text.count(word) for word in pharma])
		pharmawordList = [word for word in pharma if text.count(word)>0]
		if len(pharmawordList)>0:
			pharmaMail+=1
			print('\ntotal:'+str(twords)+' pharma :'+str(pharmawords) + ' ratio:'+ str(pharmawords/twords))
			print(pharmawordList)



		
#print output
print('\nTotal Mailboxes checked:' + str(len([x for x in data])))
print('Total Mailboxes checked with atleast 1 mail:' + str(len([x for x in data if len(data[x])!=0])))
print('\nTotal Mails:' +str(tmail))
print('Profane Mails:' +str(profaneMail))
print('Pharma Mails:' +str(pharmaMail))
print('\nProfanityRatio:'+str(profaneMail/tmail))
print('PharmaRatio:'+str(pharmaMail/tmail))
print('DEA User count:'+str(deauser))
print('DEA Used:'+str(Counter(deaUsed)))
f.close()
bad.close()