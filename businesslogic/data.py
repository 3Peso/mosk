class CollectionData:
    def __init__(self, data, currentdatetime=None, sourcehash=None):
        self.collecteddata = data
        self.currentdatetime = currentdatetime
        self.sourcehash = sourcehash

    def __str__(self):
        result = "Collection Time Stamp: {}\r\n\r\n{}".format(self.currentdatetime, self.collecteddata)
        return result
