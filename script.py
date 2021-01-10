from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from urllib.parse import quote
from keyboard import press

options = Options()
options.add_argument("--disable-notifications") # to silence alerts/ notifs vagera to top pe aate hai...

f = open("message.txt", "r")
message = f.read()
f.close()
print('The following message will be sent:\n')
print(message)
message = quote(message)

numbers = []
f = open("numbers.txt", "r")
for line in f.read().splitlines():
	if line != "":
		numbers.append(line)
f.close()
print('\n' + str(len(numbers)) + ' numbers found in the file')

print('When browser opens, sign in to web whatsapp and press enter')
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options) 
driver.get('https://web.whatsapp.com')
input() # for waiting untill the user presses enter
sleep(5) 

def send_message(driver, number, message):
	if number == "": 
		return
	print('\n\n', number)
	try:
		driver.get('https://web.whatsapp.com/send?phone=+91' + str(number) + '&text=' + message)
		sleep(10) # wait for page to load
		
		send = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH , '//*[@id="main"]/footer/div[1]/div[3]')))
		send.click()

		print('success')
	except Exception as e: # the numbers which aren't on whatsapp are added to nums_to_sms.txt file
		with open('nums_to_sms.txt', 'a') as f:
			f.write(str(number) + '\n')
		print('failure')
		print(e)

def handle_alert(driver):
	try:
		# to click ok on alterts that may appear on the top of the page! 
		alert_obj = driver.switch_to.alert # move the control from the page to the alert
		alert_obj.accept() # Accept the Alert (ok vala option click krdo...)
	except: 
		# probaly alert hi ni aaya to acchi baat hai
		pass

for num in numbers:
	send_message(driver, num, message)
	handle_alert(driver)