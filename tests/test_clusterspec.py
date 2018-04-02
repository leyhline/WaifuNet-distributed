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

import os
from os import path
import pytest
import json
from waifunet.clusterspec import ClusterSpecParser


this_directory_path = path.abspath(path.dirname(__file__))
sane_input_file = "list_hostnames_result.txt"


class TestParseTextfile:
    @staticmethod
    def initialize_parser():
        parser = ClusterSpecParser()
        parser.parse_textfile(path.join(this_directory_path, sane_input_file))
        return parser
    
    def test_to_dict(self):
        parser = self.initialize_parser()
        result = parser.to_dict()
        self.check_parsed_textfile(result)

    def test_to_json(self):
        parser = self.initialize_parser()
        result = parser.to_json()
        result_as_dict = json.loads(result)
        self.check_parsed_textfile(result_as_dict)

    def test_write_json_to_file(self):
        filename = "list_hostnames_result.json"
        filepath = path.join(this_directory_path, filename)
        parser = self.initialize_parser()
        parser.save_json(filepath)
        with open(filepath, "r") as fd:
            result = json.load(fd)
        os.remove(filepath)
        self.check_parsed_textfile(result)

    @staticmethod
    def check_parsed_textfile(result):
        assert len(result) == 2
        assert "ps" in result
        assert "worker" in result
        ps = result["ps"]
        workers = result["worker"]
        assert len(ps) == 1
        TestParseTextfile.check_for_tfpool_in_names(ps)
        assert len(workers) == 16
        TestParseTextfile.check_for_tfpool_in_names(workers)

    @staticmethod
    def check_for_tfpool_in_names(hostnames):
        for name in hostnames:
            assert name[:6] == "tfpool"


class TestConstructor:
    def test_sane_input(self):
        parser = ClusterSpecParser(max_ps=1, max_workers=1)
        assert parser.max_ps == 1
        assert parser.max_workers == 1
    
    def test_not_enough_ps(self):
        with pytest.raises(AssertionError):
            ClusterSpecParser(max_ps=0)

    def test_not_enough_workers(self):
        with pytest.raises(AssertionError):
            ClusterSpecParser(max_workers=0)


class TestParseExternalCommand:
    def test_parse_list_hostnames_mock_sh(self):
        command = [path.join(this_directory_path, "list_hostnames_mock.sh")]
        parser = ClusterSpecParser()
        parser.parse_external(command)
        result = parser.to_dict()
        TestParseTextfile.check_parsed_textfile(result)
