from __future__ import division
from pygraphviz import *
import csv
import sys

reload(sys)
sys.setdefaultencoding('utf8')

title = 'dom'

graph = AGraph(directed=True)
graph.add_node(title)
graph.graph_attr['overlap'] = 'false'
graph.graph_attr['root'] = title

with open('dom/dom.csv', 'rb') as file:
    rows = csv.reader(file, delimiter=',', quotechar='"')
    for row in rows:
        graph.add_edge('dom', row[1], weight=int(row[0]) / 900)
with open('dom/mieszkanie.csv', 'rb') as file:
    rows = csv.reader(file, delimiter=',', quotechar='"')
    for row in rows:
        graph.add_edge('mieszkanie', row[1], weight=int(row[0]) / 900)
with open('dom/moj.csv', 'rb') as file:
    rows = csv.reader(file, delimiter=',', quotechar='"')
    for row in rows:
        graph.add_edge('moj', row[1], weight=int(row[0]) / 900)
with open('dom/rodzinny.csv', 'rb') as file:
    rows = csv.reader(file, delimiter=',', quotechar='"')
    for row in rows:
        graph.add_edge('rodzinny', row[1], weight=int(row[0]) / 900)

if __name__ == '__main__':
    graph.layout()
    graph.draw(title + '.png')

def get_edges():
    return graph.edges()
