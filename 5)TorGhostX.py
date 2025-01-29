import requests
from stem import Signal
from stem.control import Controller
import time
def get_tor_session():
    session = requests.Session()
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9050',  
        'https': 'socks5h://127.0.0.1:9050'  
    }
    return session
def change_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()  
        controller.signal(Signal.NEWNYM)  
        print("IP changed successfully!")
def test_tor():
    session = get_tor_session()
    url = 'http://httpbin.org/ip'  
    response = session.get(url)
    print(f"Public IP: {response.text}")
def main():
    while True:
        test_tor()  
        change_ip()  
        time.sleep(5)  
if __name__ == "__main__":
    main()
