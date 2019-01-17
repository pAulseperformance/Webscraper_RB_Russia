# Robo paste
import robo_browser
import pickle
import config
import time

from selenium.webdriver.common.action_chains import ActionChains

paste_login_url = config.paste_login_url
paste_term_url = config.paste_term_url
username = config.username
password = config.password

def load_data():
    try:
        with open('websitedata.pickle', 'rb') as f:
            source_data = pickle.load(f)
            return source_data
    except:
        print("No data found. Starting Copy Process")
        if input("Press 1 to continue or q to quit") == 1:
            robo_browser.main()
            with open('websitedata.pickle', 'rb') as f:
                source_data = pickle.load(f)
                return source_data
        else:
            exit()



def translate(source_data, translation):
    paste_data = {}
    ## BUG: translates with "e" conjugation always
    for idx, data in source_data.items():
        paste_data[idx] = data
        for key, value in data.items():
            for source_word, replace_word in translation.items():
                paste_data[idx][key] = source_data[idx][key].replace(source_word, replace_word)
    return paste_data

def main():
    # # TODO: add exeption for terms already listed

    translation = {"Новосибирск": "Санкт-Петербург",
                 "Новосибирске": "Санкт-Петербурге",
                 "nvs": "spb"}
    # Load the data and Translate the words
    paste_data = translate(source_data=load_data(), translation=translation)


    # Start Chromedriver
    chrome_driver = robo_browser.start_chrome_driver()
    chrome_driver.implicitly_wait(30) # Set time to wait for elements


    # Login to webpage
    robo_browser.driver_login(driver=chrome_driver,
                 url=paste_login_url,
                 username=username,
                 password=password)

    # Navigate chrome driver to paste_term_url
    chrome_driver.get(paste_term_url)

    # Click Add Term
    chrome_driver.find_element_by_class_name('button--primary').click()

    for idx in range(len(paste_data)):
        # Paste Title
        chrome_driver.find_element_by_id('edit-name-0-value').send_keys(paste_data[idx]['Title'])

        # Managing javascript for description
        # Wait for javascript to load

        elem = chrome_driver.find_element_by_id('cke_1_contents')
        actions = ActionChains(chrome_driver)

        try:
            chrome_driver.find_element_by_id('cke_32').click()
        except:
            time.sleep(1)
            chrome_driver.find_element_by_link_text('Источник').click()

        actions.move_to_element(elem)
        actions.perform()
        actions.click_and_hold()
        actions.perform()
        actions.send_keys(paste_data[idx]['Form Text'].replace("\n","").replace("\t",""))
        actions.perform()

        # Url Alias
        chrome_driver.find_element_by_id('edit-path-0-alias').send_keys(paste_data[idx]['Url Alias'])

        # Click on Meta button to expand Meta fields
        chrome_driver.find_element_by_id('edit-field-meta-0').click()

        # Clear any default data
        chrome_driver.find_element_by_id("edit-field-meta-0-basic-title").clear()
        chrome_driver.find_element_by_id("edit-field-meta-0-basic-description").clear()

        # Upload Meta Title and Description
        chrome_driver.find_element_by_id("edit-field-meta-0-basic-title").send_keys(paste_data[idx]['Meta Title'])
        chrome_driver.find_element_by_id("edit-field-meta-0-basic-description").send_keys(paste_data[idx]['Meta Description'])

        # Submit the edits
        chrome_driver.find_element_by_id ("edit-submit").click()

        # Check to make sure edits were successful
        # try:
        #     chrome_driver.implicitly_wait(30)
        #     chrome_driver.find_element_by_name("Создан новый термин")
        # except:
        #     break

    # chrome_driver.quit()

main()
