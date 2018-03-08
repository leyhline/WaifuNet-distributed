import random
import os
import re
from typing import List, Dict
from os import PathLike
ClusterSpec = Dict[str, List[str]]


class ClusterSpecParser:
    """
    Class for holding cluster specification for distributed TensorFlow training.
    Each server needs the same specification, passed as a dict.
    """
    def __init__(self, max_ps=1, max_workers=16):
        """
        :param max_ps: Maximum number of parameter servers. There should at least be one.
        :param max_workers: Maximum number of workers. There should at least be one.
        """
        assert max_ps > 0
        self.max_ps = max_ps
        assert max_workers > 0
        self.max_workers = max_workers
        self.spec: ClusterSpec = dict()

    def to_dict(self) -> ClusterSpec:
        return self.spec

    def to_json(self) -> str:
        raise NotImplementedError()

    def parse_textfile(self, path: PathLike):
        """
        Parse textfile containing hostnames separated by newlines.
        """
        with open(path) as fd:
            hostnames = [line for line in fd if line]
        self.parse_list(hostnames)
        
    def parse_list(self, hostnames: List):
        match_nonascii = re.compile(r"\W", flags=re.ASCII)
        sanitized = [match_nonascii.sub("", name) for name in hostnames]
        sampled = random.sample(sanitized, self.max_ps + self.max_workers)
        ps = sampled[:self.max_ps]
        workers = sampled[self.max_ps:]
        self.spec = {"ps": ps, "worker": workers}
