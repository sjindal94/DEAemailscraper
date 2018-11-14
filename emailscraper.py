from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import sys
import linecache


#Webdriver settings here, using 20 seconds as expliccit wait time
#Setting up the driver and initializing malibox lists
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)
with open('data/Names3.txt') as f: 
    content = f.readlines() 
names = [x.strip() for x in content]
fileName = 'mailx17.txt' #next fileName to use, modify and use combine.py to combine all files for analysis
con = open('configUsed','a')



# starting from the last state, if exist, to automate the process
try:
    f = open('configUsed')
    lastConfig = f.readlines()[-1].split(' ')
    print(lastConfig)
    if(lastConfig[0] == 'END'): exit()
    url = lastConfig[0]
    email_threshhold = int(lastConfig[1])
    startMail = int(lastConfig[2])+1
    f.close()
except Exception as error:
    print(error)
    url = 'https://www.mailinator.com/'
    email_threshhold = -1 #-1 means fetch all the mails from a mailbox, otherwise fetch top X mailbox.
    startMail = 0




print('URL: '+ url)
print('Email Threshhold: ' + str(email_threshhold))
print('Starting Mailbox: ' + names[startMail])
emails = {} #all mails in all mailboxes collected so far
tcount=0 #total count of all the mails fetched in this run
tryingEmail = 0 #mailbox number according to names list


try:
    f = open('data/'+fileName,'a')
    for mIndex,tryName in enumerate(names[startMail:]):

        tryingEmail = mIndex + startMail
        driver.get(url)

        #website entered

        inputElement = driver.find_element_by_class_name('form-control')
        inputElement.clear()
        inputElement.send_keys(tryName)
        tempElement = driver.find_element_by_class_name('input-group-btn')
        buttonElement = tempElement.find_element_by_class_name('btn')
        buttonElement.click()

        #inside a mailbox



        tableElement = driver.find_element_by_class_name('table')
        rows = tableElement.find_elements(By.TAG_NAME, "tr") 
        emails[tryName] = []
        unable = False

        num_rows = len(rows) if (email_threshhold == -1) else min(len(rows),email_threshhold)
        for index,row in enumerate(rows[1:num_rows + 1]):
            tcount+=1            
            print('\nTotal MailBoxes Checked:'+str(len(emails)))
            print('Current MailBox:'+ tryName+ '('+str(tryingEmail)+')')
            print('Current Email count:'+ str(index+1))
            print('Total Emails fetched:'+ str(tcount))
            prev_url = driver.current_url
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "pointer")))# wait until row element is visible
            row.click()#click row to see the mail

            #inside an email

            time.sleep(2)#wait till the iframe is loaded with the mail
            count = 0
            unable=False

            # due to limit usage row.click() might not work for some time, so try again till it works
            while (prev_url== driver.current_url):
                count+=1
                print("Mailbox Retry:"+str(count))
                wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "pointer"))) # wait until row element is visible
                row.click()
                time.sleep(2)
                if count==5: #stop retries after 5 tries
                    unable=True
                    break
            

            if(unable):# go back to mailbox homepage if unable to open a mail of a mailbox
                print('failed')
                driver.switch_to.default_content()
                driver.back()
                break
            

            #grab the mail headers, fill the details
            header = driver.find_element_by_class_name('x_title').find_elements(By.CLASS_NAME,'ng-binding')
            data = {}
            soup = BeautifulSoup(header[0].get_attribute('innerHTML'), 'html.parser')
            temp = soup.find('small').text.split('[')
            data['senderName'] = temp[0].strip()
            data['senderEmail'] = temp[1].strip('[] ') 
            data['time'] = header[2].text
            print('SenderName:'+data['senderName'])
            print('SenderEmail:'+data['senderEmail'])
            

            #switch to iframe and grab the mail body
            driver.switch_to.frame(driver.find_element(By.ID, 'msg_body')) 
            time.sleep(2)
            driver.implicitly_wait(3)
            soup = BeautifulSoup(driver.page_source, 'html.parser') 
            x=soup.text
            data['msg_body'] = ''
            for line in x.split('\n'):
                if line.strip():
                    data['msg_body'] += (line+'\n')
            emails[tryName].append(data)




            #go back to original page holding the iframe and then navigate back to mailbox to fetch other mails
            driver.switch_to.default_content()
            prev_url = driver.current_url
            driver.back()
            time.sleep(2)
            unable=False
            count=0

            # due to limit usage row.click() might not work for some time, so try again till it works
            while (prev_url== driver.current_url):
                print(driver.current_url)
                count+=1
                print("Go Back Retry:"+str(count)+'\n')
                driver.back()
                time.sleep(2)
                if count==5:#stop retries after 5 tries
                    unable=True
                    break
            if(unable):# go back to mailbox homepage if unable to open a mail of a mailbox
                driver.back()




#if exception occurs which will occur if ip is blocked, dump the data in the file and store this configuration state in a file
except Exception as error:
    print(error)
    exc_type, exc_obj, tb = sys.exc_info()
    frame = tb.tb_frame
    lineno = tb.tb_lineno
    filename = frame.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, frame.f_globals)

    print ('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
    con.write('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

    print('\n'+url + ' '+ str(email_threshhold)+' '+ str(tryingEmail)+'\n')
    con.write('\n'+url + ' '+ str(email_threshhold)+' '+ str(tryingEmail)+'\n')
else:
    con = open('configUsed','a')
    con.write('END'+'\n')# END means all 100 mailboxes finished

#dump every mail in the file before quitiing
finally:
    con.close()
    f.write(json.dumps(emails,sort_keys=True, indent=4))
    f.close()