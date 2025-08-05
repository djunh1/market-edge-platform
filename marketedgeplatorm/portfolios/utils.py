from .models import Portfolio, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def searchPortfolios(request):

    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)

    portfolios = Portfolio.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__username__icontains=search_query) |
        Q(portfolio_type__icontains=search_query) |
        Q(tags__in=tags)
    )
    return portfolios, search_query