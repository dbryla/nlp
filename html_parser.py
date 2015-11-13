import pickle
import BeautifulSoup
import re

def makelist(table):
    result = []
    rows = table.findAll('tr')
    for row in rows:
        columns = row.findAll('td')
        fragment = u''
        for col in columns:
            words = [unicode(s) for s in col.findAll(text=True)]
            fragment += u' '.join(words)
        fragment = re.sub(r"  \[.*\]", "", fragment)
        result.append(fragment)
    return result

with open('export.html', 'rb') as f:
    data = f.read()
    soup = BeautifulSoup.BeautifulSoup(data)
    f = open('data.pkl', 'wb')
    pickle.dump(makelist(soup.find('table')), f)
    f.close()