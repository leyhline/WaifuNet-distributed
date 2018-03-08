from os import path
import unittest
import waifunet.clusterspec as spec


this_directory_path = path.abspath(path.dirname(__file__))
sane_input_file = "list_hostnames_result.txt"


class TextfileToDict(unittest.TestCase):
    def setUp(self):
        self.parser = spec.ClusterSpecParser()
    
    def test_on_sane_input(self):
        self.parser.parse_textfile(path.join(this_directory_path, sane_input_file))
        result = self.parser.to_dict()
        self.assertEqual(len(result), 2)
        self.assertTrue("ps" in result)
        self.assertTrue("worker" in result)
        ps = result["ps"]
        workers = result["worker"]
        self.assertEqual(len(ps), 1)
        self._check_for_tfpool_in_names(ps)
        self.assertEqual(len(workers), 16)
        self._check_for_tfpool_in_names(workers)
    
    def _check_for_tfpool_in_names(self, hostnames):
        for name in hostnames:
            self.assertEqual(name[:6], "tfpool")


class ConstructorTest(unittest.TestCase):
    def test_sane_input(self):
        parser = spec.ClusterSpecParser(max_ps=1, max_workers=1)
        self.assertEqual(parser.max_ps, 1)
        self.assertEqual(parser.max_workers, 1)
    
    def test_not_enough_ps(self):
        with self.assertRaises(AssertionError):
            spec.ClusterSpecParser(max_ps=0)

    def test_not_enough_workers(self):
        with self.assertRaises(AssertionError):
            spec.ClusterSpecParser(max_workers=0)