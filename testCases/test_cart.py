import pytest
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Test_login:
    baseURL = ReadConfig.getBaseURL()

    logger = LogGen.loggen()

    def test_FKKART0001(self, setup):
        self.logger.info("                                               ")
        self.logger.info("***** test_FKKART0001 execution started *****")
        self.logger.info("***** Verify HomePage Title *****")
        self.driver = setup
        self.driver.get(self.baseURL)

        actual_title = self.driver.title

        if actual_title == "Online Shopping Site for Mobiles, Electronics, Furniture, Grocery, Lifestyle, Books & More. Best Offers!":
            self.logger.info("***** Verify HomePage Title : Passed *****")
            assert True

        else:
            self.logger.error("***** Verify HomePage Title : Failed *****")
            assert False

        #Check for popup

        try:
            # Check if the popup element is present
            popup_element = self.driver.find_element(By.XPATH, "//div[contains(@class,'JFPqaw')]")

            # If element found, check if it's displayed
            if popup_element.is_displayed():
                # Close the popup
                close_button = self.driver.find_element(By.XPATH, "//span[contains(@class,'_30XB9F')]")
                close_button.click()
                self.logger.info("Popup found and closed.")
            else:
                self.logger.info("Popup found but not displayed.")

        except NoSuchElementException:
            # Handle case where the popup element is not found
            self.logger.info("Popup element not found. Continuing normal flow.")

        except Exception as e:
            # Handle any other exceptions that may occur
            self.logger.error(f"Exception occurred: {str(e)}")

            # If pop up does not present go with normal flow of search

        self.driver.find_element(By.XPATH, "//input[contains(@class,'Pke_EE')]").clear()
        self.driver.find_element(By.XPATH, "//input[contains(@class,'Pke_EE')]").send_keys("mobiles")
        self.driver.find_element(By.XPATH, "//input[contains(@class,'Pke_EE')]").send_keys(Keys.ENTER)

        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'BUOuZu')]")))

        result_count = self.driver.find_element(By.XPATH, "//span[contains(@class,'BUOuZu')]")

        if "1 – 24" in result_count.text:
            self.logger.info("***** Verify Search Results : Passed *****")
            self.driver.save_screenshot(".\\Screenshots\\" + f"{self.test_FKKART0001.__name__}_result_count_PASS.png")
            assert True
        else:
            self.logger.info("***** Verify Search Results : Failed *****")
            self.driver.save_screenshot(".\\Screenshots\\" + f"{self.test_FKKART0001.__name__}_result_count_FAIL.png")
            assert False

        # Add Elements to Compare and Compare Count

        search_result = self.driver.find_elements(By.XPATH, "//div[contains(@class,'DOjaWF gdgoEp')][2]//div[contains(@class,'_75nlfW')]//label[@class='tJjCVx']")

        if len(search_result) > 11:
            search_result[9].click()
            search_result[10].click()
            compare_text = self.driver.find_element(By.XPATH, "//a[contains(@class,'RCafFg')]//div//span[2]").text

            if compare_text == "2":
                self.logger.info("***** Added Search Products to Compare : Passed *****")
                assert True
            else:
                self.logger.info("***** Added Search Products to Compare : Failed *****")
                assert False
        else:
            self.logger.info("***** Added Search Products to Compare : Failed *****")
            assert False

        # Click on 10th Product and compare prices on price list and cart

        cart_targets = self.driver.find_elements(By.XPATH,
                                                 "//div[contains(@class,'DOjaWF gdgoEp')][2]//div[contains(@class,'_75nlfW')]")

        price_lists = self.driver.find_elements(By.XPATH,
                                                 "//div[contains(@class,'DOjaWF gdgoEp')][2]//div[contains(@class,'Nx9bqj _4b5DiR')]")

        price_on_list = price_lists[9].text

        cart_targets[9].click()

        self.driver.switch_to.window(self.driver.window_handles[1])

        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'In9uk2')]")))
        self.logger.info("***** Cart Page opened : Passed *****")

        price_on_cart = self.driver.find_element(By.XPATH, "//div[contains(@class,'Nx9bqj CxhGGd')]").text

        if price_on_list == price_on_cart:
            self.logger.info("***** Prices Matched : Passed *****")
            self.driver.save_screenshot(".\\Screenshots\\" + f"{self.test_FKKART0001.__name__}_price_match_PASS.png")
            assert True
        else:
            self.logger.info("***** Prices Matched : Failed *****")
            self.driver.save_screenshot(".\\Screenshots\\" + f"{self.test_FKKART0001.__name__}_price_match_FAIL.png")
            assert False

        # Add in cart and update with 1 for item
        #Used JS to avoid Overlay issue of click

        add_cart_elmnt = self.driver.find_element(By.XPATH, "//button[contains(@class,'In9uk2')]")
        self.driver.execute_script("arguments[0].scrollIntoView();", add_cart_elmnt)
        add_cart_elmnt.click()

        #Wait for Place Order Button to be present
        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(@class,'zA2EfJ _7Pd1Fp')]")))
        self.logger.info("***** Billing Page opened : Passed *****")

        # Click on Add item

        add_item = self.driver.find_element(By.XPATH, "//button[@class='LcLcvv' and not(@disabled)]")
        self.driver.execute_script("arguments[0].scrollIntoView();", add_item)
        add_item.click()

        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'eIDgeN') and contains(text(),'QUANTITY')]")))


        if self.driver.find_element(By.XPATH, "//div[contains(@class,'eIDgeN') and contains(text(),'QUANTITY')]").is_displayed():
            self.logger.info("***** Cart Updated : Passed *****")
            self.driver.save_screenshot(".\\Screenshots\\" + f"{self.test_FKKART0001.__name__}_pop_visible_PASS.png")
            assert True
        else:
            self.logger.info("***** Cart Updated : Failed *****")
            self.driver.save_screenshot(".\\Screenshots\\" + f"{self.test_FKKART0001.__name__}_pop_visible_FAIL.png")
            assert False


        remove_item = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Remove')]")
        self.driver.execute_script("arguments[0].scrollIntoView();", remove_item)
        remove_item.click()


        if self.driver.find_element(By.XPATH, "//div[contains(@class,'A0MXnh')]").is_displayed() and self.driver.find_element(By.XPATH, "//div[contains(@class,'t9UCZh')]").is_displayed():
            self.logger.info("***** Items Removed : Passed *****")
            self.driver.save_screenshot(".\\Screenshots\\" + f"{self.test_FKKART0001.__name__}_remove_pop_PASS.png")
            assert True

        else:
            self.logger.info("***** Items Removed: Failed *****")
            self.driver.save_screenshot(".\\Screenshots\\" + f"{self.test_FKKART0001.__name__}_remove_pop_FAIL.png")
            assert False

        # Click on Remove

        self.driver.find_element(By.XPATH, "//div[contains(@class,'A0MXnh')]").click()

        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'s2gOFd')]")))

        if self.driver.find_element(By.XPATH, "//div[contains(@class,'s2gOFd')]").is_displayed():
            assert True
            self.logger.info("***** Cart Emptied : Passed *****")
        else:
            assert False
            self.logger.info("***** Cart Emptied : Failed *****")

        self.driver.close()
        self.logger.info("***** Browser Closed *****")
        self.logger.info("***** test_FKKART0001 execution Completed *****")
