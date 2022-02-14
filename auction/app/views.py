from django.shortcuts import render,redirect,get_object_or_404
from datetime import datetime
import pytz
import redis
from  .forms import MakeAnOffer
from django.views.generic.edit import CreateView
from .models import Profile,Shoes
from django.contrib import messages
import json


#import Database Redis
client = redis.StrictRedis(host='127.0.0.1', port='6379')

#views first page app
def home_page_view(request):
    return render(request,'app/base.html')

#views create auctions shoes
class Create_object_sell_view( CreateView):
    model = Shoes
    fields = "name", "image", "description", "starting_price", "buy_now", "end_auction"
    template_name = 'app/create_section.html'
    success_url = ''



#views show shoes
def show_object_sell_view(request, pk):
    profile = Profile.objects.get(user=request.user)
    shoes = get_object_or_404(Shoes, pk=pk)
    context = {'shoes': shoes}
    utc = pytz.UTC
    #if the auction ends, it rewards the winner if one exists
    if shoes.end_auction.replace(tzinfo=utc) < datetime.today().replace(tzinfo=utc):
        if shoes.buyer!= None:
            #generates a JSON file containing all the details of the auction and references to the winner.
            # Then calculate the hash of this JSON and write it in a transaction on the Ethereum (Ropsten) blockchain.

            winner_auction = {
                'Winner': f'{shoes.buyer.user}',
                'Final Shoes Price': f'{shoes.buy_now}',
                'Winner Balance': f'{shoes.buyer.usd_balance}',
                'Shoes Image': f'{shoes.image}',
                'Shoes Name': f'{shoes.name}',
            }
            winJson = json.dumps(winner_auction)
            #shoes.write_on_chain(winJson)
            messages.success(request,f"""The Shoes {shoes.name} at auction were sold at {shoes.buyer} for the price of {shoes.offer}$""" )
        else:
            messages.success(request,f"the auction that included the sale of these shoes {shoes.name}, was not awarded to anyone")
        shoes.status='close'
        shoes.save()
    return render(request, 'app/show_section.html', context)


def home_auction_view(request):

    shoes = Shoes.objects.filter(status='open').order_by('-end_auction')
    context = {'shoes': shoes}
    return render(request, 'app/home_auction.html', context)


#views make offer
def make_offer_view(request,pk):
    profile = Profile.objects.get(user=request.user)
    shoes = get_object_or_404(Shoes, pk=pk)

    if request.method == 'POST':
        form = MakeAnOffer(request.POST)
        if form.is_valid():
            offer = form.cleaned_data.get('offer')

            if offer < 0:
                messages.error(request, 'This Offer Cannot Be Updated, Because Is Lower Than 0 $')
                return redirect('app:make_an_offer', kwargs={'pk': shoes.pk})
            if profile.usd_balance >= offer:
                #if the offer is equal to the cost of the shoes to buy now the auction ends and the user wins the shoes
                if offer == shoes.buy_now:
                    if shoes.offer > 0.0:
                        prev_offer = shoes.offer
                        prev_buyer = shoes.buyer
                        prev_buyer.usd_balance+= prev_offer
                        prev_buyer.save()
                    profile.usd_balance = profile.usd_balance - shoes.buy_now
                    shoes.buyer = profile
                    profile.save()
                    messages.success(request,f"""Your offer is equal to Buy Now price. Congrats To Your Wonderfull Item Choise. Your Balance Now Is {profile.usd_balance} $""" )
                    prev_buyer.usd_balance += float(shoes.buy_now)
                    shoes.status = 'close'
                    shoes.save()
# ROPSTEN Json Here because we want the transmission to ropsten if there is a winner
                    winner_auction = {
                        'Winner': f'{shoes.buyer.user}',
                        'Final Shoes Price': f'{shoes.buy_now}',
                        'Winner Balance': f'{shoes.buyer.usd_balance}',
                        'Shoes Image': f'{shoes.image}',
                        'Shoes Name': f'{shoes.name}',
                    }
                    winJson = json.dumps(winner_auction)
                    # shoes.write_on_chain(winJson)
                    return redirect('app:home_auction')
                #if the bid is greater than the initial price and the previous bid, the user wins the auction for the time being
                elif offer >= shoes.starting_price and offer >= shoes.offer:
                    prev_offer = shoes.offer

                    if shoes.buyer!= None:
                        prev_buyer = shoes.buyer
                        prev_buyer.usd_balance += prev_offer
                        prev_buyer.save()
                    profile.usd_balance -= offer
                    shoes.offer = offer
                    shoes.buyer = profile
                    shoes.save()
                    profile.save()
                    # REDIS here because we want to check, from our database, information about active Auction
                    # Here we are saving only the first buyer of the active Auction
                    user_with_best_offer = {
                        'User with best offer': f'{shoes.buyer.user}',
                        'Best Shoes Offer': f'{shoes.offer}',
                        'User Balance': f'{profile.usd_balance}',
                        'Shoes Image': f'{shoes.image}',
                        'Shoes Name': f'{shoes.name}',
                    }
                    client.set('user_with_best_offer ', str(user_with_best_offer))

                    messages.success(request, 'Offer Update Succesfully')
                    return redirect(f'/show_section/{shoes.pk}')
                elif offer  < shoes.starting_price:
                    messages.error(request, f'Your bid cannot be considered, because the starting price for this auction is {shoes.starting_price} $' )
                    return redirect(f'/make_an_offer/{shoes.pk}')
                elif offer >= shoes.starting_price and offer <= shoes.offer:
                    messages.error(request,f'''Excuse me. Your offer cannot be considered, because an offer of {shoes.offer} has been made.
                                        If you are going to buy it, you need to make a better offer''')
                    return redirect(f'/make_an_offer/{shoes.pk}')

    else:
        form = MakeAnOffer()
    return render(request, 'app/make_an_offer.html', {'form': form,'shoes': shoes})

#views buy now
def buy_now(request):
    profile = Profile.objects.get(user=request.user)
    for shoes in Shoes.objects.filter().order_by('-end_auction'):
        buy_now = shoes.buy_now
        if profile.usd_balance >= buy_now:
            profile.usd_balance -= buy_now
            messages.success(request, f"Your Buy-Now Choise Had Success. Congrats To Your Wonderfull Item Choise. Your Balance Now Is {profile.usd_balance}" )

            if shoes.buyer!= None:
                prev_offer = shoes.offer
                prev_buyer = shoes.buyer
                prev_buyer.usd_balance += prev_offer
                prev_buyer.save()
            shoes.buyer = profile
            shoes.status='close'
            shoes.save()

            #ROPSTEN Here
            winner_buy_now= {
                'Winner': f'{shoes.buyer.user}',
                'Final Shoes Price': f'{shoes.buy_now}',
                'Winner Balance': f'{profile.usd_balance}',
                'Shoes Image': f'{shoes.image}',
                'Shoes Name': f'{shoes.name}',
            }
            winJson = json.dumps(winner_buy_now)
            #shoes.write_on_chain(winJson)


            return redirect('app:home_auction')
        else:
            messages.error(request, "You Do Not Have Necessary Funds To Do This Transaction! We Are Sending You Back To The Offer Section !")
            return redirect(f'/make_an_offer/{shoes.pk}')



