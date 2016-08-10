import feedparser
import os
from requests.exceptions import HTTPError

#query arXiv API for paper results
def getResult(id):
    url = 'http://export.arxiv.org/api/query'
    #payload = {'id_list': '1405.6842'}
    results = feedparser.parse(url+'?id_list='+id)
    
    if results['status'] != 200:
        raise Exception('HTTP error: ' +results['status']+ ' Paper: '+id)
    
    return results['entries'][0]

#parse results into dict with relevant info, including bib entry
def parseResult(id, res):
    title = res['title']
    year = res['published'].split('-', 1)[0]
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
            'arxid': id
            }

#get all arXiv papers in given directory     
def getFiles(directory):

    files = [f for f in os.listdir(directory) if 'arXiv' in f and '.pdf' in f]
    
    return files

#gets arXiv id from .pdf name
def fileToId(fname):
    f = fname.strip('arXiv_')
    id = f.strip('.pdf')
    return id



                


