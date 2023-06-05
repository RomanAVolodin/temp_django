from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView

from movies.models import Filmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']
    
    def _aggregate_person(self, role):
        return ArrayAgg('persons__full_name', distinct=True,
            filter=Q(personfilmwork__role=role))

    def get_queryset(self):
        queryset = self.model.objects.prefetch_related('genres', 'persons')
        return queryset.values(
                    'id',
                    'title',
                    'description',
                    'creation_date',
                    'rating',
                    'type',
                ).annotate(
                    genres=ArrayAgg('genres__name', distinct=True),
                    actors=self._aggregate_person('actor'),
                    writers=self._aggregate_person('writer'),
                    directors=self._aggregate_person('director'),
                ).order_by('id')

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self):
        queryset = self.get_queryset()
        paginator, page, queryset, _ = self.paginate_queryset(
            queryset, 
            self.paginate_by
        )
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }
        return context


class MovieDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, *, object_list=None, **kwargs):
        return kwargs['object']
