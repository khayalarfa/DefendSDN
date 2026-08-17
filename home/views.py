from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import User_Data
from joblib import load
model = load('detection_model.sav')
# Create your views here.
def index(request):
    return render(request, 'index.html')
    #return HttpResponse("this is homepage")

@login_required(login_url='login')
def HomePage(request):
    # return render (request,'contact.html')
    if request.method == 'POST':

        Protocol= int(request.POST['Protocol'])
        FlowDuration= int(request.POST['FlowDuration'])
        FPLengthTotal= int(request.POST['FPLengthTotal'])
        # FPLengthMax= int(request.POST['FPLengthMax'])
        # FPLengthMin= int(request.POST['FPLengthMin'])
        # FPLengthMean= int(request.POST['FPLengthMean'])
        FPLengthMax= FPLengthTotal
        FPLengthMin= FPLengthTotal
        FPLengthMean= FPLengthTotal
        FlowBytesPers= int(request.POST['FlowBytesPers'])
        FlowPacketsPers= int(request.POST['FlowPacketsPers'])
        FwdIATTotal= int(request.POST['FwdIATTotal'])
        FwdPacketsPers= FlowPacketsPers
        # PacketLengthMin= int(request.POST['PacketLengthMin'])
        # PacketLengthMax= int(request.POST['PacketLengthMax'])
        PacketLengthMean= int(request.POST['PacketLengthMean'])
        PacketLengthMin= PacketLengthMean
        PacketLengthMax= PacketLengthMean
        ACKFlagCount= 0
        AvgPacketSize= int(request.POST['AvgPacketSize'])
        AvgFwdSegmentSize= int(request.POST['AvgFwdSegmentSize'])
        SubflowFwdBytes= FPLengthTotal
        Label= 0
        SourceIP= int(request.POST['SourceIP'])

        # Save the data to the UserData model
        User_Data.objects.create(
        Protocol=Protocol,
        FlowDuration= FlowDuration,
        FPLengthTotal= FPLengthTotal,
        FlowBytesPers= FlowBytesPers,
        FlowPacketsPers= FlowPacketsPers,
        FwdIATTotal= FwdIATTotal,
        PacketLengthMean= PacketLengthMean,
        AvgPacketSize= AvgPacketSize,
        AvgFwdSegmentSize= AvgFwdSegmentSize,
        SourceIP= SourceIP
        )


        lis=[]
        lis.append(Protocol)
        lis.append(FlowDuration)
        lis.append(FPLengthTotal)
        lis.append(FPLengthMin)
        lis.append(FPLengthMax)
        lis.append(FPLengthMean)
        lis.append(FlowBytesPers)
        lis.append(FlowPacketsPers)
        lis.append(FwdIATTotal)
        lis.append(FwdPacketsPers)
        lis.append(PacketLengthMin)
        lis.append(PacketLengthMax)
        lis.append(PacketLengthMean)
        lis.append(ACKFlagCount)
        lis.append(AvgPacketSize)
        lis.append(AvgFwdSegmentSize)
        lis.append(SubflowFwdBytes)
        lis.append(Label)

        print(lis)
        # y_pred = model.predict([[Protocol, FlowDuration, FPLengthTotal, FPLengthMax, FPLengthMin, FPLengthMean, FlowBytesPers,FlowPacketsPers , FwdIATTotal, FwdPacketsPers, PacketLengthMin, PacketLengthMax , PacketLengthMean, ACKFlagCount, AvgPacketSize,AvgFwdSegmentSize , SubflowFwdBytes, Label]])
        y_pred = model.predict([lis])
        # y_pred=1
        print(y_pred)
        # if y_pred == 0:
        #      y_pred = 'ATTACK'
        # elif y_pred == 1:
        #      y_pred = 'BENIGN'
        if y_pred == [0]:
             y_pred = 0
        elif y_pred == [1]:
             y_pred = 1
        # Pass both values to the template context
        context = {'SourceIP': SourceIP, 'result': y_pred}
        return render(request, 'contact.html', context)
    return render(request, 'contact.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('contact')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def Contact(request):
    return render(request, 'contact.html')