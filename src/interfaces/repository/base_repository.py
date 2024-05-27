from abc import ABC
from django.db import models


class BaseRepository(ABC):
    def __init__(self, model) -> None:
        self.model = model

    def get_instance(self, id, prefetch=None, related=None):
        try:
            if prefetch:
                return self.model.objects.prefetch_related(*prefetch).get(pk=id)

            elif related:
                return self.model.objects.select_related(*related).get(pk=id)

            return self.model.objects.get(pk=id)
        except Exception:
            return None

    def bulk_delete(self, ids):
        try:
            instances = self.model.objects.filter(pk__in=ids)

            for _, instance in enumerate(instances):
                instance.visible = False

            self.model.objects.bulk_update(instances, ["visible"])
            return "Ok", True
        except Exception as e:
            return e.args, False

    def get(self):
        return self.model.objects.filter(visible=True)

    def get_all(self, related=None, prefetch=None):
        if related:
            return self.model.objects.all().select_related(*related)
        elif prefetch:
            return self.model.objects.all().prefetch_related(*prefetch)
        else:
            return self.model.objects.all()

    def get_filter_related(self, filter_param=None, related=None, prefetch=None):
        filtro = None

        if filter_param:
            filtro = models.Q()

            for fk in filter_param[0].keys():
                filtro &= models.Q(**{fk: filter_param[0].get(fk, None)})

        if filter_param and related:
            return self.model.objects.filter(filtro).select_related(*related)
        elif filter_param and prefetch:
            return self.model.objects.filter(filtro).select_related(*prefetch)

        elif filter_param:
            return self.model.objects.filter(filtro)
        elif related:
            return self.model.objects.all().select_related(*related)
        elif prefetch:
            return self.model.objects.all().prefetch_related(*prefetch)

    def complex_filters(self, **kwargs):
        model = self.model.objects

        for k in kwargs.keys():
            v = kwargs.get(k, None)

            if not v:
                continue

            if k == "filter":
                filtro = models.Q()

                for fk in v.keys():
                    filtro &= models.Q(**{fk: v.get(fk, None)})

                model = model.filter(filtro)
            elif k == "related":
                model = model.select_related(*v)
            elif k == "prefetch":
                model = model.prefetch_related(*v)
            elif k == "annotate":
                annotate = {}
                for fk in v[0].keys():
                    annotate[fk] = v[0].get(fk, None)
                model = model.annotate(**annotate)
            elif k == "aggregate":
                model.aggregate(*v)
            elif k == "values":
                model = model.values(*v)
            elif k == "defer":
                model = model.defer(*v)

        return model

    def filter_in(self, **kwargs):
        field = kwargs.get("field", [])
        return self.model.filter(id__in=field)

    def post(self, data):
        return None

    def put(self):
        return None

    def delete(self):
        return None
