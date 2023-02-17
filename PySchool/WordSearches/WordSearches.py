from word_search_generator import WordSearch

cell_vocab = 'unicellular, multicellular, mitochondria, nucleus, membrane, cytoplasm, chloroplast, wall, ribosome, life'
cell_search = WordSearch(cell_vocab, level=2, size=25)
cell_search.save('cell_search.pdf', solution=True)

graph_vocab = 'scale, interval, axis, independent, dependent, variable, title, bar, line'
graph_search = WordSearch(graph_vocab, level=2, size=25)
graph_search.save('graph_search.pdf', solution=True)
