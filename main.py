import locale
import re
import time
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options




while True:
    try:
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        driver.get("https://ais.usvisa-info.com/tr-tr/niv/users/sign_in")

        email = driver.find_element(By.XPATH, "//*[@id=\"user_email\"]")
        email.send_keys("bahar_denizli@hotmail.com")

        password = driver.find_element(By.XPATH, "//*[@id=\"user_password\"]")
        password.send_keys("Denizli321*")

        policy = driver.find_element(By.XPATH, "//*[@id=\"sign_in_form\"]/div[3]/label/div")
        policy.click()

        login_button = driver.find_element(By.XPATH, "//*[@id=\"sign_in_form\"]/p[1]/input")
        login_button.click()

        time.sleep(3)

        turkish_month_names = {
            'Ocak': 'January',
            'Şubat': 'February',
            'Mart': 'March',
            'Nisan': 'April',
            'Mayıs': 'May',
            'Haziran': 'June',
            'Temmuz': 'July',
            'Ağustos': 'August',
            'Eylül': 'September',
            'Ekim': 'October',
            'Kasım': 'November',
            'Aralık': 'December'
        }


        def extract_date_from_text(text):
            locale.setlocale(locale.LC_TIME, 'tr_TR')
            date_pattern = re.compile(r'(\d{1,2} \w+,\s\d{4},\s\d{1,2}:\d{2})')
            match = date_pattern.search(text)

            if match:
                found_date = match.group(1)
                datetime_format = "%d %B, %Y, %H:%M"
                parsed_date = datetime.strptime(found_date, datetime_format)

                return parsed_date
            else:
                return None


        text_element = driver.find_element(By.XPATH, '//*[@id="main"]/div[2]/div[2]/div[1]/div/div/div[2]/p[1]')
        text_content = text_element.get_attribute(
            "innerText")
        print("Metin İçeriği:", text_content)

        result_date = extract_date_from_text(text_content)
        print("Bulunan Tarih:", result_date)

        continue_button = driver.find_element(By.XPATH,
                                              "//*[@id=\"main\"]/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/ul/li/a")
        continue_button.click()

        time.sleep(3)

        try:
            element = driver.find_element(By.LINK_TEXT, "Randevuyu Yeniden Zamanla")
            driver.execute_script("arguments[0].click();", element)
            print("Elemente tıklandı!")
        except Exception as e:
            print("Element bulunamadı veya tıklanamadı:", e)

        time.sleep(3)
        try:
            element = driver.find_element(By.XPATH,
                                          '//a[@class="button small primary small-only-expanded" and text()="Randevuyu Yeniden Zamanla"]')
            driver.execute_script("arguments[0].click();", element)
            print("Yeni butona tıklandı!")
        except Exception as e:
            print("Yeni buton görünmedi:", e)

        time.sleep(3)
        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="appointments_consulate_appointment_date"]')))
            driver.execute_script("arguments[0].click();", element)
            print("Yeni butona tıklandııı takvim açıldı!")
        except Exception as e:
            print("Yeni buton görünmedi:", e)

        day_list = []

        while len(day_list) == 0:
            day_elements = driver.find_elements(By.XPATH,
                                                '//table[@class="ui-datepicker-calendar"]//td[not(contains(@class, "ui-state-disabled"))]')
            day_list = [day.text for day in day_elements]

            if len(day_list) == 0:
                try:
                    element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="ui-datepicker-div"]/div[2]/div/a/span')))
                    driver.execute_script("arguments[0].click();", element)
                    print("Yeni aya tıklandı")
                except Exception as e:
                    print("Yeni ay açılamadı:", e)
                continue
            else:
                print("Günler:", day_list)
                first_day_element = day_elements[0]
                print("İlk gün numarası:", first_day_element.text)

                day_number = first_day_element.text
                day = first_day_element.find_element(By.TAG_NAME, "a").text
                month = first_day_element.get_attribute("data-month")
                year = first_day_element.get_attribute("data-year")
                month = str(int(month) + 1)
                print("Ay:", month)
                print("Yıl:", year)

                try:
                    first_day_element.click()
                    print("İlk gün elementine tıklandı.")
                except Exception as e:
                    print("İlk gün elementine tıklanırken hata oluştu:", e)
                break

        try:
            hour = driver.find_element(By.XPATH, '//*[@id="appointments_consulate_appointment_time"]')
            driver.execute_script("arguments[0].click();", hour)
            time.sleep(3)
            print("Saat seçim elementi bulundu!")
            select = Select(hour)
            select.select_by_index(1)
            time.sleep(10)
            print("Saat seçildi!")
        except Exception as e:
            print("Saat seçim elementi bulunamadı:", e)

        selected_time = select.first_selected_option.get_attribute("value").strip()
        print("Seçilen Saat:", selected_time)
        hour, minute = selected_time.split(":")

        formatted_date = f"{year}-{month.zfill(2)}-{day_number.zfill(2)} {hour}:{minute}"
        print("Seçilen Tarih:", formatted_date)

        if result_date > datetime.strptime(formatted_date, "%Y-%m-%d %H:%M"):
            time.sleep(10)
            submit_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                                         '//*[@id="appointments_submit"]')))
            driver.execute_script("arguments[0].click();", submit_element)
            time.sleep(10)
            confirm_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                                         '/html/body/div[6]/div/div/a[2]')))
            driver.execute_script("arguments[0].click();", confirm_element)
            time.sleep(100)
            print("Tarih değiştirildi!")
            print("Tarih uygun!")
            driver.quit()
            break

        else:
            print("Tarih uygun değil!")
        time.sleep(300)
        driver.quit()
    except Exception as e:
        print("Hata:", e)
        driver.quit()
        continue
