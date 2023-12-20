from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import logging
import sys
import time
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)01d %(levelname)s : %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        console_handler
    ]
)


class Winmasters():

    def start_chrome(self,headless):
        self.options = Options()
        if headless == 'y':
            self.options.add_argument('---headless')
        #self.options.add_extension('extension_2_4_1_0.crx')
        logging.info("Starting Chrome")
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.maximize_window()
        #time.sleep(40)
    def get_website(self):
        logging.info("Getting winmasters.gr")
        self.driver.get("https://www.winmasters.gr/el/sports/i/")
    def login_winmasters(self,username,password):
        logging.info("signing in")
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[@class='Button ButtonLogin InstanceOperatorLoginLink']")))
        link_btn = self.driver.find_element(By.XPATH,"//button[@class='Button ButtonLogin InstanceOperatorLoginLink']")
        link_btn.click()
        WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.XPATH,"//input[@name='username']")))
        enter_username = self.driver.find_element(By.XPATH,"//input[@name='username']")
        enter_username.send_keys(username)
        enter_password = self.driver.find_element(By.XPATH,"//input[@name='password']")
        enter_password.send_keys(password)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//button[@id="LoginButton-Header"]')))
        login_btn = self.driver.find_element(By.XPATH,'//button[@id="LoginButton-Header"]')
        login_btn.click()
        WebDriverWait(self.driver,10).until(EC.invisibility_of_element_located((By.XPATH,"//button[@class='Button ButtonLogin InstanceOperatorLoginLink']")))
        logging.info("Sign in Successful")
    def navigate_to_live_betting(self):
        logging.info("Navigating to live sports")
        self.driver.get("https://www.winmasters.gr/el/live-sports/i/live-sports/")
        time.sleep(1)
    def click_footbal_matches(self):
        self.driver.switch_to.frame('SportsIframe')
        try:
            WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"//span[@class='OM-Icon OM-Icon--1 OM-Icon--Svg OM-Icon--discipline OM-Icon--Medium1']")))
            logging.info("Clicking football matches")
            football = self.driver.find_element(By.XPATH,"//span[@class='OM-Icon OM-Icon--1 OM-Icon--Svg OM-Icon--discipline OM-Icon--Medium1']")
            football.click()
        except:
            return False
        WebDriverWait(self.driver,60).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='EventItem']")))
        event = self.driver.find_element(By.XPATH,"//div[@class='EventItem']")
        event.click()
        logging.info("Waiting for Matches")
        WebDriverWait(self.driver,60).until(EC.presence_of_element_located((By.XPATH,"//div[@class='MatchListGroup MatchList__Group']")))
        logging.info("Matches found!")
        return True
    def match_time(self):
        logging.info("Waiting for match time to load")
        WebDriverWait(self.driver,60).until(EC.presence_of_element_located((By.XPATH,"//span[@class='MatchTime__InfoData']")))
        logging.info("Scraping match time")
        match_time = self.driver.find_elements(By.XPATH,"//span[@class='MatchTime__InfoData']")
        return match_time
    def team_score(self,index):
        WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,"(//div[@class='Score Score--1']/span/span[@class='Score__Part Score__Part--Home'])")))
        team1_score = self.driver.find_element(By.XPATH,f"(//div[@class='Score Score--1']/span/span[@class='Score__Part Score__Part--Home'])[{index}]")
        team2_score = self.driver.find_element(By.XPATH,f"(//div[@class='Score Score--1']/span/span[@class='Score__Part Score__Part--Away'])[{index}]")
        if team1_score.text == '0' and team2_score.text == '0':

            return True
        else:
            return False

    def get_markets(self):
        logging.info("Waiting for market")
        WebDriverWait(self.driver,60).until(EC.presence_of_element_located((By.XPATH,"(//a[@class='Anchor OM-NavItem'])[1]")))
        main_market = self.driver.find_element(By.XPATH,"(//a[@class='Anchor OM-NavItem'])[1]")
        logging.info("clicking market")
        main_market.click()
        logging.info("Waiting for favourite market")
        try:
            WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.XPATH,"//div[@class='Market__Legend']/button[@class='FavoriteMarketsButton FavoriteMarketsButton--isFavorite']")))
            time.sleep(1)
            check_favourite_markets = self.driver.find_elements(By.XPATH,"//div[@class='Market__Legend']/button[@class='FavoriteMarketsButton FavoriteMarketsButton--isFavorite']")
            if len(check_favourite_markets) == 2:
                logging.info("both favourite markets found")
                return True
            else:
                logging.info("both favourite markets not found")
                self.add_favourite()
                return False
        except:
            self.add_favourite()
            return False
    def get_first_to_score_odds(self):
        odds = []
        logging.info("Scraping first to score team odds")
        first_team = self.driver.find_element(By.XPATH,"(//ul[@class='Market__OddsGroups Market__OddsGroups--layout-column'])[1]/li/ul/li[1]/button/div/span[3]")
        odds.append(first_team.text)
        second_team = self.driver.find_element(By.XPATH,"(//ul[@class='Market__OddsGroups Market__OddsGroups--layout-column'])[1]/li/ul/li[3]/button/div/span[3]")
        odds.append(second_team.text)
        return odds

    def click_first_to_score_odds(self,index_):
        logging.info("Clicking odds")
        if index_ == 0:
            first_team = self.driver.find_element(By.XPATH,"(//ul[@class='Market__OddsGroups Market__OddsGroups--layout-column'])[1]/li/ul/li[1]/button")
            try:
                first_team.click()
            except:
                return False
        if index_ == 1:
            second_team = self.driver.find_element(By.XPATH,"(//ul[@class='Market__OddsGroups Market__OddsGroups--layout-column'])[1]/li/ul/li[3]/button")
            try:
                second_team.click()
                return True
            except:
                return False


    def click_corners_odds(self,index_):
        logging.info("Clicking Corner market teams")
        if index_ == 0:
            first_team = self.driver.find_element(By.XPATH,"(//*[contains(@title, 'Σε 9:')])[3]")
            first_team.click()
        if index_ == 1:
            second_team = self.driver.find_element(By.XPATH,"(//*[contains(@title, 'Σε 9:')])[1]")
            second_team.click()

    def place_bet(self,bet_amount):
        bet_input = self.driver.find_element(By.XPATH,"//input[@step='any']")
        logging.info("placing bet")
        bet_input.send_keys(bet_amount)
        WebDriverWait(self.driver,30).until(EC.presence_of_element_located((By.XPATH,"//button[@class='OM-Button OM-Button--primary OM-Button--md BetslipFooter__PlaceBetButton']")))
        WebDriverWait(self.driver,30).until(EC.element_to_be_clickable((By.XPATH,"//button[@class='OM-Button OM-Button--primary OM-Button--md BetslipFooter__PlaceBetButton']")))
        place_bet = self.driver.find_element(By.XPATH,"//button[@class='OM-Button OM-Button--primary OM-Button--md BetslipFooter__PlaceBetButton']")
        place_bet.click()
    def wait_for_bet_success(self,timeout):
        WebDriverWait(self.driver,timeout).until(EC.presence_of_element_located((By.XPATH,"//span[@class='BetslipBet__BetSuccesMessage']")))
        logging.info("Success!")

    def add_favourite(self):
        try:
            add_fav = self.driver.find_element(By.XPATH,"//div[@class='EventItem EventItem--active']/div/div/button[@class='FavoriteButton FavoriteButton--isFavorite']")
            logging.info("Adding favourite")
            add_fav.click()
        except:
            add_fav = self.driver.find_element(By.XPATH,"//div[@class='EventItem EventItem--active']/div/div/button[@class='FavoriteButton']")
            logging.info("Adding favourite")
            add_fav.click()
    def check_favourite_dropdown(self):
        try:
            WebDriverWait(self.driver,1).until(EC.presence_of_element_located((By.XPATH,"//div[@class='MatchList MatchList--Sport-1 MatchList--Outcomes-1 MatchList--LiveEvents MatchList--hasFavorites LiveEventSidebar__MatchList']")))
            fav_dropdown_elements = self.driver.find_element(By.XPATH,"//div[@class='MatchList MatchList--Sport-1 MatchList--Outcomes-1 MatchList--LiveEvents MatchList--hasFavorites LiveEventSidebar__MatchList']")
            fav_dropdown = self.driver.find_element(By.XPATH,"//div[@class='MatchListMixed__Header']")
            fav_dropdown.click()
            logging.info("Hiding Favourite Dropdown")
        except:
            pass
    def favourite_match(self):
        time.sleep(0.5)
        self.driver.find_element(By.XPATH,"//div[@class='EventItem EventItem--active']/div/div/button[@class='FavoriteButton FavoriteButton--isFavorite']")
        logging.info("ignoring match")

    def check_login(self):
        self.driver.switch_to.default_content()
        time.sleep(0.2)
        logging.info("Checking Login Status")
        WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.XPATH,"//span[@class='Currency']")))

    def show_more_games(self):
            logging.info("Clicking show more")
            show_more = self.driver.find_element(By.XPATH,"//button[@class='OM-Button OM-Button--ghost OM-Button--md MatchList__MainButton']")
            webdriver.ActionChains(self.driver).move_to_element(show_more).perform()
            show_more.click()
    def wait_for_button(self):
        WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.XPATH,"//button[@class='OM-Button OM-Button--ghost OM-Button--md MatchList__MainButton']")))

    def total_odds(self):
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH,"//div[@class='BetslipFooter__TotalOddsValue']")))
        total_odds = self.driver.find_element(By.XPATH,"//div[@class='BetslipFooter__TotalOddsValue']").text
        while '.' not in total_odds:
            total_odds = self.driver.find_element(By.XPATH, "//div[@class='BetslipFooter__TotalOddsValue']").text
        time.sleep(1)
        total_odds_value = self.driver.find_element(By.XPATH, "//div[@class='BetslipFooter__TotalOddsValue']").text
        return float(total_odds_value)

    def quit(self):
        self.driver.quit()
    def clear_bet(self):
        WebDriverWait(self.driver,1).until(EC.presence_of_element_located((By.XPATH,"//button[@class='OM-Button OM-Button--primary OM-Button--md BetslipGroupActionBar__ClearSelections']")))
        clear_bet = self.driver.find_element(By.XPATH,"//button[@class='OM-Button OM-Button--primary OM-Button--md BetslipGroupActionBar__ClearSelections']")
        clear_bet.click()
        #WebDriverWait(self.driver,10).until(EC.invisibility_of_element_located((By.XPATH,"//button[@class='OM-Button OM-Button--primary OM-Button--md BetslipGroupActionBar__ClearSelections']")))

    def move_to_element(self,element):
        webdriver.ActionChains(self.driver).move_to_element(element).perform()
    def wait_for_element(self):
        WebDriverWait(self.driver,30).until(EC.presence_of_all_elements_located((By.XPATH,"//span[@class='MatchTime__InfoData']")))
    def find_total_matches(self):
        logging.info("Finding total matches")
        try:
            for m in self.match_time():
                time.sleep(0.3)
                self.wait_for_element()
                self.move_to_element(element=m)
        except:
            self.show_more_games()
        #self.show_more_games()
