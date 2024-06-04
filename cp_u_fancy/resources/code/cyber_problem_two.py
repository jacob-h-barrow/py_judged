import requests
import os

class MacLookup:
    def __init__(self, mac_lookup_table_location: str = "/home/optimus/mac_lookup_table.csv"):
        self.runnable = True
        self.file_location = mac_lookup_table_location
        
        exists = False
        
        try:
            exists = os.path.exists(self.file_location)
        except:
            print("Path doesn't exist!")
            print("Fetching data!")
            
        try:
            if exists == False:
                self.retrieve_table()
        except:
            print("Can't run app!")
            self.runnable = False
                
        self.load_table()
            
    def retrieve_table(self):
        data = requests.get("https://raw.githubusercontent.com/wireshark/wireshark/master/manuf")
        text = data.text
        
        with open(self.file_location, "w") as writer:
            writer.write(text)
            
        print("Saved data!")
        
    def break_mac_subnet(self, value: str) -> str:
        if '/' not in value:
            return value
            
        mac, subnet = value.split('/')
        subnet = int(subnet)
        
        count = 0
        base_mac = ""
        
        for character in mac:
            if character.isalnum():
                count += 4
                base_mac += character
                
            if count >= subnet:
                break
            else:
                base_mac += character

        return base_mac
            
    def load_table(self):
        self.mac_lookup_table = {}
        
        with open(self.file_location) as reader:
            for line in reader.read().strip().split('\n')[65:]:
                line = line.split()
                
                self.mac_lookup_table[self.break_mac_subnet(line[0])] = line[1]
                
    def lookup(self, unknown_mac: str) -> bool | str:
        # Could be faster here! Inefficiency is just terrible :P
        for mac_base, value in sorted(self.mac_lookup_table.items(), key = lambda x: len(x[0]), reverse = True):
            if mac_base in unknown_mac:
                return value
        return False
        
if __name__ == "__main__":
    mac_table = MacLookup()
    
    print(mac_table.lookup("00:03:DA:FF:FD:DE"))
