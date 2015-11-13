import pickle

import sys
#import dict

reload(sys)

PRIMARY_PATTERN = u"dom"
sys.setdefaultencoding('utf8')

def main():
    f = open('data.pkl', 'rb')
    fragments = pickle.load(f)
    f.close()

    verbs = []

    snippets = []
    for fragment in fragments:
        words = fragment.split(PRIMARY_PATTERN)
        left_half = words[0].split(" ")
        right_half = words[-1].split(" ")
        left_part = ''
        right_part = ''
        found = False
        for word in left_half[::-1]:
            tmp_word = word.replace(',','').replace('.','')
            #if not dict.check_if_verb(tmp_word):
            if not tmp_word in verbs:
                left_part = word + ' ' + left_part
            else:
                left_part = word + ' ' + left_part
                found = True
                break
        if not found:
            continue
        found = False
        for word in right_half:
            tmp_word = word.replace(',','').replace('.','')
            #if not dict.check_if_verb(tmp_word):
            if not tmp_word in verbs:
                right_part += ' ' + word
            else:
                right_part += ' ' + word
                found = True
                break

        if not found:
            continue

        snippet = (left_part + PRIMARY_PATTERN + right_part)\
            .replace('  ', ' ')\
            .replace('&quot;', '"')
        snippets.append(snippet)

    return snippets

if __name__ == '__main__':
    f = open('snippets.pkl', 'wb')
    m = main()
    print m
    pickle.dump(m, f)
    f.close()