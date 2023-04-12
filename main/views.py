from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
import re
import random
import smtplib

def signup(request):
	
	def validate_password(password):
	       regular_expression = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,1000}$"
	       pattern = re.compile(regular_expression)
	       valid = re.search(pattern, password)
	       return valid
		
		
	if request.method == "POST":
		username = request.POST.get("username")
		first_name = request.POST.get("first_name")
		last_name = request.POST.get("last_name")
		email = request.POST.get("email")
		password = request.POST.get("password")
		confirm_password = request.POST.get("confirm-password")
		
		valid_password = validate_password(password)
		
		#authentications
		if not User.objects.filter(username=username).exists():
			if not User.objects.filter(email=email).exists():
				if valid_password:
					if password == confirm_password:
							
						User.objects.create_user(
							username=username,
							email=email, 
							password=password)
						messages.info(request, f"account for {username} successfully created")
						
						return redirect("verification")
						
					else:
						messages.error(request, "both password must match")
				else:
						messages.error(request, "password should be a combination of  numbers, alphabets(upper and lower case ) and minimum length should be 8")
			else:
				messages.error(request, "email already exist!!")		
		else:
			messages.error(request, "username already exist!!")		
		
	return render(request, "signup.html")

		
def verification(request):
	
	def gen_code():
		num = "0123456789"
		code = random.choices(num, k=4)
		return code
		
	email = User.objects.get(email)

	code = gen_code()
		
	USER = "izzyjosh2@gmail.com"
	PASSWORD = "xloatbqmtumttwjk"
		
	server = smtplib.SMTP("smtp.gmail.com",  587)
	server.starttls()
	server.login(USER,  PASSWORD)

	server.sendmail(USER, email,  f"{code}")
						
						
	if request.method == "POST":
		verification1 = request.POST.get("verification-code1")
		verification2 = request.POST.get("verification-code2")
		verification3 = request.POST.get("verification-code3")
		verification4 = request.POST.get("verification-code4")
	
	if code == f"{verification1}{verification2}{verification3}{verification4}":
		return redirect("login")	
		
	return render(request, "verification.html")
	

def signin(request):
	if request.method == "POST":
		email = request.POST.get("email")
		password = request.POST.get("password")
		
		username = User.objects.filter(email=email).get().username
		user = auth.authenticate(username=username, password=password)
		
		if user is not None:
			auth.login(request, user)
			messages.info(request, "sigin successfully")
		else:
			messages.error(request, "Incorrect username or password")
			
	return render(request, "signin.html")
		
		
		