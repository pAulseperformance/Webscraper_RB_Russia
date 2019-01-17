import robo_browser

def copy_car_submodel_data():

    car_submodel_dict = dict()
    title = chrome_driver.find_element_by_id('edit-title-0-value').get_attribute('value')
    subtitle = chrome_driver.find_element_by_id('edit-field-zagolovok-anonsa-0-value').get_attribute('value')
    description = chrome_driver.find_element_by_id("edit-body-0-value").get_attribute('data-editor-value-original')

    el = chrome_driver.find_element_by_id('edit-field-razdel-kataloga')
    for option in el.find_elements_by_tag_name('option'):
        if option.is_selected():
            selected_option = option.text
            break

    meta_title = chrome_driver.find_element_by_id("edit-field-meta-0-basic-title").get_attribute('value')
    meta_description = chrome_driver.find_element_by_id("edit-field-meta-0-basic-description").get_attribute('value')

    car_submodel_dict["Title"] = title
    car_submodel_dict["Subtitle"] = subtitle
    car_submodel_dict["Form Text"] = description
    car_submodel_dict["Selected Option"] = selected_option
    car_submodel_dict["Meta Title"] = meta_title
    car_submodel_dict["Meta Description"] = meta_description

    return car_submodel_dict

# Copy data from each term_url
chrome_driver = robo_browser.start_chrome_driver()
chrome_driver.implicitly_wait(10) # Set time to wait for elements

robo_browser.driver_login(driver=chrome_driver,
                          url=robo_browser.config.copy_login_url,
                          username=robo_browser.config.username,
                          password=robo_browser.config.password)



chrome_driver.get(robo_browser.copy_term_url)
car_elements = chrome_driver.find_elements_by_class_name("menu-item__link")
len(car_elements)

car_links = []
for car_element in car_elements:
    car_links.append(car_element.get_attribute("href"))

cars_submodels_dict = {}
for car_link in car_links:
    chrome_driver.get(car_link)

    # Get the Car submodels urls
    car_model_links = []
    for i in range(2,100):
        try:
            car_model_link = chrome_driver.find_element_by_xpath("//div/div/div["+str(i)+"]/div[1]/div/a").get_attribute("href")
            car_model_links.append(car_model_link)
        except:
            break

    car_submodels_dict = dict()
    # Navigate to car_model_link
    for i in range(len(car_model_links)):
        chrome_driver.get(car_model_links[i])

        # Navigate to edit the car model
        chrome_driver.get(chrome_driver.find_element_by_link_text("Редактировать").get_attribute("href"))
        try:
            car_submodel_dict = copy_car_submodel_data()
        except Exception as e: # This catches any cars with no submodels.
            print("Exception Occured at Link:%s"% (car_model_links[i]))
            print(e)
            continue

        car_submodels_dict[i] = car_submodel_dict

    cars_submodels_dict[car_link] = car_submodels_dict

# Save the website data
import pickle
with open('cars_submodels_dict.pickle', 'wb') as f:
          pickle.dump(cars_submodels_dict, f)
