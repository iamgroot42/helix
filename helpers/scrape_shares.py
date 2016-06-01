from selenium import webdriver
import time

fp = webdriver.FirefoxProfile()
driver = webdriver.Firefox(firefox_profile=fp)

driver.get("https://www.facebook.com/login.php")

driver.find_element_by_id('email').send_keys('fragver4eva')
driver.find_element_by_id('pass').send_keys('Ss1415Fg16')
driver.find_element_by_id("loginbutton").click()

ide =  str(1404331996258923)
driver.get("https://www.facebook.com/shares/view?id="+ide)

lastHeight = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    newHeight = driver.execute_script("return document.body.scrollHeight")
    if newHeight == lastHeight:
        break
    lastHeight = newHeight

x = driver.find_element_by_id("view_shares_dialog_"+ide)

y = x.find_elements_by_class_name('userContentWrapper')

for z in y:
	p = z.find_element_by_class_name('clearfix').find_element_by_class_name('profileLink').get_attribute('data-hovercard')
	p = p.encode('utf-8')
	idee = p.split('/')[3].split('&')[0].split('=')[1]
