class Nix_Cgroup(object):
    def __init__(self, **kwargs):
        for field in ('name', 'cpu_limit', 'memory_limit'):
            setattr(self, field, kwargs.get(field, None))

class Process(object):
    def __init__(self, **kwargs):
        for field in ('pid', 'name'):
            setattr(self, field, kwargs.get(field, None))