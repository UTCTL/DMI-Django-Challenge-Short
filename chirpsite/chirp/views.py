from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from chirp.forms import RegistrationForm, LoginForm
from chirp.models import Chirper
from django.contrib.auth import authenticate, login, logout

def ChirperRegistration(request):
	if(request.user.is_authenticated()):
		return HttpResponseRedirect('/profile/')
	if(request.method == 'POST'):
		form = RegistrationForm(request.POST)
		if(form.is_valid()):
			user = User.objects.create_user(username = form.cleaned_data['username'], email = form.cleaned_data['email'], password = form.cleaned_data['password'])
			user.save()
			# chirper = user.get_profile()
			# chirper.name = form.cleaned_data['name']
			chirper = Chirper(user = user, name = form.cleaned_data['name'])
			chirper.save()
			return HttpResponseRedirect('/profile/')
		else:
			return render_to_response('chirp/register.html', {'form':form}, context_instance=RequestContext(request))
	else:
		""" Display blank registration form if user isn't submitting the form """
		form = RegistrationForm()
		context = {'form' : form}
		return render_to_response('chirp/register.html', context, context_instance=RequestContext(request))
		
def LoginRequest(request):
	if(request.user.is_authenticated()):
		return HttpResponseRedirect('/profile/')
	if(request.method == 'POST'):
		form = LoginForm(request.POST)
		if(form.is_valid()):
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			chirper = authenticate(username=username, password=password)
			if(chirper is not None):
				login(request, chirper)
				return HttpResponseRedirect('/profile/')
			else:
				return render_to_response('chirp/login.html', {'form' : form}, context_instance = RequestContext(request))
		else:
			return render_to_response('chirp/login.html', {'form' : form}, context_instance = RequestContext(request))
			
	else:
		""" Display blank login form if user isn't submitting the form """
		form = LoginForm()
		context = {'form' : form}
		return render_to_response('chirp/login.html', context, context_instance=RequestContext(request))
		
def LogoutRequest(request):
	logout(request)
	return HttpResponseRedirect('/login/')