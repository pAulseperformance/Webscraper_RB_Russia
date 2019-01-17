from robobrowser import RoboBrowser
import config
copy_login_url = config.copy_login_url
copy_term_url = config.copy_term_url
paste_login_url = "https://www.spec-akpp.ru/user/login"
username = config.username
password = config.password

# Create robobrowser object
def create_robobrowser():
    return RoboBrowser(parser='html.parser')

# Login to url
def login_robobrowser(RB,url,username, password):
    RB.open(copy_login_url)
    form = RB.get_form()
    form['name'] = username
    form['pass'] = password
    RB.submit_form(form)

# Navigate to list of terms
def get_term_url_list(RB):
    RB.open(copy_term_url)
    soup = RB.parsed
    terms = soup.findAll('tr')
    len(terms)
    term_url_list = []
    for idx, term in enumerate(terms):
        try:
            element = term.find('li').find('a', href=True)
            href = element.attrs['href']
            term_url = "https://novosibirsk.spec-akpp.ru"+href
            term_url_list.append(term_url)
        except:
            pass
    term_url_list = list(set(term_url_list))
    return term_url_list

# Run webdriver to navigate javascript
def start_chrome_driver():
    import webdriver
    chrome_path = "/Users/pAulse/Documents/Projects/webpage-copier/chromedriver"
    driver = webdriver.Chrome(executable_path=chrome_path)
    # driver.set_window_size(window_width, window_height)
    return driver

def driver_login(driver, url, username, password):
    driver.get(url)
    driver.find_element_by_id('edit-name').send_keys(username)
    driver.find_element_by_id('edit-pass').send_keys(password)
    driver.find_element_by_id("edit-submit").click()

def copy_source_data(driver,term_url_list):
    # Start the chrome driver and login
    # driver = start_chrome_driver()
    # driver_login(driver=driver, url=copy_login_url, username=username, password=password)
    terms_dict = dict()
    for idx, url_term in enumerate(term_url_list):
        term_dictionary = dict()
        driver.get(url_term)
        title = driver.find_element_by_id('edit-name-0-value').get_attribute('value')
        # driver.find_element_by_id('cke_32').click()
        form_text = driver.find_element_by_class_name('form-textarea').get_attribute('data-editor-value-original')
        url_alias = driver.find_element_by_id('edit-path-0-alias').get_attribute('value')
        meta_title = driver.find_element_by_id("edit-field-meta-0-basic-title").get_attribute('value')
        meta_description = driver.find_element_by_id("edit-field-meta-0-basic-description").get_attribute('value')
        term_dictionary["URL"] = url_term
        term_dictionary["Title"] = title
        term_dictionary["Form Text"] = form_text
        term_dictionary["Url Alias"] = url_alias
        term_dictionary["Meta Title"] = meta_title
        term_dictionary["Meta Description"] = meta_description
        terms_dict[idx] = term_dictionary

    return terms_dict

def main():
    robobrowser = create_robobrowser()
    login_robobrowser(RB=robobrowser, url=copy_login_url, username=username, password=password)

    term_url_list = get_term_url_list(RB=robobrowser)

    # Copy data from each term_url
    chrome_driver = start_chrome_driver()
    driver_login(driver=chrome_driver,
                 url=copy_login_url,
                 username=username,
                 password=password)
    source_data = copy_source_data(driver=chrome_driver, term_url_list=term_url_list)

    # source_data[0]['Form Text'].replace("\n","")
    # source_data[0]

    # Save the website data
    import pickle
    with open('websitedata.pickle', 'wb') as f:
              pickle.dump(source_data, f)
    chrome_driver.quit()
