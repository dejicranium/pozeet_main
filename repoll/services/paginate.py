class Paginate:
    
    def __init__(self, collection, page, items_per_page=5):
        self.collection = collection
        #page is the page number
        self.page = int(page)
        self.items_per_page = int(items_per_page)

    @property
    def items(self):
        #head is the first element to start reading from, while tail is the end
        head = 0
        tail = 0
        page_number =  self.page
        if page_number == 1: 
            tail = self.items_per_page
        else:
            tail = (page_number * self.items_per_page) #adding an extra 1 because slicing of lists will end
            head = ((page_number * self.items_per_page) - self.items_per_page)
            
        return self.collection[head:tail]

    @property
    def last_page(self):
        #last page
        if len(self.collection) % self.items_per_page != 0: 
            return int(len(self.collection)/self.items_per_page) + 1
        return int(len(self.collection)/self.items_per_page)
        
