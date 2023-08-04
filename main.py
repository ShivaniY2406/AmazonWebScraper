from bs4 import BeautifulSoup
import requests
import csv

def get_product_details(product_links):
    HEADERS=({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36','Accept=language':'en-US,en;q=0.5'})
    web_page = requests.get(product_links,headers=HEADERS)
    new_soup = BeautifulSoup(web_page.content,'html.parser')
    title = new_soup.find('span',attrs={'id':'productTitle'}).text.strip()
    ratings = new_soup.find('span',attrs={'id':'acrCustomerReviewText'}).text
    price = new_soup.find('span',attrs={'class':'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'}).text
    product_desc = new_soup.find('meta', attrs={'name': 'description'})['content'].strip()
    reviews = new_soup.find('span', {'id': 'acrCustomerReviewText'}).get_text().strip()
    reviews_count = int(reviews.replace(',', ''))
    return{
        'title':title,
        'price':price,
        'ratings':ratings,
        'reviews':reviews_count,
        'product_Description':product_desc
    }

def save_csv(data,name):
    with open(name, 'w', newline='', encoding='utf-8') as csvfile:
        fieldname = ['Title', 'Price', 'Rating', 'Reviews', 'Product_Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldname)
        writer.writeheader()
        writer.writerows(data)

def main():
    keyword=input("Enter keyword to search and fetch data :")
    url = f'https://www.amazon.com/s?k='+keyword
    scraped_data=[]
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    links=[soup.find_all('a',attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})]

    for link in links:
        link_1 = str(link.get('href'))
        product_links="https://www.amazon.com" + link_1
        product_data=get_product_details(product_links)
        scraped_data.append(product_data)

    csv_file = f"amazon {keyword} file .csv"
    save_csv(scraped_data,csv_file)
    print(f"{csv_file} is saved")

if __name__ == '__main__':
    main()

