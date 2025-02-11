import unittest
# Load this project's module explicitly, including when invoked from repository root.
import importlib.util as _import_util
from pathlib import Path as _Path
import sys as _sys
_spec = _import_util.spec_from_file_location(
    "sunil_agents_" + _Path(__file__).parent.name, _Path(__file__).with_name("main.py"))
_main = _import_util.module_from_spec(_spec)
_sys.modules[_spec.name] = _main
_spec.loader.exec_module(_main)
expand = _main.expand

class ExpansionTests(unittest.TestCase):
    def test_one_hop_and_provenance(self):
        result=expand("voice",{"voice":["audio"],"audio":["sound"]})
        self.assertEqual(result["expansions"],[{"term":"audio","weight":0.5,"rule":"voice"}])
    def test_whole_token_and_multiword_rules(self):
        self.assertEqual(expand("drag",{"rag":["retrieval"]})["expansions"],[])
        self.assertEqual(expand("vector store",{"vector store":["index"]})["expansions"][0]["term"],"index")

