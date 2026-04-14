# This program fetches the newest Apple telemetry domains
# and converts them to a Little Snitch readable format.

import json
import requests
from datetime import date

def main():
    domains = add_data()
    write('Apple telemetry', list(domains), 'apple')


def add_data():
    domains = set()
    response = requests.get('https://raw.githubusercontent.com/mullvad/dns-blocklists/refs/heads/main/lists/doh/privacy/hagezi-tracker-apple')
    lines = response.text.split('\n')
    for line in lines:
        if len(line) > 0:
            domains.add(line)
    response = requests.get('https://raw.githubusercontent.com/FinnedScript/hosts/main/domains/apple-telemetry')
    lines = response.text.split('\n')
    for line in lines:
        if len(line) > 0:
            domains.add(line)
    
    return set(sorted(list(domains)))


def write(description, remotes, output):
    current_date = date.today().strftime("%m-%d-%y")
    dictionary = {'name': 'Blocklist', 'description': f'Blocks known {description} domains. Updated on {current_date}', 'denied-remote-domains': remotes}
    jsonString = json.dumps(dictionary, indent=4)
    with open(f'/home/linux/github/hosts/lists/ls-{output}', 'w') as file:
       file.write(jsonString)


if __name__ == '__main__':
    main()
