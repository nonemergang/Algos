class Element:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.none = None

class PhoneTable:
    def __init__(self, size: int = 20):
        self.size = size
        self.table = [None] * size
        self.count = 0

    def _hash(self, key):
        hash_value = 0
        i = 1
        for char in key:
            hash_value = (hash_value + ord(char)**i) % self.size
            i += 1
        return hash_value

    def put(self, new_element):
        if self.count / self.size > 0.7:
            self._rehash()
        temp_hash = self._hash(new_element)
        if self.table[temp_hash] is None:
            self.table[temp_hash] = new_element
            return
        current_element = self.table[temp_hash]
        while current_element.next is not None:
            current_element = current_element.next
    def get(self, name):
        index = self._hash(name)
        current = self.table[index]
        while current.next is not None:
            if current.key == name:
                return current.value
            current = current.next
        return None

    def _rehash(self):
        old_table = self.table
        self.size *= 2
        self.table = [None] * self.size
        self.count = 0
        for bucket in old_table:
            if bucket:
                self.put(bucket.key, bucket.value)
                self.count += 1
                current = bucket
                while current.next is not None:
                    current = current.next
                    self.put(current.key, current.value)

    def remove(self, name):
        index = self._hash(name)

        if self.table[index] is None:
            return False
        current = self.table[index]
        prev = None
        while current is not None:
            if current.key == name:
                if prev == None:
                    self.table[index] = current.next

                else:
                    prev.next = current.next
                self.count -= 1
                return True
            prev = current
            current = current.next

        return False











