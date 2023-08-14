
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import argparse


def get_trans(driver, text, prev_result):
    driver.find_element(By.XPATH,'//*[@id="txtSource"]').click()
    driver.find_element(By.ID,"txtSource").clear()
    driver.find_element(By.ID,"txtSource").send_keys(text)
    data = driver.find_element(By.XPATH,'//*[@id="txtTarget"]').text
    while(prev_result[:10] ==  data[:10] or len(data) < 50  ):
        data = driver.find_element(By.XPATH,'//*[@id="txtTarget"]').text
    driver.find_element(By.XPATH,'//*[@id="txtSource"]').click()
    driver.find_element(By.ID,"txtSource").clear()
    print(f"data:{data[:30]}")
    if data:
        return data
    else:
        return ''

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Open a file.')
    parser.add_argument('--filename', type=str, help='Name of the file to open')
    args = parser.parse_args()
    
    text_file = open(args.filename, "r")
    data = text_file.read()
    text_file.close()
    addr_list = data.splitlines()
    idx = 0
    base_url = 'https://papago.naver.com'
    prev_result = ""
    num_called = 0
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1920, 1080) 
    driver.implicitly_wait(10)
    driver.get(base_url)
    result_list = []
    trans_len = 100
    check_len = 100

    while(idx < len(addr_list)):
        query_string = addr_list[idx:idx+trans_len]
        idx += trans_len

        if num_called >= 100:
            driver.close()
            driver = webdriver.Chrome(options=chrome_options)
            driver.implicitly_wait(10)
            driver.get(base_url)
            num_called = 0
        result = get_trans( driver,"\n".join(query_string), prev_result)
        num_called += 1
        prev_result =result
        result_list.extend(result.splitlines())
        print(f"{idx} / {len(addr_list)}")
        
        if len(result_list) % check_len == 0:
          f = open(f"./result{int(len(result_list))/check_len}.csv","w")
          f.write(("\n").join(result_list)+'\n')
          f.close()
        # print(result_list[0:])

   
