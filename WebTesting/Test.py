import unittest
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(executable_path="F:\WebDrivers\chromedriver.exe")

    # #Test: Verify results match the search criterias
    def test_verify_results(self):
        # Check site open with success and title is correct
        driver = self.driver
        request = requests.get("https://www.bayut.com/")
        if request.status_code == 200:
            driver.get("https://www.bayut.com/")
            driver.maximize_window()
            #Add Dubai Marina as input
            try:
                elem = driver.find_element_by_xpath("/html/body/div[1]/header/div[4]/div/div[2]/div/div[1]/div[2]/div/div/ul/input")
                elem.send_keys("Dubai Marina")
                elem.send_keys(Keys.RETURN)
            except NoSuchElementException:
                self.fail("Cannot input path")

            #Search with the input
            try:
                searchButton = driver.find_element_by_xpath("/html/body/div[1]/header/div[4]/div/div[2]/div/div[2]/a")
                searchButton.click()
            except NoSuchElementException:
                self.fail("Cannot search the input, button missing")

            #Iterate through items from list
            try:
                invalidResultFound = False
                items = driver.find_elements_by_tag_name("li")
                for item in items:
                    info = item.find_elements_by_class_name("_7afabd84")
                    for data in info:
                        text = data.text
                        #In case we don't find Dubai Marina and we find it with a different name fail testcase
                        if(text.find(", Dubai Marina") == -1) and (text.find(", Dubai Marina,") == -1) and (text.find("Dubai Marina,") == -1) and (text.find("Dubai Marina") == -1 and len(text) == len("Dubai Marina")):
                            invalidResultFound = True
                            break
                self.assertEqual(invalidResultFound,False)
            except NoSuchElementException:
                self.fail("Cannot find list")

    #Test: Verify Popular Searches links work correctly
    def test_search_links(self):
        driver = self.driver
        request = requests.get("https://www.bayut.com/")

        if request.status_code == 200:
            driver.get("https://www.bayut.com/")
            driver.maximize_window()
            driver.implicitly_wait(2)
            try:
                toRentButton = driver.find_element_by_xpath("/html/body/div[1]/main/div[6]/div/div[2]/div[2]/div/div/div[2]")
                driver.execute_script("arguments[0].scrollIntoView();", toRentButton)
                toRentButton.click()

            except NoSuchElementException:
                self.fail("Cannot find To Rent button")

            try:
                listOfLinks = driver.find_elements_by_css_selector(".fc910dcd > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > ul:nth-child(2)")
            except NoSuchElementException:
                self.fail("Cannot find list of Dubai Apartaments to access")
            allLinksValid = True
            for location in listOfLinks:
                try:
                    info = location.find_elements_by_class_name("_78d325fa")
                    for infoData in info:
                        link = infoData.get_attribute("href")
                        request = requests.get(link)
                        if request.status_code != 200:
                            allLinksValid = False
                            print(link + " invalid link")
                except NoSuchElementException:
                    self.fail("Cannot reach links from list")
            self.assertEqual(allLinksValid, True)
        else:
            self.fail("https://www.bayut.com/ unreachable!")
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()