from django.shortcuts import render,redirect
from .models import*
from django.contrib import messages
from django.contrib.auth import authenticate
from django.utils import timezone
from django.db.models import Q

# Create your views here.

def index(request):
    return render(request,"index.html")

def ngoReg(request):
    msg=''
    if request.POST:
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        password=request.POST['pass']
        photo = request.FILES['photo']
        lisence = request.FILES['lisence']
        address=request.POST['address']
        try:
            cust=Logintbl.objects.create_user(username=email,password=password,is_active=0,usertype="ngo")
            cust.save()
            user=Ngo.objects.create(name=name,email=email,phone=phone,lisence=lisence,logo=photo,address=address,user=cust)
            user.save()
            msg="Registration Successfull.."
            return render(request,"ngoReg.html",{"msg":msg})
        except:
            msg="Username Already Exists.."
            return render(request,"ngoReg.html",{"msg":msg})
    else:
        return render(request,"ngoReg.html",{"msg":msg})

def volReg(request):
    msg=''
    if request.POST:
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        password=request.POST['pass']
        cv = request.FILES['cv']
        photo = request.FILES['photo']
        address=request.POST['address']
        try:
            cust=Logintbl.objects.create_user(username=email,password=password,is_active=1,usertype="volunteer")
            cust.save()
            user=Volunteer.objects.create(name=name,email=email,phone=phone,photo=photo,cv=cv,address=address,user=cust)
            user.save()
            msg="Registration Successfull.."
            return render(request,"volReg.html",{"msg":msg})
        except:
            msg="Username Already Exists.."
            return render(request,"volReg.html",{"msg":msg})
    else:
        return render(request,"volReg.html",{"msg":msg})

def donReg(request):
    msg=''
    if request.POST:
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        password=request.POST['pass']
        address=request.POST['address']
        photo = request.FILES['photo']
        try:
            cust=Logintbl.objects.create_user(username=email,password=password,is_active=1,usertype="donor")
            cust.save()
            user=Donor.objects.create(name=name,email=email,phone=phone,photo=photo,address=address,user=cust)
            user.save()
            msg="Registration Successfull.."
            return render(request,"donReg.html",{"msg":msg})
        except:
            msg="Username Already Exists.."
            return render(request,"donReg.html",{"msg":msg})
    else:
        return render(request,"donReg.html",{"msg":msg})

def login(request):
    msg=''
    if request.POST:
        email=request.POST['email']
        password=request.POST['pass']
        user=authenticate(username=email,password=password)
        if user is not None:
            if user.is_superuser:
                return redirect("/adminHome")
            elif user.usertype == 'ngo':
                data=Ngo.objects.get(email=email)
                request.session['id'] = data.id
                return redirect("/ngoHome")
            elif user.usertype == 'volunteer':
                data=Volunteer.objects.get(email=email)
                if data:
                    request.session['id'] = data.id
                    return redirect("/volunteerHome")
            elif user.usertype == 'donor':
                data=Donor.objects.get(email=email)
                request.session['id'] = data.id
                return redirect("/donorHome")
        else:
            msg="Invalid Username or Password"
            return render(request,"login.html",{"msg":msg})
    else:
         return render(request,"login.html",{"msg":msg})
    


def blog(request):
    blogs = Blog.objects.filter().order_by('-id')
    return render(request,"blog.html",{"blogs":blogs})
    
def adminHome(request):
    return render(request,"adminHome.html")
    
def adminngo(request):
    ngos = Ngo.objects.all().order_by('-id')
    return render(request,"adminngo.html", {"ngos": ngos})

def adminActive(request):
    id=request.GET['id']
    status=request.GET['status']
    data=Logintbl.objects.get(id=id)
    data.is_active=status
    data.save()        
    return redirect("/adminngo")

def adminActiveVol(request):
    id=request.GET['id']
    status=request.GET['status']
    data=Logintbl.objects.get(id=id)
    data.is_active=status
    data.save()        
    return redirect("/adminvol")

