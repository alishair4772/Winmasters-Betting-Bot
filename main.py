import time
from winmasters_functions import *



username = input("Enter username: ")
password = input("Enter password: ")
bet_amount = input("Enter bet amount: ")
minimum_odds = input("Enter minimum odds: ")
timeout = int(input("Enter wait time for bet success: "))
head_less = input("headless mod? y/n: ")

bot = Winmasters()
bot.start_chrome(headless=head_less)
not_login = False
while True:
    bot.get_website()
    try:
        bot.login_winmasters(username=username,password=password)
    except:
        pass
    while True:
        try:
            bot.navigate_to_live_betting()
            try:
                bot.check_login()
                logging.info("User is Logged in")
            except:
                break
            if bot.click_footbal_matches() is False:
                logging.info("Football Matches not Available")
            else:
                bot.check_favourite_dropdown()
                time.sleep(1)
                while True:
                    try:
                        bot.show_more_games()
                        bot.wait_for_button()
                    except:
                        break
                matches = bot.match_time()
                for m_time in matches:
                    time.sleep(0.3)
                    bot.wait_for_element()
                    bot.move_to_element(element=m_time)
                    if int(m_time.text.replace("'",'')) < 20:
                        ind = matches.index(m_time)
                        if bot.team_score(index=ind+1) is True:
                            m_time.click()
                            logging.info("Clicking match")
                            try:
                                bot.favourite_match()
                                continue
                            except:
                                pass
                            if bot.get_markets() is True:
                                try:
                                    bot.clear_bet()
                                except:
                                    pass
                                logging.info("Getting odds")
                                try:
                                    first_to_score_odds = bot.get_first_to_score_odds()
                                except:
                                    continue
                                outsider = max(first_to_score_odds)
                                ind_ex = first_to_score_odds.index(outsider)
                                try:
                                    bot.click_first_to_score_odds(index_=ind_ex)
                                    bot.click_corners_odds(index_=ind_ex)
                                except:
                                    continue
                                total_odds = bot.total_odds()
                                if total_odds >= float(minimum_odds):
                                    logging.info("Placing bet")
                                    bot.place_bet(bet_amount=bet_amount)
                                    try:
                                        bot.wait_for_bet_success(timeout=timeout)
                                    except:
                                        continue
                                    logging.info("Success!")
                                    bot.add_favourite()
                                    bot.check_favourite_dropdown()
                                else:
                                    bot.clear_bet()
        except:
            pass

