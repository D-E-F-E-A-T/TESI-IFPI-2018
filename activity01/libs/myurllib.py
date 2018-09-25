import requests

def download(url, num_retries=2):
    print('Downloading data from:', url)
    page = None
    try:
        response = requests.get(url)
        page = response.text
        if response.status_code >= 400:
            print('Download error:', response.text)
        if num_retries and 500 <= response.status_code < 600:
            return download(url, num_retries - 1)
    except requests.exceptions.RequestException as e:
        print('Download error:', e.reason)
    return page

if __name__ == '__main__':
    a = download('http://www.google.com')
    print(a)