from datetime import datetime
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class Hosttest(TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000/'

    def tearDown(self):
        self.driver.quit()
        
    def test_01_login_page(self):
        driver = self.driver

        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(1)
        login=driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/login']")
        login.click()
        time.sleep(2)
        email=driver.find_element(By.CSS_SELECTOR,"input[type='email']#email")
        email.send_keys("raoofvenad123@gmail.com")
        password=driver.find_element(By.CSS_SELECTOR,"input[name='password']")
        password.send_keys("Asdf234@")
        time.sleep(2)
        submit=driver.find_element(By.CSS_SELECTOR,"button[type='submit']")
        submit.click()
        time.sleep(2)
        # veg=driver.find_element(By.CSS_SELECTOR,"a[href='/vegetables/20/']")
        # veg.click()
        # time.sleep(2)
        # add=driver.find_element(By.CSS_SELECTOR,"a#cart.btn-cart[href='/add_to_cart/13/']")
        # add.click()
        # time.sleep(2)
        # pay=driver.find_element(By.CSS_SELECTOR,"a.btn-checkout[href='/checkout_delivery/']")
        # pay.click()
        # time.sleep(2)
        # address=driver.find_element(By.CSS_SELECTOR,"input[type='radio'][name='selected_delivery']#delivery_15")
        # address.click()
        # time.sleep(2)
        # payment=driver.find_element(By.CSS_SELECTOR,"input.razorpay-payment-button[type='submit'][value='Pay with Razorpay']")
        # payment.click()
        # time.sleep(2)


    # def test_01_login_page(self):
    #     driver = self.driver
    #     driver.get(self.live_server_url)
    #     driver.maximize_window()
    #     time.sleep(1)
    #     login=driver.find_element(By.CSS_SELECTOR,"a[href='/login/']")
    #     login.click()
    #     time.sleep(2)
    #     email=driver.find_element(By.CSS_SELECTOR,"input[name='username']")
    #     email.send_keys("pranav")
    #     password=driver.find_element(By.CSS_SELECTOR,"input[name='password']")
    #     password.send_keys("Pranav@123")
    #     time.sleep(2)
    #     submit=driver.find_element(By.CSS_SELECTOR,"button[type='submit']#submit")
    #     submit.click()
    #     time.sleep(2)

    #     stock=driver.find_element(By.CSS_SELECTOR,"a[href='/sell_product_list/'] .button-box h2")
    #     stock.click()
    #     time.sleep(2)
    #     nav=driver.find_element(By.CSS_SELECTOR,".navbar-menu-button")
    #     nav.click()
    #     time.sleep(2)
    #     update=driver.find_element(By.CSS_SELECTOR,"a[href='/update_products/']")
    #     update.click()
    #     time.sleep(2)
    #     # more.click()
    #     # time.sleep(2)
    #     quantity=driver.find_element(By.CSS_SELECTOR,"a[href='/update_product_quantity/10/']")
    #     quantity.click()
    #     time.sleep(2)

    #     updated=driver.find_element(By.CSS_SELECTOR,"button[type='submit']")
    #     updated.click()
    #     time.sleep(2)






    # def test_01_login_page(self):
    #     driver = self.driver
    #     driver.get(self.live_server_url)
    #     driver.maximize_window()
    #     time.sleep(1)
    #     login=driver.find_element(By.CSS_SELECTOR,"a[href='/login/']")
    #     login.click()
    #     time.sleep(2)
    #     email=driver.find_element(By.CSS_SELECTOR,"input[name='username']")
    #     email.send_keys("deepa")
    #     password=driver.find_element(By.CSS_SELECTOR,"input[name='password']")
    #     password.send_keys("Deep@123")
    #     time.sleep(2)
    #     submit=driver.find_element(By.CSS_SELECTOR,"button[type='submit']#submit")
    #     submit.click()
    #     time.sleep(2)
    #     modalclose=driver.find_element(By.CSS_SELECTOR,"a[href='/view_wishlist/'] > i.fa.fa-heart")
    #     modalclose.click()
    #     time.sleep(2)






        # roomclose=driver.find_element(By.CSS_SELECTOR,"button.btn.btn-danger#close-chat-room")
        # roomclose.click()
        # time.sleep(2)
        # roomclose=driver.find_element(By.CSS_SELECTOR,"button.btn.btn-danger#close-chat-room")
        # roomclose.click()
        # time.sleep(2)
        # profile=driver.find_element(By.CSS_SELECTOR,"a.nav-link.text-success p")
        # profile.click()
        # time.sleep(2)
        # logout = driver.find_element(By.CSS_SELECTOR, "a.dropdown-item[href='/logout/']")
        # logout.click()
        # time.sleep(2)
        # login=driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/login/'] button.btn.btn-outline-success")
        # login.click()
        # time.sleep(2)
        # email=driver.find_element(By.CSS_SELECTOR,"input[type='email'][name='email']")
        # email.send_keys("ontario@gmail.com")
        # password=driver.find_element(By.CSS_SELECTOR,"input[type='password'][name='password']")
        # password.send_keys("Ontario@123")
        # time.sleep(2)
        # submit=driver.find_element(By.CSS_SELECTOR,"button.btn-login#submitBtn")
        # submit.click()
        # time.sleep(3)
        # addcourse=driver.find_element(By.CSS_SELECTOR,"button.btn.btn-primary#learnMoreButton")
        # addcourse.click()
        # time.sleep(2)
        # coursename=driver.find_element(By.CSS_SELECTOR,"input#course_name")
        # coursename.send_keys("MS in computer Application")
        # time.sleep(1)
        # coursemode=driver.find_element(By.CSS_SELECTOR,"select#course_mode")
        # coursemode.click()
        # coursemodeselect=driver.find_element(By.CSS_SELECTOR,"option[value='On-campus']")
        # coursemodeselect.click()
        # time.sleep(1)
        # coursetype=driver.find_element(By.CSS_SELECTOR,"select#course_type")
        # coursetype.click()
        # coursetypeselect=driver.find_element(By.CSS_SELECTOR,"option[value='Master Degree']")
        # coursetypeselect.click()
        # time.sleep(1)
        # coursetype=driver.find_element(By.CSS_SELECTOR,"select#academic_disciplines")
        # coursetype.click()
        # coursetypeselect=driver.find_element(By.CSS_SELECTOR,"option[value='Engineering and Applied Science']")
        # coursetypeselect.click()
        # time.sleep(1)
        # desc=driver.find_element(By.CSS_SELECTOR,"textarea#course_desc")
        # desc.send_keys("This is a test course desc")
        # time.sleep(1)
        # eligibility=driver.find_element(By.CSS_SELECTOR,"textarea#eligibility")
        # eligibility.send_keys("This is a test course eligibility")
        # time.sleep(1)
        # fees=driver.find_element(By.CSS_SELECTOR,"input#fees[type='number']")
        # fees.send_keys("210")
        # time.sleep(1)
        # coursedur=driver.find_element(By.CSS_SELECTOR,"select#duration")
        # coursedur.click()
        # time.sleep(1)
        # coursedurselect=driver.find_element(By.CSS_SELECTOR,"select#duration option[value='2 years']")
        # coursedurselect.click()
        # time.sleep(1)
        # input_date1= "2023-10-20"
        # formatted_date = datetime.strptime(input_date1, '%Y-%m-%d').strftime('%m-%d-%Y')
        # opendate_input = driver.find_element(By.CSS_SELECTOR, "input#opendate")
        # opendate_input.send_keys(formatted_date)
        # time.sleep(1)
        # input_date2= "2023-11-28"
        # formatted_date = datetime.strptime(input_date2, '%Y-%m-%d').strftime('%m-%d-%Y')
        # deaddate_input = driver.find_element(By.CSS_SELECTOR, "input#appdeadline")
        # deaddate_input.send_keys(formatted_date)
        # time.sleep(1)
        # seats_available_input = driver.find_element(By.CSS_SELECTOR, "input#seats_available")
        # seats_available_input.send_keys("20")
        # time.sleep(1)
        # file_path = 'C:\\Users\\Rony\\Downloads\\IT.jpeg'
        # thumbnail_image_input = driver.find_element(By.CSS_SELECTOR, "input#thumbnail_image[type='file']")
        # thumbnail_image_input.send_keys(file_path)
        # time.sleep(3)
        # submit_button = driver.find_element(By.CSS_SELECTOR, "input#submitBtn[type='submit']")
        # submit_button.click()
        # time.sleep(5)
        # print("Added course successfully")
        # manage = driver.find_element(By.CSS_SELECTOR, "a[href='/courselisting/'] button.btn.btn-primary.mt-3")
        # manage.click()
        # time.sleep(3)
        # # Scroll down
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(3)  # Optional sleep to let the page load

        # # Scroll up (negative scroll distance)
        # driver.execute_script("window.scrollTo(0, -document.body.scrollHeight);")
        # time.sleep(5)  # Optional sleep after scrolling up
        
        # home = driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/institute-dashboard/']")
        # home.click()

        
        
        
        
        
        
        
        
        
        


        

    # Add more test methods as needed

# if __name__ == '__main__':
#     import unittest
#     unittest.main()