from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
import threading



# FUNCTIONS
# function to send Telegram msegs
def send_Tlg_msg(message):
	try:
		TOKEN = "####################"
		telegram_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
		params = {
			'chat_id': ###########,
			'text': message,
			'parse_mode': 'HTML',
		}
		response = requests.post(telegram_url, params=params)
	except:
		print_msg(" - Possible internet communication error - Could not send Telegram message.")						# Print error to console

# function to send 'alive' ping to uptime kuma
def parallel_im_alive():
	while True:
		try:
			response = requests.get("http://192.168.2.225:3005/api/push/xTeEHMosVI?status=up&msg=OK&ping=")
			response.close()
			print_msg(" - pinged uptime kuma")
		except requests.exceptions.RequestException as e:
			print_msg(f" - Error pinging Uptime Kuma: {e}")
		time.sleep(230)

# function to print to console
def print_msg(message):
	current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	print(current_time + message)



# Start the parallel function thread for sending 'alive' pings to uptime kuma
alive_thread = threading.Thread(target=parallel_im_alive)
alive_thread.start()
# alive_thread.join() # Wait for both threads to finish





# DECLARATIONS
# Web Link
link = "https://forums.redflagdeals.com/hot-deals-f9/trending/"

headers = {'Accept': 'text/html, application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'en-US,en;q=0.5',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

# Dictionary
dictionaryObject = {}
DictCount = 1

Errors_Web=0

# MAIN LOOP
FirstTimeRun = 0
while True:

	try:

		# Get refreshed copy of link - has to be inside Main Loop
		# Otherwise youre using the same page that you only pulled once.
		source = requests.get(link, headers=headers).text
		soup = BeautifulSoup(source, 'lxml')
		all_items = soup.find_all('li', class_='topic')
		# print(all_items)	# FOR TESTING

		# Web scrape thru each item on the page
		for li in all_items:
		    
			# Trending_score = li.find('dd', class_='total_count total_count_selector').text
			Trending_score = li.find('div', class_='votes thread_stat').text.strip()
			# print(Trending_score)		#FOR TESTING - keep this as a test, when viewing the console you will be able to see it is still reading off the site
			if int(Trending_score) < 50:	#only continue if trending score is 50 or more.  dont want small deals to flood my telegram
				continue		

			Title = li.find('h3', class_='thread_title').text
			Title = Title.replace('\n', '')
			# print(Title) 		#FOR TESTING - keep this as a test, when viewing the console you will be able to see it is still reading off the site
		    
			# Link = "https://forums.redflagdeals.com"+(li.find('a', class_='topic_title_link').get('href'))
			Link = li.find('a', class_='thread_title_link').get('href')
			# print(Link)		#FOR TESTING - keep this as a test, when viewing the console you will be able to see it is still reading off the site



			# Check if this is a new item. new item is match=0, not a new item is match=1
			match = 0
			for b in dictionaryObject:
				if dictionaryObject[b]['Title'] == Title and dictionaryObject[b]['Link'] == Link:
					match = 1
					break

			# If it is a new item:
			if match == 0:

				# If this is not the first time running the script, send Telegram Msg
				if FirstTimeRun != 0:
					send_Tlg_msg("Red Flag Deal!!\n\n"+Title+"\nTrending Score: "+Trending_score+"\n"+"https://forums.redflagdeals.com"+Link)

				# Add new item to Dictionary
				# So it can now be checked against each time it checks an item.
				AddEntry = {(DictCount): {'Title':(Title), 'Link':(Link)}}
				# print(AddEntry)		#FOR TESTING
				dictionaryObject.update(AddEntry)
				DictCount+=1

	except Exception as e: 
		# raise		# to view error and line of error
		print(e)
		Errors_Web+=1
		pass




	# Error Reporting
	if Errors_Web > 10:

		# Attempt to send error message thru Telegram.
		# If internet is down which is causing these errors it may not send through.
		try:
			send_Tlg_msg("SCRIPT ERROR \n\n RFD.py - Possible Error with Accessing Website \n\n Investigate Python Script")
		except:
			print_msg(" - RFD.py - Possible Error with Internet, could not send Telegram message")

		# print error to console
		print_msg(" - RFD.py - Possible Error with Accessing Website - Investigate Python Script")

		Errors_Web = 0	# Restart count




	# First time run function.  
	# So that you dont get a huge number of alerts on the first time you run the script.
	# Did it this way so that the number doesnt keep getting unnessarily bigger when adding, just need it to be either 0 or 1.
	if FirstTimeRun == 0:
		FirstTimeRun=1	




	# At 4:30 AM - 4:33 AM clear out the dictionary
	# This is so the dictionary doesnt get too big and bogs down the script.
	# I set it to be done at this time so that there is no real danger of new items getting added at this time.
	current_time = datetime.now().strftime("%H:%M")
	if current_time >= "04:30" and current_time <= "04:50":
		dictionaryObject.clear()
		FirstTimeRun=0




	# Printing 'Im Alive' log to console
	print_msg(" - RFD.py - Script Still Running.")



	# Sleep before looping thru pages again.  Again random
	current_time = datetime.now().strftime("%H:%M")
	if current_time > "01:00" and current_time < "06:30":
		time.sleep(3600)
	else:
		time.sleep(1800)