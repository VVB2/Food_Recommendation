import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

def driver_setup():
    edge_options = Options()
    edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    edge_options.add_argument('--headless')
    edge_options.add_argument('--disable-extensions')
    edge_options.add_argument('--disable-logging')
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument('--disable-gpu')
    edge_options.page_load_strategy = 'eager'
    driver = webdriver.Edge(options=edge_options)
    driver.implicitly_wait(5)
    return driver

def bulk_scrapper(df, driver):
    index = 1
    data_json = []
    for _, data in df.iterrows():
        print(f'Scrapping {index} of {df.shape[0]}')
        index += 1
        result_data = {
            'title': data['title'],
            'ingredients': data['ingredients'],
            'directions': data['directions'],
            'link': data['link'],
            'narration': data['NER'],
            'image_url': 'https://t4.ftcdn.net/jpg/04/73/25/49/360_F_473254957_bxG9yf4ly7OBO5I0O5KABlN930GwaMQz.jpg'
        }
        try:
            driver.get(f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q={data['title']} recipe")

            img_box = driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img')

            img_box.click()

            time.sleep(0.5)

            try:
                fir_img = driver.find_element(By.XPATH, '/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]')

                result_data['image_url'] = fir_img.get_attribute('src')

            except Exception:
                pass

            data_json.append(result_data)

        except Exception:
            pass

    return data_json