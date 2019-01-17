import robo_browser
import pickle
import config

from selenium.webdriver.common.action_chains import ActionChains

paste_login_url = config.paste_login_url
paste_term_url = config.paste_term_url
username = config.username
password = config.password

def load_data():
    with open('cars_submodels_dict.pickle', 'rb') as f:
        return pickle.load(f)

def translate(source_data, translation):
    paste_data = {}
    ## BUG: translates with "e" conjugation always
    for url, car_submodels_dict in cars_submodels_dict.items():
        paste_data[url] = car_submodels_dict
        for idx, car_submodel in car_submodels_dict.items():
            for key, value in car_submodel.items():
                for source_word, replace_word in translation.items():
                    paste_data[url][idx][key] = cars_submodels_dict[url][idx][key].replace(source_word, replace_word)

    return paste_data

def paste_car_submodel_data(submodel):
    #paste Title
    chrome_driver.find_element_by_id('edit-title-0-value').send_keys(submodel['Title'])
    # Paste Subtitle
    chrome_driver.find_element_by_id('edit-field-zagolovok-anonsa-0-value').send_keys(submodel['Subtitle'])

    # interact with javascript form
    elem = chrome_driver.find_element_by_id('cke_1_contents')
    actions = ActionChains(chrome_driver)
    chrome_driver.find_element_by_id('cke_32').click() # Click java button for html formatting label: A source
    actions.move_to_element(elem)
    actions.perform()
    actions.click_and_hold()
    actions.perform()
    actions.send_keys(submodel['Form Text'].replace("\n","").replace("\t",""))
    actions.perform()



    # Send blank keys to title to scroll back up for visible meta
    chrome_driver.find_element_by_id('edit-title-0-value').send_keys("")
    # Open the Meta Tab
    chrome_driver.find_element_by_xpath("//*[@id='edit-field-meta-0']/summary").click()

    # Clear default meta data
    chrome_driver.find_element_by_id("edit-field-meta-0-basic-title").clear()
    chrome_driver.find_element_by_id("edit-field-meta-0-basic-description").clear()
    # Paste Meta data
    chrome_driver.find_element_by_id("edit-field-meta-0-basic-title").send_keys(submodel['Meta Title'])
    chrome_driver.find_element_by_id("edit-field-meta-0-basic-description").send_keys(submodel['Meta Description'])

    # Open the Edit Domain Drop down Tab
    chrome_driver.find_element_by_xpath("//*[@id='edit-domain']/summary").click()
    # Uncheck the default box
    chrome_driver.find_element_by_xpath("//*[@id='edit-field-domain-access']/div[1]/label").click()
    # Click the checkboxs for st.petersburg
    chrome_driver.find_element_by_xpath("//*[@id='edit-field-domain-access-sankt-peterburg-spec-akpp-ru']").click()
    # Select the domain in the dropdown menu
    chrome_driver.find_element_by_xpath("//*[@id='edit-field-domain-source']/option[4]").click()

    # select option in drop down form
    el = chrome_driver.find_element_by_id('edit-field-sankt-peterburg')
    for option in el.find_elements_by_tag_name('option'):
        if option.text == submodel['Selected Option']:
            option.click()
            break


# Get source data
cars_submodels_dict = load_data()

# Translation dictionary
translation = {"Новосибирск": "Санкт-Петербург",
             "Новосибирске": "Санкт-Петербурге",
             "nvs": "spb"}

# Translate source data for new webpage
paste_data = translate(source_data=cars_submodels_dict, translation=translation)

# Start Chromedriver
chrome_driver = robo_browser.start_chrome_driver()
chrome_driver.implicitly_wait(10) # Set time to wait for elements

# Login to webpage
robo_browser.driver_login(driver=chrome_driver,
             url=paste_login_url,
             username=username,
             password=password)

for idx, submodels in enumerate(paste_data.values()):
    if not submodels: # Skips empty dictionarys
        continue
    else:
        for submodel in submodels.values():
            # Navigate chrome driver to add a submodel
            chrome_driver.get("https://www.spec-akpp.ru/node/add/remont_dvigatelei")
            # Paste contents
            paste_car_submodel_data(submodel)
            # submit Contents
            chrome_driver.find_element_by_xpath("//*[@id='edit-submit']").click()
