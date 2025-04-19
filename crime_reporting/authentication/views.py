from django.shortcuts import render,redirect

from django.views import View

from .forms import LoginForm,RegisterForm

from django.contrib.auth import authenticate,logout,login

from .models import Profile


# Create your views here.


class LoginView(View):

    def get(self,request,*args,**kwargs):

        form = LoginForm()

        data = {'form':form}

        return render(request,'authentication/login.html',context=data)
    
    def post(self,request,*args,**kwargs):

        form = LoginForm(request.POST)

        error = None

        if form.is_valid():

            # username = form.cleaned_data.get('username')

            # password = form.cleaned_data.get('password')

            user = authenticate(**form.cleaned_data)

            if user:

                login(request,user)

                role = user.role

                if role in ['Admin']:

                    redirect_url ='dashboard'
                
                elif role in ['User']:

                    redirect_url ='dashboard'

                return redirect(redirect_url)    
            
            else:

                error = 'user does not exists '

                print(error)       
            
        data = {'form':form,'error':error}

        return render(request,'authentication/login.html',context=data)


class LogoutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect('login')
    

class RegisterView(View):

    def get(self,request,*args,**kwargs):

        form = RegisterForm()

        data = {'form':form}

        return render(request,'authentication/register.html',context=data)
 
    def post(self,request,*args,**kwargs):

        form = RegisterForm(request.POST,request.FILES)

        if form.is_valid():

            validated_data = form.cleaned_data.copy()

            validated_data['username']=validated_data['email']

            validated_data['role']='User'

            Profile.objects.create_user(**validated_data)

            return redirect('login')
        
        data = {'form':form}

        print(form.errors)

        return render(request,'authentication/register.html',context=data)    