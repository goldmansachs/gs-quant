import json
import os
import sphinx.search
from pathlib import Path

from docutils import nodes

def setup(app):
    print("Adding searchdataext output")
    sphinx.search.IndexBuilder = IndexBuilder


class IndexBuilder(sphinx.search.IndexBuilder):
    def __init__(self, env, lang, options, scoring):
        super(IndexBuilder, self).__init__(env, lang, options, scoring)
        self._doc_collector=[]
        self._outputfile = Path(os.path.dirname(__file__), '..', '_build', 'search', 'search-index.json').resolve().absolute()

    def feed(self, docname, filename, title, doctree):
        super(IndexBuilder, self).feed(docname, filename, title, doctree)

        visitor = sphinx.search.WordCollector(doctree, self.lang)
        doctree.walk(visitor)

        # index page should be marked as 'Home' for developer site search results
        if ' '.join(visitor.found_title_words) == '':
            visitor.found_title_words = ['Home']

        newdoc = {
            'title': ' '.join(visitor.found_title_words),
            'body': ' '.join(visitor.found_words),
            'key': docname
        }

        self._doc_collector.append(newdoc)

    def freeze(self):
        data = super(IndexBuilder, self).freeze()

        def ensure_dir(file_path):
            if not os.path.exists(file_path):
                os.makedirs(file_path)

        output_file_path = str(self._outputfile)
        print('Writing search data to ' + output_file_path)
        ensure_dir(os.path.dirname(output_file_path))
        with open(str(self._outputfile), 'w+') as outfile:
            json.dump(self._doc_collector, outfile, sort_keys=True, indent=4)
        return data

