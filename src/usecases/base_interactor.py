class BaseInteractor:
    def __init__(self, repo) -> None:
        self.repo = repo

    def get_filter_related(
        self, filter_param=None, related=None, prefetch=None, **kwargs
    ):
        reps = self.repo.get_filter_related(filter_param, related, prefetch)

        order = kwargs.get("order", None)
        if order:
            return reps.order_by(*order)
        return reps

    def complex_filters(self, **kwargs):
        reps = self.repo.complex_filters(**kwargs)

        order = kwargs.get("order", None)
        if order:
            return reps.order_by(*order)
        return reps

    def filter_in(self, **kwargs):
        reps = self.repo.filter_in(**kwargs)
        return reps

    def get_instance(self, data, prefetch=None, related=None):
        return self.repo.get_instance(data, prefetch, related)

    def get_all(self, related=None, prefetch=None):
        return self.repo.get_all(related, prefetch)

    def bulk_delete(self, ids):
        return self.repo.bulk_delete(ids)

    def get(self) -> list:
        return self.repo.get()

    def post(self, data):
        return self.repo.post(data)

    def put(self, id: int, data):
        return self.repo.put(id, data)

    def delete(self, data: list[int]):
        return self.repo.delete(data)
