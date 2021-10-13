from django.shortcuts import render

# Create your views here.
def chat(request):

	username = request.session['customer']['username']

	context = {
		'username': username
	}

	return render(request, 'chat.html', context)