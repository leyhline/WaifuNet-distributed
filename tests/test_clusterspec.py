"""
Small-scale distributed deep learning with TensorFlow.
Copyright (C) 2018 Thomas Leyh <thomas.leyh@mailbox.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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