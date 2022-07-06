import helpers
from utils.clean import clean_str ,clean_list
from utils.filters import remove_basic_lands

class Deck(object):
    """
    Class used as abstraction for a domain object deck
    """
    def __init__(self,raw_data:dict,format:str):
        self.raw_data:dict = raw_data
        self.domain_helper: helpers.Domain = helpers.Domain()
        if "sections" in raw_data.keys():
            self.constructor_with_sections()
        else:
            self.constructor_without_sections()

    def constructor_with_sections(self):
        """
        Method used to build deck information when the 
        raw data becomes with sections specified
        """
        for section in self.raw_data.get("sections").keys():
            cards:list = self.raw_data.get("sections").get(section)
            name:str = clean_str(section)
            if name in self.domain_helper.allowed_sections:
                if name == "lands":
                    cards = list(filter(remove_basic_lands,cards))
                cards = clean_list(cards)
                self.sections.append(Section(name,cards))

    def constructor_without_sections(self):
        """
        Method used to build deck information when the 
        raw data becomes without sections specified
        """
        pass

class Section(object):
    def __init__(self,name:str,cards:list):
        self.raw_cards:list = cards
        self.name:str = name
        self.build()
    
    def build(self):
        pass