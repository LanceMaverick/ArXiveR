import feedparser
import os
from requests.exceptions import HTTPError

#query arXiv API for paper results
def getResult(id, path):
    url = 'http://export.arxiv.org/api/query'
    results = feedparser.parse(url+'?id_list='+id)
    
    if results['status'] != 200:
        raise Exception('HTTP error: ' +str(results['status'])+ ' Paper: '+id)
        
    res = results['entries'][0]
    res['loc'] = path
    
    return res

#parse results into dict with relevant info, including bib entry
def parseResult(id, res):
    title = res['title']
    year = res['published'].split('-', 1)[0]
    author = str(res['authors'][0]['name'])
    
    if 'collaboration' in author.lower():
        authors = author
    else:
        authors = ' and '.join([a['name'] for a in res['authors']])

    doi = res['arxiv_doi']
    bibstr = ',\n'.join(['@article{'+id,
                'Author = '+ authors,
                'Year = ' + year,
                'Doi = '+ doi
                ])
    bibstr = bibstr+'\n}'
    
    return {'bib': bibstr,
            'title': title,
            'year': year,
            'authors': authors,
            'doi': doi,
            'arxid': id,
            'loc': res['loc']
            }


def checkName(fname):
    #TODO replace lots of this with regex
    c1 = '.pdf' in fname #check is pdf
    c2 = ')' not in fname #check if duplicate download - ignoring these for now
    
    fstrip = fname.strip('.pdf')
    fsstrip = fstrip.split('.',1)[0]
    
    #check format is YYMM.XXXXX
    c3 = len(fsstrip)==4
    c4 = fsstrip.isdigit() or 'arXiv' in fsstrip #or see if contains arXiv 
    
    return all([c1, c2, c3, c4])
    

#get all arXiv papers in given directory     
def getFiles(directory):
    files = [f for f in os.listdir(directory) if checkName(f)]
    
    return files

#gets arXiv id from .pdf name
def fileToId(fname):
    try:
        f = fname.strip('arXiv_')
    except:
        pass
    
    id = f.strip('.pdf')

    return id



                