def adminActiveDon(request):
    id=request.GET['id']
    status=request.GET['status']
    data=Logintbl.objects.get(id=id)
    data.is_active=status
    data.save()        
    return redirect("/admindon")
    
def adminvol(request):
    vol = Volunteer.objects.all().order_by('-id')
    return render(request,"adminvol.html", {"vol": vol})
    
def admindon(request):
    don = Donor.objects.all().order_by('-id')
    return render(request,"admindon.html", {"don": don})

def adminOpen(request):
    file=request.GET['file']
    return render(request,"adminOpen.html",{"file":file})

def adminActivity(request):
    activity=Activity.objects.filter().order_by('-id')
    return render(request,"adminActivity.html", {"activity": activity})
    
def adminActVol(request):
    id = request.GET['id']
    activity = Activity.objects.get(id=id)
    req = VolunteerActivity.objects.filter(activity=activity).order_by('-id')
    return render(request,"adminActVol.html", {"req": req})
    
def adminActDon(request):
    id = request.GET['id']
    activity = Activity.objects.get(id=id)
    req = Donations.objects.filter(activity=activity).order_by('-id')
    return render(request,"adminActDon.html", {"req": req})
    

def adminChat(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        answer = request.POST.get('answer', '')
        chat=ChatbotQA.objects.create(keyword=keyword, answer=answer)
        chat.save()
        messages.success(request, "Response added successfully.")
        return redirect("/adminChat")
    return render(request,"adminChat.html")



def adminBlog(request):
    blogs=Blog.objects.filter().order_by("-id")
    return render(request,"adminBlog.html",{"blogs":blogs})

# def adminReport(request):
#     data=Donations.objects.filter().order_by('-id')
#     return render(request,"adminReport.html",{"data":data})


from django.shortcuts import render
from .models import Donations
from django.db.models import Sum
from datetime import datetime

def adminReport(request):
    selected_month = request.GET.get('month')
    data = Donations.objects.all().order_by('-id')
    error = None

    if selected_month:
        try:
            year, month = map(int, selected_month.split('-'))
            data = data.filter(date__year=year, date__month=month)
        except ValueError:
            error = "Invalid month format."

    # Calculate totals
    total_amount = data.aggregate(Sum('amount'))['amount__sum'] or 0
    total_ngodon = data.aggregate(Sum('ngodon'))['ngodon__sum'] or 0
    total_fee = data.aggregate(Sum('fee'))['fee__sum'] or 0

    context = {
        'data': data,
        'selected_month': selected_month or '',
        'total_amount': total_amount,
        'total_ngodon': total_ngodon,
        'total_fee': total_fee,
        'error': error
    }

    return render(request, "adminReport.html", context)



def blogDelet(request):
    id=request.GET['bid']
    blog=Blog.objects.get(id=id)
    blog.delete()
    return redirect("/adminBlog")

def ngoHome(request):
    uid=request.session['id']
    ngo = Ngo.objects.get(id=uid)
    name = ngo.name
    return render(request,"ngoHome.html",{"name": name})
    
def ngoActivity(request):
    uid=request.session['id']
    ngo = Ngo.objects.get(id=uid)

    activity = Activity.objects.filter(ngo=ngo).order_by('-id')

    email = ngo.email
    phone = ngo.phone

    if request.POST:
        name = request.POST['name']
        category = request.POST['category']
        description = request.POST['description']
        loc = request.POST['loc']
        volunteers_needed = request.POST['volunteers_needed']
        sDate = request.POST['sDate']
        eDate = request.POST['eDate']

        activity = Activity.objects.create(
            ngo=ngo,
            name=name,
            category=category,
            description=description,
            loc=loc,
            volunteers_needed=volunteers_needed,
            sDate=sDate,
            eDate=eDate
        )
        activity.save()
        messages.success(request, "Activity created successfully.")
        return redirect("/ngoActivity")
    return render(request,"ngoActivity.html",{"email": email, "phone": phone, "activity": activity})

def ngoVolRequest(request):
    uid = request.session['id']
    ngo = Ngo.objects.get(id=uid)
    
    id = request.GET['id']
    activity = Activity.objects.get(id=id)
    req = VolunteerActivity.objects.filter(activity=activity).order_by('-id')
    return render(request,"ngoVolRequest.html",{"req": req, "id":id})

def ngoAcceptVol(request):
    uid = request.session['id']
    id = request.GET['did']
    did = request.GET['id']
    status = request.GET['status']
    req = VolunteerActivity.objects.get(id=did)
    req.status = status
    if status == "Accepted":
        req.activity.volunteers_needed -= 1
    req.save()
    req.activity.save()
    return redirect(f"/ngoVolRequest?id={id}")

def ngoDonations(request):
    uid = request.session['id']
    ngo = Ngo.objects.get(id=uid)   

    id = request.GET.get('id')
    don=Donations.objects.filter(activity_id=id).order_by('-id')
    return render(request,"ngoDonations.html",{"req":don})
   
# def ngoBlog(request):
#     uid=request.session['id']
#     ngo = Ngo.objects.get(id=uid)  
#     blogs=Blog.objects.filter(ngo=ngo)
#     blog=Image.objects.filter(blog=blogs).order_by("-id")
#     if request.POST:
#         title=request.POST['title']
#         description=request.POST['description']
#         images = request.FILES.getlist('image')

#         blog=Blog.objects.create(title=title,description=description,ngo=ngo)
#         blog.save()
#         for image in images:
#                     Image.objects.create(blog=blog, image=image)
#         messages.success(request,"Blog Added Successfully!")
#         return redirect("/ngoBlog")

#     return render(request,"ngoBlog.html",{"blog":blog})


def ngoBlog(request):
    # Ensure user is logged in
    if 'id' not in request.session:
        return redirect('/login')  # adjust based on your login URL

    uid = request.session['id']
    ngo = Ngo.objects.get(id=uid)

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        images = request.FILES.getlist('image')

        # Create the blog post
        blog = Blog.objects.create(title=title, description=description, ngo=ngo)

        # Save all uploaded images
        for image in images:
            Image.objects.create(blog=blog, image=image)

        messages.success(request, "Blog Added Successfully!")
        return redirect("/ngoBlog")

    # Fetch all blogs by the logged-in NGO
    blogs = Blog.objects.filter(ngo=ngo).order_by('-id')

    return render(request, "ngoBlog.html", {"blogs": blogs})


    
def volunteerHome(request):
    uid=request.session['id']
    vol = Volunteer.objects.get(id=uid)
    name=vol.name
    return render(request,"volunteerHome.html",{"name": name})
    
def volActivity(request):
    uid = request.session['id']

    activty=Activity.objects.filter().order_by('-id')
    vol = Volunteer.objects.get(id=uid)
    req = VolunteerActivity.objects.filter(volunteer=vol).order_by('id')
    subscribed = Subscribe.objects.filter(vol=vol,status="yes").values_list('ngo', flat=True)
    today = timezone.now().date()
    for i in activty:
        if i.id in req.values_list('activity_id', flat=True):
            i.flag = 1
        else:
            i.flag = 0

    if request.POST:
        song = request.POST["txtSearch"]
        activty = Activity.objects.filter(Q(name__contains=song) | Q(category__contains=song) | Q(loc__contains=song) ).order_by("-id")
        return render(request, "volActivity.html", {"activity": activty})
    else:
        return render(request,"volActivity.html",{"activity": activty, "vol": vol, "req": req, "subscribed": subscribed,"today":today})

def volRequest(request):
    uid = request.session['id']
    vol = Volunteer.objects.get(id=uid)

    id = request.GET['id']
    activity = Activity.objects.get(id=id)
    req= VolunteerActivity.objects.create(
        volunteer=vol,
        activity=activity
    )
    req.save()
    messages.success(request, "Request sent successfully.")
    return redirect("/volActivity")
    
def volApplied(request):
    uid=request.session['id']
    act= VolunteerActivity.objects.filter(volunteer=uid).order_by('-id')
    return render(request,"volApplied.html",{"act": act})
    
def VolSubscribe(request):
    uid = request.session['id']
    vol = Volunteer.objects.get(id=uid)

    ngoid = request.GET.get('ngo')
    ngo=Ngo.objects.get(id=ngoid)
    sts=request.GET.get('sts')
    sub = Subscribe.objects.filter(ngo=ngo, vol=vol).first()
    if sub:
        if sts == "yes":
            sub = Subscribe.objects.filter(ngo=ngo, vol=vol).first()
            print(sub,"###########################################################")
            if sub:
                sub.status = sts
                sub.save()

        elif sts == "no":
            sub = Subscribe.objects.filter(ngo=ngo, vol=vol).first()
            print(sub,"###########################################################")
            if sub:
                sub.status = sts
                sub.save()
    else:
        sub=Subscribe.objects.create(ngo=ngo, vol=vol, status=sts)
        sub.save()
    return redirect("/volActivity")
    
   
def volChat(request):
    return render(request,"volChat.html")

from django.http import JsonResponse
from .models import ChatbotQA

def chatbot_response(request):
    query = request.GET.get('query', '').lower()

    if query:
        all_entries = ChatbotQA.objects.all()

        for entry in all_entries:
            keywords = [k.strip().lower() for k in entry.keyword.split(',')]
            for keyword in keywords:
                if keyword in query:
                    return JsonResponse({'response': entry.answer})

    return JsonResponse({'response': "Sorry, I couldn't understand that. Can you please rephrase?"})

    


# def volSub(request):
#     uid=request.session['id']
#     vol=Volunteer.objects.get(id=uid)
#     sub=Subscribe.objects.filter(vol=vol).order_by("-id")
#     return render(request,"volSub.html")

# def volSub(request):
#     uid = request.session['id']
#     vol = Volunteer.objects.get(id=uid)
#     activities =Subscribe.objects.filter(vol=vol).order_by("-id")
    

#     return render(request, "volSub.html", {"activities": activities})


# def volSub(request):
#     uid = request.session['id']
#     vol = Volunteer.objects.get(id=uid)

#     # Get unique NGOs the volunteer is subscribed to
#     unique_ngos = Subscribe.objects.filter(vol=vol).values('ngo').distinct()

#     # Optional: If you need the actual NGO objects:
#     ngo_ids = [entry['ngo'] for entry in unique_ngos]
#     ngos = Ngo.objects.filter(id__in=ngo_ids)

#     activities=Activity.objects.filter(ngo=ngos)

#     return render(request, "volSub.html", {"activities": activities})



# def volSub(request):
#     uid = request.session['id']
#     vol = Volunteer.objects.get(id=uid)

#     unique_ngos = Subscribe.objects.filter(vol=vol, status="yes").values('ngo').distinct()
#     ngo_ids = [entry['ngo'] for entry in unique_ngos]
#     ngos = Ngo.objects.filter(id__in=ngo_ids)

#     activities = Activity.objects.filter(ngo__in=ngos).order_by('-id')

#     return render(request, "volSub.html", {"activities": activities})


def volSub(request):
    uid = request.session['id']
    vol = Volunteer.objects.get(id=uid)

    # Get distinct NGO IDs the volunteer is subscribed to with status "yes"
    ngo_ids = Subscribe.objects.filter(vol=vol, status="yes").values_list('ngo', flat=True).distinct()

    # Fetch activities posted by those NGOs
    activities = Activity.objects.filter(ngo_id__in=ngo_ids).order_by('-id')

    return render(request, "volSub.html", {"activities": activities})

def donSub(request):
    uid = request.session['id']
    don = Donor.objects.get(id=uid)

    # Get distinct NGO IDs the volunteer is subscribed to with status "yes"
    ngo_ids = Subscribe.objects.filter(don=don, status="yes").values_list('ngo', flat=True).distinct()

    # Fetch activities posted by those NGOs
    activities = Activity.objects.filter(ngo_id__in=ngo_ids).order_by('-id')

    return render(request, "donSub.html", {"activities": activities})




def donorHome(request):
    uid=request.session['id']
    don = Donor.objects.get(id=uid)     
    name = don.name
    return render(request,"donorHome.html",{"name": name})



def donEvents(request):
    uid = request.session['id']
    don = Donor.objects.get(id=uid)
    activty = Activity.objects.all().order_by('-id')
    subscribed = Subscribe.objects.filter(don=don, status="yes").values_list('ngo', flat=True)
    today = timezone.now().date()
    if request.POST:
        song = request.POST["txtSearch"]
        activty = Activity.objects.filter(Q(name__contains=song) | Q(category__contains=song) | Q(loc__contains=song) ).order_by("-id")
        return render(request, "donEvents.html", {"activity": activty})
    else:
        return render(request, "donEvents.html", {"activity": activty,"subscribed": subscribed,"today": today})

       
# def donEvents(request):
#     uid = request.session['id']
#     don = Donor.objects.get(id=uid)
#     activty=Activity.objects.filter().order_by('id')
#     subscribed = Subscribe.objects.filter(don = don,status="yes").values_list('ngo', flat=True)
#     return render(request,"donEvents.html",{"activity": activty, "subscribed": subscribed})


def DonSubscribe(request):
    uid = request.session['id']
    don = Donor.objects.get(id=uid)

    ngoid = request.GET.get('ngo')
    ngo=Ngo.objects.get(id=ngoid)
    sts=request.GET.get('sts')
    sub = Subscribe.objects.filter(ngo=ngo, don=don).first()
    if sub:
        if sts == "yes":
            sub = Subscribe.objects.filter(ngo=ngo, don=don).first()
            print(sub,"###########################################################")
            if sub:
                sub.status = sts
                sub.save()

        elif sts == "no":
            sub = Subscribe.objects.filter(ngo=ngo, don=don).first()
            print(sub,"###########################################################")
            if sub:
                sub.status = sts
                sub.save()
    else:
        sub=Subscribe.objects.create(ngo=ngo, don=don, status=sts)
        sub.save()
    return redirect("/donEvents")


def donConfirm(request):
    uid=request.session['id']
    don = Donor.objects.get(id=uid)
    eid=request.GET['id']
    if request.POST:
        activity_id = request.POST['activity_id']
        activity = Activity.objects.get(id=activity_id)
        amount = request.POST['amount']
        return redirect(f"/payment?amt={amount}&activity={activity_id}")
    return render(request,"donConfirm.html",{"id": eid})
 
def payment(request):
    uid=request.session['id']
    donor= Donor.objects.get(id=uid)
    if request.GET:
        amount = request.GET.get('amt')
        
        actibity_id = request.GET.get('activity')
        activity = Activity.objects.get(id=actibity_id)
    if request.POST:
        
        if int(amount)>1000:
            dona=int(amount)-15
            fee=15
        elif int(amount)>500:
            dona=int(amount)-10
            fee=10
        else:
            dona=amount
            fee=0
        donation=Donations.objects.create(donor=donor, activity=activity, amount=amount, ngodon=dona, fee=fee)
        donation.save()
        messages.success(request, "Donation successful.")
        return redirect("/donEvents")
        

    return render(request,"payment.html",{"amount": amount})

def donHistory(request):
    uid= request.session['id']
    don = Donor.objects.get(id=uid)
    donations = Donations.objects.filter(donor=don).order_by('-id')
    return render(request,"donHistory.html",{"donations": donations})

def donReciept(request):
    uid = request.session['id']
    don = Donor.objects.get(id=uid)
    donation_id = request.GET.get('id')
    donation = Donations.objects.get(id=donation_id)
    return render(request,"donReciept.html",{"donation": donation, "donor": don})