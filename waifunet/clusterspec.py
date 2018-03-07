import random
from typing import List, Dict
ClusterSpec = Dict[str, List[str]]


def generate_clusterspec_dict(hostnames: List[str], max_ps=1, max_workers=16) -> ClusterSpec:
    sampled_hostnames = random.sample(hostnames, max_ps + max_workers)
    ps = sampled_hostnames[:max_ps]
    workers = sampled_hostnames[max_ps:]
    clusterspec = {"ps": ps, "worker": workers}
    return clusterspec
