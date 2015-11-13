import pickle
import graph

edges_counter = {}

def create_pairs(snippets):
    pairs_per_snippet = {}
    for snippet in snippets:
        words = snippet.replace(',','').replace('.','').split(' ')
        for i in range(len(words) - 1):
            for j in range(i + 1, len(words)):
                if snippet in pairs_per_snippet:
                    pairs_per_snippet[snippet].append([words[i], words[j], None])
                else:
                    pairs_per_snippet[snippet] = [[words[i], words[j], None]]
    return pairs_per_snippet

def check_if_exists(pairs, edges):
    for pair in pairs:
        for edge in edges:
            if pair[0] == edge[0] and pair[1] == edge[1] or pair[0] == edge[1] and pair[1] == edge[0]:
                pair[2] = edge
                if edge in edges_counter:
                    edges_counter[edge] += 1
                else:
                    edges_counter[edge] = 1


def filter_results(pairs):
    results = []
    for pair in pairs:
        if (pair[2]):
            results.append(pair)
    return results

if __name__=='__main__':
    f = open('snippets.pkl', 'rb')
    snippets = pickle.load(f)
    f.close()
    pairs_per_snippet = create_pairs(snippets)
    edges = graph.get_edges()
    for pairs in pairs_per_snippet.values():
        check_if_exists(pairs, edges)
    for snippet, pairs in pairs_per_snippet.iteritems():
        new_pairs = filter_results(pairs)
        if len(new_pairs) != 0:
            print snippet
            for pair in new_pairs:
                print '\t', pair[0], pair[1], edges_counter[pair[2]], pair[2].attr['weight']