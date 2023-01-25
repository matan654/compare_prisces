# import ftplib
# import gzip
# import requests
# from requests.auth import HTTPDigestAuth
from selenium import webdriver
# import webbrowser
import time
# from cerberus.client import CerberusClient
# import logging
# from ftplib import FTP
from xml.dom import minidom
from ftplib import FTP_TLS
import sqlite3
# from datetime import datetime as dt


listOfStoresFiles = []
listOfPriceFiles = []
listOfPromoFiles = []

def load_db_ramilevi_files(store_id, file_type, file_date, file_name):
    connection = sqlite3.connect('stors.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS RamiLeviFiles(StoreId INT PRIMARY KEY, filetype TEXT, priceDate INT, pricefile TEXT, promoDate INT, promofile TEXT)''')
    cursor.execute("SELECT COUNT(StoreId) FROM RamiLeviFiles WHERE StoreId = " + store_id)
    if cursor.fetchone()[0] > 0: #check if StoreId exist in the DB
        # צריך להוסיף התניה שבדוק את סוג הקובץ ותעדכן אם זה מבצעים או מחירים
        cursor.execute("SELECT * FROM RamiLeviFiles WHERE StoreId =" + store_id)
        if "PriceFull" in file_name:
            record = cursor.fetchone()[2]
            if record <= int(file_date):
                cursor.execute("UPDATE RamiLeviFiles SET filetype = '" + file_type + "',priceDate= '" + file_date + "', pricefile= '" + file_name + "' WHERE StoreId = " + store_id)
        else:
            record = cursor.fetchone()[4]
            if record <= int(file_date):
                cursor.execute("UPDATE RamiLeviFiles SET filetype = '" + file_type + "',promoDate= '" + file_date + "', promfile= '" + file_name + "' WHERE StoreId = " + store_id)
    else:
        if "PriceFull" in file_name:#להמשיך להוסיף את כל הפרמטרים של שאילתת הכנסה לDB אם התניה לבדיקה של סוג הקובץ מבצעים או מחירים
            cursor.execute("INSERT INTO RamiLeviFiles VALUES('" + store_id + "','" + file_type + "','" + file_date +  "','" + file_name + "')")
    connection.commit()
    connection.close()

def fill_list(line):
    # load_db_ramilevi_files(line)
    # print(line[-15:-3])
    if ("xml" in line):
        load_db_ramilevi_files('0', line[29:41], line[-3:], 'none',line[-16:-4], line[-36:])
        listOfStoresFiles.append(line[42:])
        # print(line[42:])
    if ("PriceFull" in line):
        print(line[-42:])
        load_db_ramilevi_files(line[-19:-16], line[29:41], line[-2:], 'PriceFull', line[-15:-3], line[-42:])
        # print(line[-20:-15])
        # if any(line[-20:-15] in s for s in listOfPrice):
        listOfPriceFiles.append(line[-2:])
        # print(line[42:])
    if ("PromoFull" in line):
        load_db_ramilevi_files(line[-19:-16], line[29:41], line[-2:], 'PromoFull', line[-15:-3], line[-42:])
        # print(line[-20:-15])
         # print(line[42:])
        listOfPromoFiles.append(line[42:])


def find_store_number_by_name(file_name, city_name):
    with open(file_name, "wb") as file:
        # Command for Downloading the file "RETR filename"
        ftps.retrbinary(f"RETR {file_name}", file.write)
        print(filename)
    doc = minidom.parse(file_name)
    staffs = doc.getElementsByTagName("Store")

    finded_stores_list = []
    for staff in staffs:
        ct = staff.getElementsByTagName("City")[0]
        city = ct.firstChild.data.strip()
        if city_name == city:
            store = staff.getElementsByTagName("StoreId")[0]
            finded_stores_list.append(store.firstChild.data.strip())
    return finded_stores_list


def load_db_ramilevi_stores_list(file_name):
    connection = sqlite3.connect('stors.db', timeout=10)
    cursor = connection.cursor()
    # Create table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Stores(StoreId INT PRIMARY KEY, StoreName TEXT, Address TEXT, City TEXT)''')
    with open(file_name, "wb") as file:
        # Command for Downloading the file "RETR filename"
        ftps.retrbinary(f"RETR {file_name}", file.write)
        print(filename)
    doc = minidom.parse(file_name)
    staffs = doc.getElementsByTagName("Store")
    for staff in staffs:
        store_id = ((staff.getElementsByTagName("StoreId")[0]).firstChild.data.strip())
        store_name = ((staff.getElementsByTagName("StoreName")[0]).firstChild.data.strip())
        address = ((staff.getElementsByTagName("Address")[0]).firstChild.data.strip())
        city = ((staff.getElementsByTagName("City")[0]).firstChild.data.strip())
        # city = city.firstChild.data.strip()

        if cursor.execute("SELECT COUNT(StoreId) FROM Stores WHERE StoreId = " + store_id):
            cursor.execute("UPDATE Stores SET StoreName = '" + store_name + "',Address= '" + address + "', City= '" + city + "' WHERE StoreId = " + store_id)
        else:
            cursor.execute("INSERT INTO Stores VALUES('" + store_id + "','" + store_name + "','" + address + "','" + city + "')")
        # x = cursor.fetchone()[0]
    connection.commit()
    connection.close()


