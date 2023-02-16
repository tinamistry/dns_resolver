import array
import dns
import dns.query
import dns.resolver
import dns.message
import dns.rdataclass
import dns.rdatatype
import dns.rcode
import dns.name


def mydig():
    domain_name = input("Enter a domain name ")
    find_root_server(domain_name)  # returns the ip address of the root server


def find_root_server(domain_name):
    root_servers = ['198.41.0.4', '199.9.14.201','192.33.4.12']
    #  # all the roots servers we need to check
    # '199.7.91.13', '192.203.230.10', '192.5.5.241',
    # '192.112.36.4', '198.97.190.53', '192.36.148.17',
    # '192.58.128.30', '193.0.14.129', '199.7.83.42', '202.12.27.33']

    for server in root_servers:  # check all the root server
        recursive_query(domain_name, server)
        return

def check_additional_section(response):
    additional = response.additional
    for a in additional:
        if a.rdtype == dns.rdatatype.A:
            ip_address = (a.to_text().split())[4]  # now we have the new ip_address we want to query
            return ip_address


def recursive_query(domain_name, ip_address):
    query = dns.message.make_query(domain_name, 'A', 'IN', None, False, None, None, None, None, None, None, 0)
    response = dns.query.udp(query, ip_address, None, 53, None, 0, True, True, True, False, None)
   # print("response for query: ")
    #print(response)
    if response.answer != []:
        answer = response.answer
        for ans in answer:
            if ans.rdtype == dns.rdatatype.CNAME: # if we get the cname we have to repeat the query with the new domainname
                new_domain_name = ans.to_text().split()[4]
                find_root_server(new_domain_name)
            if ans.rdtype == dns.rdatatype.A:
                final_answer_found(ans)
                return

    else:  # if the answer section is not filled, we need to check the additional section
        if response.additional != []:
            ip = check_additional_section(response)
            recursive_query(domain_name, ip)
        else:
            return

def final_answer_found(final_response):
    print(final_response)

if __name__ == '__main__':
    mydig()
