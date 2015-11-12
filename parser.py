import os
import BeautifulSoup
import re
#import nltk

#from nltk.corpus import WordNetCorpusReader
import graph
import sys

reload(sys)

PRIMARY_PATTERN = u"dom"
sys.setdefaultencoding('utf8')

# def load_wordnet():
#     cwd = os.getcwd()
#     nltk.data.path.append(cwd)
#     wn_path = "{0}/plwordnet_2_3_pwn_format".format("plwordnet_2_3/")
#     wn = WordNetCorpusReader(os.path.abspath("{0}/{1}".format(cwd, wn_path)), nltk.data.find(wn_path))
#     return wn

def get_table(htmldoc):
    soup = BeautifulSoup.BeautifulSoup(htmldoc)
    return soup.find('table')

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
 
def read_fragments(file_name):
    with open(file_name, 'rb') as f:
        data = f.read()
        fragments = makelist(get_table(data))
        return fragments
    
def main():
    fragments = read_fragments("export.html")

    # wn = load_wordnet()

    verbs = []
    # set(wn.all_lemma_names(pos='v'))

    snippets = []
    for fragment in fragments:
        words = fragment.split(PRIMARY_PATTERN)
        left_half = words[0].split(" ")
        right_half = words[-1].split(" ")
        left_part = ''
        right_part = ''
        for word in left_half[::-1]:
            if not word in verbs:
                left_part = word + ' ' + left_part
            else:
                left_part = word + ' ' + left_part
                break
        for word in right_half:
            if not word in verbs:
                right_part += ' ' + word
            else:
                right_part += ' ' + word
                break

        snippet = (left_part + PRIMARY_PATTERN + right_part)\
            .replace('  ', ' ')\
            .replace('&quot;', '"')
        snippets.append(snippet)

    return snippets


def create_pairs(snippets):
    pairs_per_snippet = {}
    for snippet in snippets:
        words = snippet.replace(',','').replace('.','').split(' ')
        for i in range(len(words) - 1):
            for j in range(i + 1, len(words)):
                if snippet in pairs_per_snippet:
                    pairs_per_snippet[snippet].append([words[i], words[j], 0, 0.0])
                else:
                    pairs_per_snippet[snippet] = [[words[i], words[j], 0, 0.0]]
    return pairs_per_snippet

def check_if_exists(pairs, edges):
    for pair in pairs:
        for edge in edges:
            if pair[0] == edge[0] and pair[1] == edge[1] or pair[0] == edge[1] and pair[1] == edge[0]:
                pair[2] += 1
                pair[3] = edge.attr['weight']


def filter_results(pairs):
    results = []
    for pair in pairs:
        if (pair[2] != 0):
            results.append(pair)
    return results

if __name__=='__main__':
    snippets = main()
    pairs_per_snippet = create_pairs(snippets)
    edges = graph.get_edges()
    for pairs in pairs_per_snippet.values():
        check_if_exists(pairs, edges)
    for snippet, pairs in pairs_per_snippet.iteritems():
        new_pairs = filter_results(pairs)
        if len(new_pairs) != 0:
            print snippet
            for pair in new_pairs:
                print pair[0], pair[1], pair[2], pair[3]