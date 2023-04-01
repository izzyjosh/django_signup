from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def signup(request):
	if request.method == "POST":
		username = request.POST.get("username")
		first_name = request.POST.get("first_name")
		last_name = request.POST.get("last_name")
		email = request.POST.get("email")
		password = request.POST.get("password")
		confirm_password = request.POST.get("confirm-password")
		
		if not User.objects.filter(username=username).exists():
			if not User.objects.filter(email=email).exists():
				if password == confirm_password:
					User.objects.create_user(
						username=username, 
						first_name=first_name, 
						last_name=last_name, 
						email=email, 
						password=password
						)
				else:
					messages.error(request, f"both password must be the same")
			else:
				messages.error(request, f"this email {email} already exist")
		else:
			messages.error(request, f"the username {username} already exist")
		return redirect("verification.html")
	return render(request, "signup.html")
		