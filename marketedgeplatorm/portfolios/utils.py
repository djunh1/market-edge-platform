from .models import Portfolio, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def searchPortfolios(request) -> tuple[Portfolio, str]:

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

def paginatePortfolios(request, portfolios, results) -> tuple[range, list[Portfolio]]:

    page = request.GET.get('page')
    paginator = Paginator(portfolios, results)

    try:
        portfolios = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        portfolios = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        portfolios = paginator.page(page)

    # rolling window for number of pages to show, in case there are too many pages 
    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, portfolios