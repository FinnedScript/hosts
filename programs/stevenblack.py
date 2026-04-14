# This program fetches the newest version of StevenBlack's host files
# and converts it to a Little Snitch readable format.

import os
import json
from datetime import date


def main():
    domains = add_data()
    convert(domains)


def add_data():
    # Local variables
    hosts = {}
    hosts['unified_domains'] = parse('python3 /home/linux/github/stevenblack/updateHostsFile.py -s -m -a', is_unified=True)
    hosts['pornography_domains'] = parse('python3 /home/linux/github/stevenblack/updateHostsFile.py -e porn -s -m -a', unified_domains=hosts['unified_domains'])
    hosts['gambling_domains'] = parse('python3 /home/linux/github/stevenblack/updateHostsFile.py -e gambling -s -m -a', unified_domains=hosts['unified_domains'])
    hosts['fake_news_domains'] = parse('python3 /home/linux/github/stevenblack/updateHostsFile.py -e fakenews -s -m -a', unified_domains=hosts['unified_domains'])
    hosts['social_domains'] = parse('python3 /home/linux/github/stevenblack/updateHostsFile.py -e social -s -m -a', unified_domains=hosts['unified_domains'])

    # Return the domains list
    return hosts

    
def parse(os_command, unified_domains=list(), is_unified=False):
    unified_domains = set(unified_domains)
    domains = set()
    hosts_path='/home/linux/github/stevenblack/hosts'
    # Update main hosts list
    os.system(os_command)
    # Add each domain to the domains list
    with open(hosts_path) as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('0.0.0.0'):
                domain = line.strip('0.0.0.0')
                domain = domain.strip()
                domain = domain.strip('\n')
                if is_unified:
                    domains.add(domain)  
                else:
                    if domain not in unified_domains:
                        domains.add(domain)        
    # Remove main hosts list
    os.remove(hosts_path)
    # Sort list
    sorted_list = list(domains)
    sorted_list.sort()
    # Return a sorted list
    return sorted_list


def convert(hosts):
    for key in hosts:
        if key == 'unified_domains':
            write('adware and malware', hosts[key], 'unified')
        elif key == 'pornography_domains':
            write('pornography', hosts[key], 'pornography')
        elif key == 'gambling_domains':
            write('gambling', hosts[key], 'gambling')
        elif key == 'fake_news_domains':
            write('fake news', hosts[key], 'fakenews')
        else:
            write('social', hosts[key], 'social')


def write(description, remotes, output):
    current_date = date.today().strftime("%m-%d-%y")
    dictionary = {'name': 'Blocklist', 'description': f'Blocks known {description} domains. Updated on {current_date}', 'denied-remote-domains': remotes}
    jsonString = json.dumps(dictionary, indent=4)
    with open(f'/home/linux/github/hosts/lists/ls-{output}', 'w') as file:
        file.write(jsonString)


if __name__ == '__main__':
    main()
