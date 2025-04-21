from django.shortcuts import render,redirect

from .utility import send_email

from django.views import View
# Create your views here.

from .models import CrimeReports

from authentication.models import Profile

import threading

from .forms import CrimeRegisterForm

from django.contrib import messages

import json

from django.db.models import Q 


class DashboardView(View):

    def get(self,request,*args,**kwargs):

        return render(request,'reporting/dashboard.html')


class CrimeListView(View):

    def get(self,request,*args,**kwargs):

        query = request.GET.get('query')

        if request.user.role == 'User':

            crimes = CrimeReports.objects.filter(user=request.user).order_by('-id')

            if query:
            
                crimes = CrimeReports.objects.filter(Q(user=request.user)&(Q(location__icontains=query)|Q(description__icontains=query)|Q(type_of_crime__icontains=query)))
        
        elif request.user.role == 'Admin':

            crimes = CrimeReports.objects.all().order_by('-id')

            if query:
            
                crimes = CrimeReports.objects.filter(Q(user__first_name__icontains=query)|Q(user__last_name__icontains=query)|Q(location__icontains=query)|Q(description__icontains=query)|Q(type_of_crime__icontains=query))

        elif request.user.role == 'Police':

            crimes = CrimeReports.objects.filter(p_officer=request.user).order_by('-id')

            if query:
            
                crimes = CrimeReports.objects.filter(Q(p_officer=request.user)&(Q(location__icontains=query)|Q(description__icontains=query)|Q(type_of_crime__icontains=query)))        

        return render(request,'reporting/crime-list.html',context={'crimes':crimes,'query':query})

class CrimeDetailsView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        crime = CrimeReports.objects.get(uuid=uuid)

        police_officers = Profile.objects.filter(role='Police')

        return render(request,'reporting/crime-details.html',context={'crime':crime,'police_officers':police_officers})
    def post(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        crime = CrimeReports.objects.get(uuid=uuid)

        status = request.POST.get('status')

        p_officer_id = request.POST.get('p_officer_id')

        p_status = request.POST.get('p_status')

        if p_status:

            crime.p_status = p_status

            crime.save()

            title = 'Investigation Status Updated'
       

            message = f'Crime Report is {p_status}'

            data = {
                    'title': title,
                    'message': message
                    }
            messages.add_message(request, messages.INFO, json.dumps(data), extra_tags='json')

            recepient = crime.user.email
            template ='email/investigation-status.html'
            subject = 'Crime Report investigation Status'
            context = {'status':p_status,'crime':crime}
            # sending email
            thread = threading.Thread(target=send_email,args=(subject,recepient,template,context))

            thread.start()

            return redirect('crime-details',uuid=crime.uuid)


        if p_officer_id:

            p_officer = Profile.objects.get(id=int(p_officer_id))

            crime.p_officer = p_officer

            crime.save()

            return redirect('crime-details',uuid=crime.uuid)

        if status:

            crime.status = status

            crime.save()

            title = 'Status Updated'

            if status == 'Approve':

                sts = 'Approved'

            elif status == 'Reject':

                sts = 'Rejected' 

            elif status == 'Pending':

                sts = 'Pending'        

            message = f'Crime Report {sts}'

            data = {
                    'title': title,
                    'message': message
                    }
            messages.add_message(request, messages.INFO, json.dumps(data), extra_tags='json')

            recepient = crime.user.email
            template ='email/status.html'
            subject = 'Crime Report Status'
            context = {'status':sts,'crime':crime}
            # sending email
            thread = threading.Thread(target=send_email,args=(subject,recepient,template,context))

            thread.start()

            return redirect('crime-details',uuid=crime.uuid)
        
class CrimeRegisterView(View):

    def get(self,request,*args,**kwargs):

        form = CrimeRegisterForm()

        data = {'form':form}

        return render(request,'reporting/crime-register.html',context=data)

    def post(self,request,*args,**kwargs):

        form = CrimeRegisterForm(request.POST,request.FILES)

        if form.is_valid():

            crime=form.save(commit=False)

            crime.user = request.user

            crime.save()

            title = 'Crime Reporing'

            message = 'You are Reported a Crime Successfully'

            data = {
                    'title': title,
                    'message': message
                    }
            messages.add_message(request, messages.INFO, json.dumps(data), extra_tags='json')

            return redirect('crime-list')
        
        data = {'form':form}

        print(form.errors)

        return render(request,'reporting/crime-register.html',context=data)
        