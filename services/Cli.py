from collections import namedtuple
from persistance.Models import CustomerDetails

class Cli:
    
    def __init__(self):
        pass
        
    def get_new_customer_details(self) -> CustomerDetails:
        return CustomerDetails('Ankush', 'Challa', 'test_addr')
