import logging

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .serializers import PortfolioSerializer

from portfolios.models import Portfolio, Review
from api.service.stock_bar_service import StockBarService
from django.http import JsonResponse

import api.helpers.clients as helper_clients



@api_view(['GET'])
def getRoutes(request) -> Response:
    routes = [
        {'GET': '/api/portfolios'},
        {'GET': '/api/portfolios/id'},
        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},
    ]
    return Response(routes)

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def getPortfolios(request):
    portfolios = Portfolio.objects.all()
    serializer = PortfolioSerializer(portfolios, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPortfolio(request, pk):
    portfolio = Portfolio.objects.get(id=pk)
    serializer = PortfolioSerializer(portfolio, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fetchWeekdayOdds(request, ticker) -> Response:
    '''
    Fetches weekday odds for a given ticker
    '''

    stock_api_client = helper_clients.FmpAPIClient(ticker)
    stock_price_data = stock_api_client.get_stock_data()

    if len(stock_price_data) == 0:
        logging.warning('No data returned from the API for ticker={}'.format(ticker))
        Response(status=status.HTTP_204_NO_CONTENT)

    logging.info('Successfully fetched data for the ticker={}'.format(ticker))

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    stock_service = StockBarService(start_date, end_date, ticker)
    hit_matrix_json = stock_service.generate_weekday_hit_matrix_response(stock_price_data)

    return Response(hit_matrix_json)


