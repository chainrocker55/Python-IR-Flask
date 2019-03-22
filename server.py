from flask import Flask,render_template,request,redirect,url_for
import operator
import threading
from nltk.tokenize import TreebankWordTokenizer
import pandas as pd
import re
from urllib.request import urlopen

from time import time as sec
from time import asctime as asc
from time import localtime as loc
import sys
import logging

# เอาไว้ render ข้อมูล
class Result:
    def __init__(self,word=None,value=None,file=None):
        self.word = word
        self.value = value
        self.file = file

# router สำหรับรับ path
app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
@app.route('/')
def hello():
    return render_template('index.html')
@app.route('/result',methods=['POST'])
def showResult():
    word=[]
    inter=set()
    option=""
    timeStart = 0
    timeEnd = 0
    title = ""
    dateStart = asc(loc(sec()))
    dateEnd = asc(loc(sec()))
    if request.method=='POST':
        word=request.form['word'].lower().split(" ")
        option = request.form['algo']
    result=[]
    if option == "1" :
        title = "Sequence"
        timeStart = sec()
        dateStart = asc(loc(sec()))
        for i in word:
            temp = search(i)

            if temp != None:
                result.append(Result(temp.word,temp.num,temp.file))
            else:
                result.append(Result(i))
        timeEnd = sec()
        dateEnd = asc(loc(sec()))


    elif option == "2" :
        title = "Binary Search Tree"
        timeStart = sec()
        dateStart = asc(loc(sec()))
        for i in word:
            temp = binary.get(i)
            if temp != None:
                result.append(Result(temp.key,temp.payload,temp.file))
            else:
                result.append(Result(i))
        timeEnd = sec()
        dateEnd = asc(loc(sec()))

    elif option == "3" :
        title = "Hash Table"
        timeStart = sec()
        dateStart = asc(loc(sec()))
        for i in word:
            temp = hashTable.search(i)
            if temp != None:
                result.append(Result(temp.key,temp.value,temp.file))
            else:
                result.append(Result(i))
        timeEnd = sec()
        dateEnd = asc(loc(sec()))

    elif option == "4" :
        title = "Binary search"
        timeStart = sec()
        dateStart = asc(loc(sec()))
        for i in word:
            temp = searchBinary(i)
            if temp != None:
                result.append(Result(temp.word,temp.num,temp.file))
            else:
                result.append(Result(i))
        timeEnd = sec()
        dateEnd = asc(loc(sec()))

    elif option == "5" :
        title = "Intersection"
        timeStart = sec()
        dateStart = asc(loc(sec()))
        inter = intersect(word)
        for i in word:
            temp = hashTable.search(i)
            if temp != None:
                result.append(Result(temp.key,temp.value,temp.file))
            else:
                result.append(Result(i))
        timeEnd = sec()
        dateEnd = asc(loc(sec()))

    time = timeEnd - timeStart
    return render_template('result.html',result=result,time=time,title = title,dateStart=dateStart,dateEnd=dateEnd,size=hashTable.size,intersect=inter)

@app.route('/position/<word>')
def showPosition(word):
    temp = hashTable.search(word)
    return render_template('position.html',word=word,position=temp.position)

# โหลดข้อมูล จาก ไฟล์ csv
df = pd.read_csv('Web.csv')
url=[]
for line in range(len(df)):
  url.append(df['Column'][line])
# class สำหรับเก็บข้อมูล
class Data:
    def __init__(self,id,word,position):
        self.id = id
        self.word = word
        self.file = {id}
        self.position = [[id,position]]
        self.num = 1

    def __str__(self):
        return self.word+ " "+ str(self.num)+" "+str(self.file)+" position: "+str(self.position)

class TreeNode:
    def __init__(self,key,val,file,left=None,right=None,parent=None):
        self.key = key
        self.payload = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent
        self.file = {file}

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def __str__(self):
      return "%s %s" % (self.key, self.payload)

