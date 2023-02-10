HASH_LEN = 9857
HASH_VAR = 47


class Node:
    def __init__(self,key,value):
        self.key = key
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self,key,value):
        new_node = Node(key,value)

        if self.head == None:
            self.head = new_node
        else:
            new_node.next = self.head
            self.head = new_node

    def __str__(self):
        res = ''
        node = self.head
        while node:
            res += f'[{node.key}]: [{node.value}] ==>> '
            node = node.next
            if node == None:
                res += 'NULL'
        return res

class Hashtable:
    def __init__(self):
        self.size = HASH_LEN
        self.cells = [None] * HASH_LEN

    def gen_hash(self, key):
        sum = 0
        if isinstance(key, int):
            key = str(key)
        for char in key:
            sum += ord(char)
        hash_key = (sum * HASH_VAR)%(self.size)
        return hash_key

    def add(self,key,value):
        index = self.gen_hash(key)
        if self.cells[index] is None:
            self.cells[index] = LinkedList()
            self.cells[index].insert(key,value)
        else:
            self.cells[index].insert(key,value)


    def get(self,key):
        index = self.gen_hash(key)

        if self.cells[index] is None:
            return self.cells[index]
        else:
            node = self.cells[index].head
            while node:
                if node.key == key:
                    return node.value
                node = node.next

    def check_exist(self,key):
        index = self.gen_hash(key)
        if self.cells[index] != None:
            node = self.cells[index].head
            while node:
                if node.key == key:
                    return True
                node = node.next
        else:
            return False

if __name__ == "__main__":
    hashtable = Hashtable()
    hashtable.add("data1", 10)
    hashtable.add("data2", False)
    hashtable.add("data3", 'string')
    hashtable.add(123, 5645)

    print("data1", ' => ', hashtable.get("data1"))
    print("data2", ' => ', hashtable.get("data2"))
    print("data3", ' => ', hashtable.get("data3"))
    print(f'"data3" is {["not exist", "exist"][hashtable.check_exist("data3")]}')
    print(f'"iwewior" is {["not exist", "exist"][hashtable.check_exist("iwewior")]}')
    print(hashtable.get(123))