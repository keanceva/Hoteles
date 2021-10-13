from django.shortcuts import render,get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.views.generic import ListView
from django.urls import reverse_lazy
from accesos.models import Perfil
from reservas.models import Booking
from accesos.models import Usr
from shopping_cart.models import OrderItem, Order
from .models import Tour_Package
from .forms import TourOrderForm

# Create your views here.
def list_tours(request):

	objects_list = Tour_Package.objects.all()
	tour_out_of_stock = Tour_Package.objects.filter(quantity = 0)
	
	context = {
		'objects_list':objects_list,
		'tours_out_of_stock':tour_out_of_stock
	}

	return render(request,"tours_index.html",context)

class TourList(ListView):
	
	model = Tour_Package
	context_object_name = 'tours'
	template_name = 'tours_index.html'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)

		context['tours_out_of_stock'] = Tour_Package.objects.filter(available_stock = 0)
		return context


"""class TourDetails(DetailView):

	model = Tour_Package
	template_name = 'tour_details.html'

	def get_context_data(self,**kwargs):
		context = super(TourDetails,self).get_context_data(**kwargs)
		context['form'] = TourOrderForm

		return context

class TourOrder(SingleObjectMixin,FormView):

	template_name = 'tour_details.html'
	form_class = TourOrderForm
	model = Tour_Package

	def get_context_data(self,**kwargs):



	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return HttpResponseForbidden()
		self.object = self.get_object()

		return super(AuthorInterest, self).post(request, *args, **kwargs)

"""
class ParticularOrder(FormMixin,DetailView):

	template_name = 'tour_details.html'
	model = Tour_Package
	form_class = TourOrderForm
	context_object_name = 'tour_p'

	def get_success_url(self):
		return reverse_lazy('tour_package:list_tours')

	def get_context_data(self,**kwargs):
		context = super(ParticularOrder,self).get_context_data(**kwargs)
		perfil = get_object_or_404(
				Perfil, id=self.request.session["customer"]['customer_id'])

		context['form'] = TourOrderForm(initial={'tour':self.object,
			'title':self.object.title,'description':self.object.description,
			'reservation_name':perfil})
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			print(form.errors)
			return self.form_invalid(form)

	def form_valid(self, form):
		tour_order = form.save()	#Aqui esta el perfil como 'reservation_name'

		final_price = tour_order.quantity * tour_order.tour.price
		order_item = OrderItem(
			product = tour_order,
			price = final_price
		)
		order_item.save()

		order = Order.objects.filter(owner = tour_order.reservation_name)
		if len(order)>0:
			order.first().items.add(order_item)
		else:
			new_order = Order(
				reference_code = '123456789012',
				owner = tour_order.reservation_name
			)
			new_order.save()
			new_order.items.add(order_item)

		return super(ParticularOrder, self).form_valid(form)