class BinarySearchTree:

    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def __iter__(self):
        return self.root.__iter__()

    def put(self,key,val,file):
        if self.root:
            self._put(key,val,self.root,file)
        else:
            self.root = TreeNode(key,val,file)
        self.size = self.size + 1

    def _put(self,key,val,currentNode,file):

        if key == currentNode.key:
          currentNode.payload+=val
          currentNode.file.add(file)
          return

        if key < currentNode.key:
            if currentNode.hasLeftChild():
                   self._put(key,val,currentNode.leftChild,file)
            else:
                   currentNode.leftChild = TreeNode(key,val,file,parent=currentNode)
        else:
            if currentNode.hasRightChild():
                   self._put(key,val,currentNode.rightChild,file)
            else:
                   currentNode.rightChild = TreeNode(key,val,file,parent=currentNode)


    def get(self,key):
       if self.root:
           res = self._get(key,self.root)
           if res:
                  return res
           else:
                  return None
       else:
           return None


    def _get(self,key,currentNode):
       if not currentNode:
           return None
       elif currentNode.key == key:
           return currentNode
       elif key < currentNode.key:
           return self._get(key,currentNode.leftChild)
       else:
           return self._get(key,currentNode.rightChild)

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
      self.capacity = 1000
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

class MyThread(threading.Thread):
  def __init__(self,arr,lo,hi,sequence,binary,hashTable):
    threading.Thread.__init__(self)
    self.arr=arr
    self.lo=lo
    self.hi=hi
    self.sequence=sequence
    self.binary=binary
    self.hashTable=hashTable

  def run(self):
    for i in range(int(self.lo),int(self.hi)):
      data = urlopen(str(url[i]))
      mybytes = data.read().decode('windows-1252').lower()
      tokenizer = TreebankWordTokenizer()
      line = re.sub('[i?.,\',;:/\"<>\\%@#+-_&^$=()…—“”’*»’.``!¿\'`"â€™ï–]','', mybytes)
      arrayWord=tokenizer.tokenize(line)
      for j in range(len(arrayWord)):
        self.binary.put(arrayWord[j],1,i)
        self.sequence.append(Data(i,arrayWord[j],j))
        w=self.hashTable.find(arrayWord[j])
        if(w!=None):
          self.hashTable.insert(arrayWord[j],w+1,i,j)
        else:
          self.hashTable.insert(arrayWord[j],1,i,j)
def intersect(word):
  j=0
  temp=set()
  while True:
    if j>=len(word):
      break
    b=hashTable.search(word[j])
    if (b != None) :
      temp=b.file
      break
    else:
      j+=1
  while j < len(word):
      a=hashTable.search(word[j])
      if (a != None) :
        temp=set(temp.intersection(a.file))
      else:
        return "no intersect because word not found!!"
      j=j+1
  return temp

def cleanWord():
  i=0
  while i < len(sequence):
    j=i+1
    while j < len(sequence):  
      if(sequence[i].word == sequence[j].word ):
          sequence[i].num+=1
          sequence[i].file.add(sequence[j].id)
          k=0
          flag=0
          while k < len(sequence[i].position):
              if(sequence[i].position[k][0]==sequence[j].id):
                sequence[i].position[k].append(sequence[j].position[0][1])
                flag=1
              k=k+1
              
          if(flag==0):
            sequence[i].position.insert(k,[sequence[j].position[0][0],sequence[j].position[0][1]])
          sequence.remove(sequence[j])
      else:
          break
    i=i+1
def getData():
  l=len(url)
  thread = []
  numThread=100
  for i in range(numThread):
    thread.append(MyThread(url,(i*l)/numThread,((i+1)*l)/numThread,sequence,binary,hashTable))
    thread[i].start()
  for i in range(numThread):
    thread[i].join()
def binarySearch (l, r, x):
    if r >= l:
        mid = int(l + (r - l)/2)
        if str(sequence[mid].word) == x:
            return mid
        elif str(sequence[mid].word) > x:
            return binarySearch(l, mid-1, x)
        else:
            return binarySearch(mid + 1, r, x)
    else:
        return -1

def searchBinary(word):
  res = binarySearch(0, len(sequence)-1,word)
  if res == -1:
     return  None
  else:
    return sequence[res]

def search(word):
  for i in sequence:
    if(i.word == word):
      return i
# main
if __name__ == '__main__':
    sequence  = []
    hashTable = HashTable()
    binary = BinarySearchTree()
    getData()
    sequence = sorted(sequence, key=operator.attrgetter('word'))
    cleanWord()
    app.run(debug=True)
