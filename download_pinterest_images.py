import os
import wget
import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#def execute_with_retry(method, max_attempts):
#    e = None
#    for i in range(0, max_attempts):
#        try:
#            return method()
#        except Exception as e:
#            print(e)
#            time.sleep(1)
#    if e is not None:
#        raise e

def download_images(urls):
    urls = list(set(urls))
    print('\nDownloading imagens...')
    log_file.write('Downloading imagens...\n')
    icont = 0
    for url in urls:
        try:
            wget.download(url, out=images_folder)
            icont += 1
        except:
            print('\nCound not download the image: ' + url)
            images_err.write('Cound not download the image: ' + url + '\n')
    #os.system("rm *\(1\)*")
    os.system("rm images/*\(1\)*")

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--email', type=str, dest='email', action='store',
                        required=True, help='E-mail to login on google.')
    parser.add_argument('--passwd', type=str, dest='password', action='store',
                        required=True, help='Password to login on google.')
    parser.add_argument('--link', type=str, dest='link', action='store',
                        help='Url to a pinterest folder.')
    parser.add_argument('--list', type=str, dest='url_list', action='store',
                        help='Path to a txt file with a list of urls.')
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    
    mail_address = args.email
    my_password = args.password
    link = args.link
    url_list = args.url_list

    if link == None:
        if url_list == None:
            print('Please enter an url or an url file!')
            exit()
        links = open(url_list, 'r').read().splitlines()
    else:
        links = [link] 

    log_file = open('log.txt','w')
    images_err = open('images_err.txt', 'w')

    options = webdriver.FirefoxOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Firefox(options=options)
    #capabilities = DesiredCapabilities.FIREFOX
    #capabilities["marionette"] = True
    #firefox_bin = "/usr/bin/firefox"
    #driver = execute_with_retry(lambda: webdriver.Firefox(firefox_binary=firefox_bin, capabilities=capabilities), 10)
    driver.set_page_load_timeout(60)

    print('Opening Google login page!')
    log_file.write('Opening Google login page!\n')

    try:
        driver.get("https://accounts.google.com/signin")
        print('Successfully accessed!')
        log_file.write('Google page successfully accessed!\n')
        time.sleep(5)
    except TimeoutException as e:
        print('Could not access google page!')
        log_file.write('Could not access google page!\n')
        exit()

    print('Making login on Google...')
    log_file.write('Making login on Google...\n')
    email_phone = driver.find_element_by_xpath("//input[@id='identifierId']")
    email_phone.send_keys(mail_address)
    driver.find_element_by_id("identifierNext").click()
    time.sleep(2)
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='password']")))
    password.send_keys(my_password)
    driver.find_element_by_id("passwordNext").click()

    print('Waiting for second step verification...')
    log_file.write('Waiting for second step verification...\n')
    time.sleep(30)

    print('Opening pinterest page!')
    log_file.write('Opening pinterest page!\n')
    try:
        driver.get('https://br.pinterest.com/baianode/animais-fofos/')
        print('Pinterest successfully accessed!')
        log_file.write('Pinterest successfully accessed!\n')
        time.sleep(5)
    except TimeoutException as e:
        print('Could not access the pinterest!')
        log_file.write('Could not access the pinterest!\n')
        exit()

    images_folder = 'images'
    
    print('Creating folder ' + images_folder + '...!')
    log_file.write('Creating folder ' + images_folder + '...!\n')
    os.makedirs(images_folder, exist_ok=True)
    
    num_links = len(links)
    cont = 1
    for link in links:
        print('\nDownloading ' + str(cont) + '/' + str(num_links) + '...')
        log_file.write('Downloading ' + str(cont) + '/' + \
                                        str(num_links) + '...\n')
        cont += 1
        print('Accessing pinterest link: ' + link)
        log_file.write('Accessing pinterest link: ' + link + '\n')

        try:
            driver.get(link)
            print('Link successfully accessed!')
            log_file.write('Link successfully accessed!\n')
        except TimeoutException as e:
            print('Could not access the link:' + link)
            log_file.write('Could not access the link:' + link + '\n')
            exit()
        
        print('Waitning page load...')
        log_file.write('Waitning page load...\n')
        time.sleep(30)
    
        last_height = driver.execute_script("return document.body.scrollHeight")

        urls = []
        len_urls = 0
        change_times = 0
        
        scroll_times = 0
        print('Searching images... It can take a long time!')
        log_file.write('Searching images... It can take a long time!\n')
        cont_images = 0
        while True:
            link_tags = driver.find_elements_by_tag_name('img')
            
            for tag in link_tags:
                try:
                    url = tag.get_attribute('srcset')
                    url = url.split(' ')
                    if len(url) == 8:
                        url = url[6]
                        urls.append(url)
                except:
                    continue

            driver.execute_script("window.scrollBy(0, 100);")
            scroll_times += 1

            if scroll_times == 50:
                cont_images += len(urls)
                download_images(urls)
                urls = []
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height or cont_images > 5000:
                    break
                else:
                    last_height = new_height
                    scroll_times = 0
    log_file.close()
    images_err.close()