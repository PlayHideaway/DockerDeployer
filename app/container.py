from os import getenv 

class Container:
    def __init__(self):
        self.containerName = getenv("CONTAINER")

    def Update(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def delete(self):
        pass

    def create(self):
    
    def pull(self):
        pass

    def getLabels(self):
        pass

    def getEnVars(self):
        pass

    def getVolumes(self):
        pass

    def getPorts(self):
        pass
    
    def getUser(self):
        pass

    def getDepends(self):
        pass

    def getImage():
        pass