# WEB_SCRAPING_RFD_website

This is my script to web scrape the redflagdeals.com website for trending topics. When a new trending topics score goes above a threshold it is sent to a Telegram bot I have set up that is only used for web scraping alerts.<br><br>



Basic Structure of the script:<br>
LOOP<br>
- Scrapes link for:
  - title
  - link
  - trending score

- check if item is a new item.
    - if it is it stores it in a dictionary & sends it to telegram

- at 4:30am clear out the dictionary
    - so that dictionary doesnt get too large and bogs down the script
- dont send telegram message on first pass so that after clearing out the dictionary at 430am you dont get alot of new item messages
