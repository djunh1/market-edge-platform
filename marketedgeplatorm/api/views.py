from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import PortfolioSerializer

from portfolios.models import Portfolio, Review
from django.http import JsonResponse



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
def fetchWeekdayOdds(request, pk):
    portfolio = Portfolio.objects.get(id=pk)
    user = request.user.profile
    data = request.data

    # review, created = Review.objects.get_or_create(
    #     owner=user,
    #     portfolio=portfolio,
    # )

    # review.body = data['body']
    # review.save()
    print('DATA', data)
    serializer = PortfolioSerializer(portfolio, many=False)
    return Response(serializer.data)


# @api_view(['GET'])
#@permission_classes([IsAuthenticated])
# def getWeekdayOdds(request):
#     projects = Project.objects.all()
#     serializer = PortfolioSerializer(projects, many=True)
#     return Response(serializer.data)
