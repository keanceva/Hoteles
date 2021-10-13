from django.shortcuts import render,get_object_or_404
from accesos.models import Perfil
from reservas.models import Booking
from .models import Order

# Create your views here.
"""def index(request):

	reservas = Booking.objects.filter(customer_id = request.session['customer']['customer_id'])
	cuartos = [reserva.room_id for reserva in reservas]

	duos = []
	for i in range(len(reservas)):
		duos.append((reservas[i],cuartos[i]))

	print(duos)
	context = {
		'reservas': duos
	}

	return render(request, 'shopping_cart/index.html', context)
"""
def list_cart(request):

	perfil = get_object_or_404(Perfil, id = request.session['customer']['customer_id'])
	current_cart = get_object_or_404(Order, owner = perfil)

	context = {
		'cart': current_cart.items.all()
	}

	return render(request, 'shopping_cart/index.html', context)
