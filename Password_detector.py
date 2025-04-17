import requests
import hashlib

def request_api_data(query_char):
    url = "https://api.pwnedpasswords.com/range/" + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the API and try again.')
    return res

def get_pass_leak_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)  # Fixed typo
    return get_pass_leak_count(response, tail)

def main(args):
    count = pwned_api_check(args)
    if count:
        print(f"\n{args} and the semiliar passwords were hacked {count} times, you should change it.\n")
    else:
        print(f"\n{args} was not hacked, Its a good password, Carry on!\n")
    return "done!"

while True:
    option = input("Enter 1 for checking password seafty or enter any other key to exit: ")
    if option == '1':
        data = input("Enter the password you want to check for: ")
        main(data)
    else:
        print("Thank you!")
        break