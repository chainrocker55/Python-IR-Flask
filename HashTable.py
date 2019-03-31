class Node:
	def __init__(self, key, value, file,position):
            self.key = key
            self.value = value
            self.file = {file}
            self.position = [[file,position]]
            self.next = None

	def __str__(self):
		return "%s %s" % (self.key, self.value)

	def __repr__(self):
		return str(self)

class HashTable:

    def __init__(self):
      self.capacity = 2663 
      self.size = 0
      self.buckets = [None]*self.capacity

    def hash(self, key):
      hashsum = 0
      for idx, c in enumerate(key):
        hashsum += (idx + len(key)) ** ord(c)
        hashsum = hashsum % self.capacity
      return hashsum


    def insert(self, key, value, file, position):

      index = self.hash(key)
      node = self.buckets[index]

      if node is None:
        self.buckets[index] = Node(key, value , file, position)
        self.size += 1
        return
      prev = node
      while node is not None:
        if(node.key==key):
          node.value=value
          node.file.add(file)
          k=0
          flag=0
          while k < len(node.position):
              if(node.position[k][0]==file):
                node.position[k].append(position)
                flag=1
              k=k+1
          if(flag==0):
            node.position.insert(k,[file,position])

          self.size += 1
          return
        prev = node
        node = node.next
      prev.next = Node(key, value , file, position)
      self.size += 1

    def find(self, key):
      index = self.hash(key)
      node = self.buckets[index]
      while node is not None and node.key != key:
        node = node.next
      if node is None:
        return None
      else:
        return node.value

    def search(self, key):
      index = self.hash(key)
      node = self.buckets[index]
      while node is not None and node.key != key:
        node = node.next
      if node is None:
        return None
      else:
        return node
