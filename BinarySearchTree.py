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

