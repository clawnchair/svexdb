from sv.models import Trainer, TSV
from sv.serializers import TrainerSerializer, TSVSerializer
from rest_framework import renderers, viewsets
from django.http import Http404


class TrainersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Trainer.objects.all().order_by('username')
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = TrainerSerializer
    paginate_by = 200


class ShinyValueViewSet(viewsets.ReadOnlyModelViewSet):
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = TSVSerializer

    def get_queryset(self):
        gen = self.kwargs['gen']
        tsv = int(self.kwargs['tsv'])
        if tsv >= 4096:
            raise Http404
        return TSV.objects.tsv_search(tsv, gen)


class TrainerViewSet(viewsets.ReadOnlyModelViewSet):
    renderer_classes = [renderers.JSONRenderer]
    serializer_class = TrainerSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        return Trainer.objects.user_search(username)
