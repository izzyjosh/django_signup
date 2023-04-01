from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
import re
import random
import smtplib

def signup(request):
	
	def gen_code():
		num = "0123456789"
		code = random.choices(num, k=4)
		return code
		
	
	def verify(password):
		reg_exp = "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[a-zA-Z0-9]{8, 1000}$"
		pattern = re.compile(reg_exp)
		valid = re.search(pattern, password)
		return valid
		
		
	if request.method == "POST":
		username = request.POST.get("username")
		first_name = request.POST.get("first_name")
		last_name = request.POST.get("last_name")
		email = request.POST.get("email")
		password = request.POST.get("password")
		confirm_password = request.POST.get("confirm-password")
		
		valid_password = verify(password)
		
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
						return redirect("signin")
					else:
						messages.error(request, "both password must match")
				else:
						messages.error(request, "password should be a combination of  numbers, alphabets(upper and lower case ) and minimum length should be 8")
			else:
				messages.error(request, "email already exist!!")		
		else:
			messages.error(request, "username already exist!!")
			
		code = gen_code()
		
		USER = "joshuajosephizzyjosh@gmail.com"
		PASSWORD = "xloatbqmtumttwjk"
		
		server = smtplib.SMTP("smtp.gmail.com",  587)
		server.starttls()
		server.login(USER,  PASSWORD)

		server.sendmail(
			USER, 
			email,  
			f"{code}"
		)
		return redirect("verification")
		
	return render(request, "signup.html")

		
def verification(request):
	return render(request, "verification.html")