stores = "xml"
prices = "PriceFull"
promo = "PromoFull"


# def test():
#     r = {'StoreId': , 'StoreName':, 'Address':, 'City':}



def insert_stores(self):
    insert_db = "INSERT INTO stores{} VALUES (:StoreId, :StoreName, :Address, :City)"
    with connection:
        cursor.execute(insert_db, (self.store_id, self.store_name, self.address, self.city))

super_dict_list = [{'url':'publishedprices.co.il', 'login_name':'RamiLevi', 'login_pass':'', 'chain_store':'RamiLevi'},
                   {'url':'publishedprices.co.il', 'login_name':'RamiLevi', 'login_pass':'', 'chain_store':'RamiLevi'},
                   {'url':'publishedprices.co.il', 'login_name':'RamiLevi', 'login_pass':'','chain_store': 'RamiLevi'},
                   {'url':'publishedprices.co.il', 'login_name':'RamiLevi','login_pass': '','chain_store': 'RamiLevi'}]


if __name__ == "__main__": #test()


    ftps = FTP_TLS('publishedprices.co.il')
    ftps.login('RamiLevi', '')  # login anonymously before securing control channel
    ftps.prot_p()  # switch to secure data connection.. IMPORTANT! Otherwise, only the user and password is encrypted and not all the file data.

    # x = ftps.nlst()


    ftps.retrlines('LIST', fill_list)

    # allStores[:] = [i for i in allStores if i.find(stores) != -1]

    filename = listOfStoresFiles[-1].split(" ")[-1]
    load_db_ramilevi_stores_list(filename)
    # print(find_store_number_by_name(filename, "אילת"))
    # Write file in binary mode
    ####################################
    # with open(filename, "wb") as file:
    #     # Command for Downloading the file "RETR filename"
    #     ftps.retrbinary(f"RETR {filename}", file.write)
    #     print(filename)
    #
    # doc = minidom.parse(filename)
    # staffs = doc.getElementsByTagName("Store")
    # for staff in staffs:
    #     staff_id = staff.getElementsByTagName("StoreId")[0]
    #     name = staff.getElementsByTagName("Address")[0]
    #     city = staff.getElementsByTagName("City")[0]
    #     print("Store Id:% s, Address:% s, City:% s" % (staff_id.firstChild.data.strip(), name.firstChild.data.strip(), city.firstChild.data.strip()))
    #
    #
    # for y in staffs:
    #     ct = y.getElementsByTagName("City")[0]
    #     city = ct.firstChild.data.strip()
    #     if 'באר שבע' == city:
    #         store = y.getElementsByTagName("StoreId")[0]
    #         print(store.firstChild.data.strip())
    #################################

    # with gzip.open(filename, "rb") as f:
    #     data = f.read()
    #     print(data)
# test

    exit(0)

url = "https://publishedprices.co.il/login"
post_login_url = "https://publishedprices.co.il/file"

payload = {
    'username': 'RamiLevi',
    'password': 'ads',
    'RememberUser': 'true'
}

# without opening chrome browser.
# op = webdriver.ChromeOptions()
# op.add_argument('headless')
# driver = webdriver.Chrome("C:/Users/matanam1/PycharmProjects/pythonProject1/venv/Lib/site-packages/chromedriver/chromedriver.exe", options=op)

# use for open chrome.
driver = webdriver.Chrome(
    "C:/Users/matanam1/PycharmProjects/pythonProject1/venv/Lib/site-packages/chromedriver/chromedriver.exe")
driver = webdriver.Chrome(
    "C:\Users\matanam1\PycharmProjects\pythonProject\venv\Lib\site-packages\chromedriver\chromedriver.exe")

driver.get(url)

elem = driver.find_element_by_id("username")
elem.clear()
elem.send_keys("RamiLevi\n")
time.sleep(0.5)
elem = driver.find_element_by_class_name("form-control")
elem.clear()
elem.send_keys("pricefull")
# time.sleep(1)
driver.find_element('id', "breadcrumb")
print(driver.page_source)

elem = driver.find_elements_by_class_name('f')
# print(elem)
button = driver.find_element_by_class_name('dt')
button.click()
button.click()
time.sleep(3)
driver.close()

# s = requests.session()
# res = s.post(url, data=payload, verify=False)
# res = s.post(url, auth=HTTPDigestAuth("RamiLevi", 'asd'), verify=False)
# print(res.text)
# res = s.get(post_login_url)
# print(res.text)
