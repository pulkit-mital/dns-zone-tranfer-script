#!/usr/bin/python
'''
This script will take file or google excel sheet as the list 
of domains for which we have to transfer zone files
'''
import dns.query
import dns.resolver
import dns.zone
from multiprocessing import Pool
import os

class ZoneFileTransfer(object):
    
    def __init__(self):
        self.option=0
        self.welcome_text='welcome to zone tranfer'

    def banner(self):
        print(self.welcome_text)
        print('this script will help you to tranfer zone file for the domains')
        print('Please choose the given option from which you have to list of domains')
        print('[1] From Google Excel Sheet')
        print('[2] From Local File')


    def show_options(self):
        self.option = int(input('Choose option from above (1 or 2):'))
        if self.option == 1:
            #TODO do parsing with excel
            print('From google excel')
        elif self.option == 2:
            #TODO do parse from local file
            local_file_path = input('Please Enter local file path: ')
            print(local_file_path)
            self.get_domains_from_file(local_file_path)
        else:
            print('Incorrect option. Please choose from the list above')
            self.show_options()


    def get_domains_from_file(self, file_path):
        file_content = open(file_path,"r").readlines()
        self.dns_querying(file_content)


    def dns_querying(self, file_content):
        pool = Pool(processes=25)
        pool.map(self.start, file_content)


    def start(self, line):
        domain = line.replace("www.","")
        domain = domain.strip()
        print(domain)
        try:
            ns = dns.resolver.query(domain, 'NS')
            for ser in ns.rrset:
                server = str(ser)[:-1]
                print(server)
                try:
                    zone_file = dns.zone.from_xfr(dns.query.xfr(str(server), domain, relativize=False), relativize=False)
                except Exception as e:
                    print(e)
                    zone_file = None
                    continue
                print(zone_file.to_text())
        except Exception as e:
            print(e)
            return


def main():
    zone_file_transfer = ZoneFileTransfer()
    zone_file_transfer.banner()
    zone_file_transfer.show_options()


if __name__ == '__main__':
    main()

