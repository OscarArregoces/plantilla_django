from abc import ABC


class ProviderRepository(ABC):
    def __init__(self, repo) -> None:
        self.repo = repo

    def get_instance(self, id, prefetch=None, related=None):
        return self.repo.get_instance(id, prefetch, related)

    def filter_in(self, **kwargs):
        return self.repo.filter_in(**kwargs)

    def get_filter_related(self, filter_param=None, related=None, prefetch=None):
        return self.repo.get_filter_related(filter_param, related, prefetch)

    def complex_filters(self, **kwargs):
        return self.repo.complex_filters(**kwargs)

    def get_all(self, related=None, prefetch=None):
        return self.repo.get_all(related, prefetch)

    def bulk_delete(self, ids):
        return self.repo.bulk_delete(ids)

    def get(self):
        return self.repo.get()

    def post(self, data):
        return self.repo.post(data)

    def put(self, id, data):
        return self.repo.put(id, data)

    def delete(self, id):
        return self.repo.delete(id)
