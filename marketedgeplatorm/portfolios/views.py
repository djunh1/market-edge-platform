from django.shortcuts import render, redirect

from django.http import HttpResponse
from .models import Portfolio
from .forms import PortfolioForm


def portfolios(request):
    # portfolios, search_query = searchportfolios(request)
    # custom_range, portfolios = paginateportfolios(request, portfolios, 6)
    portfolios = Portfolio.objects.all()
    context = {'portfolios': portfolios}
    return render(request, 'portfolios/portfolios.html', context)

def portfolio(request, pk):
    portfolio = Portfolio.objects.get(id=pk)
    return render(request, 'portfolios/portfolio.html', {'portfolio': portfolio})

def stock(request, pk):
    return HttpResponse('Caesar')

def createPortfolio(request):
    portfolio_form = PortfolioForm()
    context = {'form': portfolio_form}
    if request.method == 'POST':
        portfolio_form = PortfolioForm(request.POST)
        if portfolio_form.is_valid():
            portfolio_form.save()
            return redirect('portfolios')


    return render(request, 'portfolios/portfolio_form.html', context)

def updatePortfolio(request, pk):

    portfolio = Portfolio.objects.get(id=pk)
    portfolio_form  = PortfolioForm(instance=portfolio)

    if request.method == 'POST':
        # newtags = request.POST.get('newtags').replace(',',  " ").split()

        portfolio_form = PortfolioForm(request.POST, instance=portfolio)
        if portfolio_form.is_valid():
            portfolio = portfolio_form.save()
            # for tag in newtags:
            #     tag, created = Tag.objects.get_or_create(name=tag)
            #     portfolio.tags.add(tag)

            return redirect('portfolios')

    context = {'form': portfolio_form , 'portfolio': portfolio}
    return render(request, "portfolios/portfolio_form.html", context)

def deletePortfolio(request, pk):
    portfolio = Portfolio.objects.get(id=pk)
    if request.method == 'POST':
        portfolio.delete()
        return redirect('portfolios')
    
    context = {'object': portfolio}
    return render(request, 'delete_template.html', context)  
