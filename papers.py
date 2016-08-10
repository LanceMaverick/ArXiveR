import sys
import re
import dataset
import parsers

class papers:
    
    def __init__(self, db_loc = 'sqlite:///papers.db'):
        
        self.db_loc = db_loc
        
        db = dataset.connect(self.db_loc)
        
        self.table = db['papers']
        self.dirs = db['dirs']

    #syncs db with all the added directories
    def update(self, force = False):
        for directory in self.dirs:
            self.addPapers(directory['path'], force)

    #add a directory to sync db of papers with
    def addDir(self, directory):
        if  not self.dirs.find_one(path = directory):
            self.dirs.insert(dict(path = directory))
                
    #scan directories and add arXiv info for arXiv_<arxiv_id>.pdf files
    #if force == True, all info is updated from the arXiv API 
    def addPapers(self, directory, force):
        files = parsers.getFiles(directory)
        ids = [parsers.fileToId(f) for f in files]
        
        for id in ids:
            
            if not self.table.find_one(arxid = id) or force:
                
                res = parsers.parseResult(id, parsers.getResult(id))
                self.table.insert(res)
                return True
            else:
                return False

    #returns list of sync paths
    def getDirs(self):
        dirs = [] 
        for directory in self.dirs:
            dirs.append(directory['path'])
        return dirs 

    #returns list of all paper id's
    def getPapers(self):
        papers = [] 
        for paper in self.table.all():
            papers.append(paper['arxid'])
        return papers 
    
    #remove a sync path
    def removeDir(self, directory):
        #TODO find the relevant exception from dataset...
        try:
            self.dirs.delete(path=directory)
        except Exception as e:
            print e
            pass

