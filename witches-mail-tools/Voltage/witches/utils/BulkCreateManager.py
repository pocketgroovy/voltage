__author__ = 'yoshi.miyamoto'


class BulkCreateManager(object):
    model = None
    chunk_size = None
    instances = None

    def __init__(self, model, chunk_size=None):
        self.model = model
        self.chunk_size = chunk_size
        self.instances = []

    def append(self, instance):
        if self.chunk_size and len(self.instances) >= self.chunk_size:
            self.create()
            self.instances = []

        self.instances.append(instance)

    def create(self):
        self.model.objects.bulk_create(self.instances)
