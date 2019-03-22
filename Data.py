class Data:
    def __init__(self,id,word,position):
        self.id = id
        self.word = word
        self.file = {id}
        self.position = [[id,position]]
        self.num = 1

    def __str__(self):
        return self.word+ " "+ str(self.num)+" "+str(self.file)+" position: "+str(self.position)
