import requests
from bs4 import BeautifulSoup
import re
import csv

url = 'https://www.amazon.in/gp/bestsellers/books/'
response = requests.get(url)
page_content = BeautifulSoup(response.content, "html.parser")
kaamhogaya = page_content.find_all(class_='zg_pagination')
hogaya = kaamhogaya[0].find_all('a')

url = []
page_content = []
output = []
output.append(["Name", "URL", "Author", "Price"])
output[0].append("Number of Ratings")
output[0].append("Average Rating")
for x in hogaya:
    url.append(x['href'])

for x in url:
    response = requests.get(x)
    page_content.append(BeautifulSoup(response.content, "html.parser"))

for x in page_content:
    kaamhogaya = x.find_all(class_='zg_itemImmersion')
    for y in kaamhogaya:
        hogaya = y.find_all(class_='zg_itemWrapper')
        for z in hogaya:
            # print(z)
            temp1 = z.find(class_='p13n-sc-truncate')
            name = ' '.join(temp1.get_text().rsplit())

            temp2 = z.find_all(class_='a-link-normal')
            i = 1
            for a in temp2:
                if i == 1:
                    out_url = "www.amazon.in"+''.join(a['href'].rsplit())
                    i = 2
                    continue
                temp5 = a.get_text()
                match = re.search('out of 5 stars', temp5)
                if i == 2 and match is not None:
                    flag = 1
                    avg_rat = a['title']
                    i = 3
                    continue
                elif i == 2:
                    avg_rat = "Not Available"
                    no_of_rat = "Not Available"
                    i = 4
                if i == 3 and flag == 1:
                    no_of_rat = a.get_text()
                    i = 4
                    continue
                if i == 4:
                    temp4 = a.find(class_='p13n-sc-price')
                    if temp4 is not None:
                        temp4 = ''.join(temp4.get_text().rsplit())
                        price = temp4
                        price = "Rs. "+price
                    else:
                        price = "Not Available"
                    i = 5

            '''temp3=z.find(class_='a-size-small a-link-child')'''
            temp3 = z.find(class_='a-row a-size-small')
            if temp3 is not None:
                temp3 = ' '.join(temp3.get_text().rsplit())
                author = temp3
            else:
                author = "Not Available"
            row1 = []
            row1.append(name)
            row1.append(out_url)
            row1.append(author)
            row1.append(price)
            row1.append(no_of_rat)
            row1.append(avg_rat)
            output.append(row1)
            # print("AdityaJP")
        # print("-----------book_content++---------")

with open('./output/in_bestseller.csv', 'w', newline='') as csvfile:
    adi_writer = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for x in output:
        adi_writer.writerow(x)
'''text_content()
'''
