class Node:
    def __init__(self, initdata):
        self.data = initdata
        self.next = None

    def getData(self):
        return self.data

    def getNext(self):
        return self.next

    def setData(self, newdata):
        self.data = newdata

    def setNext(self, newnext):
        self.next = newnext


class UnorderedList:

    def __init__(self):
        self.head = None

    def isEmpty(self):
        return self.head == None

    def add(self, item):
        n = Node(item)
        n.setNext(self.head)
        self.head = n

    def size(self):
        count = 0
        current = self.head
        while current != None:
            count = count + 1
            current = current.getNext()
        return count

    def search(self, item):
        current = self.head
        found = False
        while current != None and not found:
            if current.getData() == item:
                found = True
            else:
                current = current.getNext()

        return found

    ##Searches for item, returns true and moves it forward if item is in the list
    ##returns false if item is not in the list.
    # def HPsearch(self, item):

    def remove(self, item):
        current = self.head
        previous = None
        found = False
        while not found:
            if current.getData() == item:
                found = True
            else:
                previous = current
                current = current.getNext()
        if previous == None:
            self.head = current.getNext()
        else:
            previous.setNext(current.getNext())

    def append(self, item):
        current = self.head
        temp = Node(item)
        if current == None:
            self.head = temp
        else:
            while current.getNext() != None:
                current = current.getNext()
            current.setNext(temp)

    def insert(self, pos, item):
        # inserts item at position pos
        current = self.head
        previous = None
        temp = Node(item)
        for i in range(pos):
            previous = current
            current = current.getNext()
        temp.setNext(current)
        previous.setNext(temp)

    def __str__(self):
        listAsString = "["
        current = self.head
        while current.getNext() != None:
            listAsString = listAsString + str(current.getData()) + ","
            current = current.getNext()
        listAsString = listAsString + str(current.getData()) + "]"

        return listAsString

    def index(self, item):
        # returns the index or position of item, assume item is in list
        current = self.head
        index = 0
        while current.getData() != item:
            current = current.getNext()
            index += 1
        return index

    def pop(self):
        # removes and returns the last item on the list
        current = self.head
        previous = None
        while current.getNext() != None:
            previous = current
            current = current.getNext()
        previous.setNext(None)
        return current.getData()


# Every time I set the Next node to the previous it would make it a intiger not
    def HPsearch(self, item):
        current = self.head
        found = False
        previous = None
        prePrevious = None

        while current != None and not found:
            if current.getData() == item:
                if current == self.head:
                    found = True
                else:
                    if previous == self.head:
                        previous.setNext(current.getNext())

                        found = True
                    else:
                        prePrevious.setNext(current)
                        previous.setNext(current.getNext())
                        current.setNext(previous)
                        found = True
            else:
                prePrevious = previous
                previous = current
                current = current.getNext()

        return found
