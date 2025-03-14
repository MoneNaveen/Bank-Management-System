from django.shortcuts import render,HttpResponse,redirect
from .models import Account
from .forms import AccountForm
from django.conf import settings
from django.core.mail import send_mail 
from django.core.mail import EmailMessage
from .forms import Recaptcha
# Create your views here.
def Home(request):
    
    return render(request,"index.html")

# profile
def Profile_creation(request):
    form = AccountForm()
    form2 = Recaptcha()
    if request.method == "POST":
        form = AccountForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("Successfully saved the form.")
            reciver_email = form.cleaned_data["email"]
            data = Account.objects.get(email=reciver_email)
            acc = data.Account_number

            try:
                send_mail(
                    "Thanks for registration",
                    f"Thank you for registring with our ProBank. we are excited to have you on board! your account number is {acc} ,\nthank you \nregards \n proBank manager ",
                    settings.EMAIL_HOST_USER,[reciver_email],fail_silently=False,
                )
                print("email sent")
                
            except Exception as e:
                return HttpResponse(f'Error sending email: {e}')
    context = {
        'form':form,
        'form2':form2
    }

    return render(request, "Profile.html", context)

# pin generation
def Pin_generation(request):
    if request.method == "POST":
        Acc_num = request.POST.get("account_number")
        mobile = request.POST.get("mobile")
        pin = int(request.POST.get("pin"))
        cpin = int(request.POST.get("cpin"))
        print(Acc_num,mobile,pin,cpin)
        try:
            account = Account.objects.get(Account_number = Acc_num)
        except:
            return HttpResponse("account not found in database")
        finally:
            print("exception is handled")
        if account.mobile == int(mobile):
            if pin == cpin:
                pin += 111
                # print(pin)
                account.pin = pin
                account.save()
                print("pin added")
                reciver_email = account.email
                try:
                    send_mail(
                    "Pin Generation Successful",
                    f"Thank you for pin generation. we are excited to have you on board! your account number is {account.Account_number} and pin {account.pin-111} ,\nthank you \nregards \n proBank manager ",
                    settings.EMAIL_HOST_USER,[reciver_email],fail_silently=False,
                    )
                    print("email sent")
                
                except Exception as e:
                    return HttpResponse(f'Error sending email: {e}')

                return redirect('Home')
            else:
                print("both pins are dont match")
    return render(request,"Pin_generation.html")

# balance
def Balance(request):
    flag = False
    bal = 0
    if request.method == 'POST':
        flag = True
        Acc = request.POST.get("account_number")
        pin = request.POST.get("pin")
        # print(Acc,pin)
        try:
            account = Account.objects.get(Account_number = Acc)
        except:
            return HttpResponse('Entered account number is not found')

        encpin = account.pin - 111
        # print(encpin)
        if int(pin) == int(encpin):
            print('PIN matched')
            bal = account.balance            
        else:
            return HttpResponse('Enter a Valid PIN')
    
    context = {
        'bal':bal,
        'flag':flag
    }
        
    return render(request,"Balance.html",context)

# deposit
def Deposit(request):
    if request.method == 'POST':
        Account_number = request.POST.get("account_number")
        mobile = request.POST.get("mobile")
        amount = request.POST.get("amount")
        # print(account_number,mobile,amount)
        try:
            account = Account.objects.get(Account_number = Account_number)
        except:
            return HttpResponse("account not found")
        finally:
            print("exception handled")
        if int(account.mobile) == int(mobile):
            print("account verified")
            if int(amount) >= 100 and int(amount) <= 50000:
                account.balance += int(amount)
                account.save()
                print('done')

                reciver_email = account.email
                try:
                    send_mail(
                        "Money Deposit Successful",
                        f"Dear ProBank User,your account is credited INR {amount},available balance INR {account.balance},\n thank you \n regards \n proBank manager ",
                        settings.EMAIL_HOST_USER,
                        [reciver_email],
                        fail_silently=False,
                    )
                    print("email sent")
                
                except Exception as e:
                    return HttpResponse(f'Error sending email: {e}')
                return redirect('Home')

            else:
                return HttpResponse("please enter the proper amount to deposit")
        else:
            return HttpResponse("enter the valid mobile number")
    return render(request,"Deposit.html")

# money transfer
def Money_transfer(request):
    if request.method == "POST":
        acc = request.POST["acc"]
        tacc = request.POST["tacc"]
        pin = request.POST["pin"]
        amt = request.POST["amt"]
        print(acc,tacc,amt,pin)
        try:
            account = Account.objects.get(Account_number = acc)
        except:
            return HttpResponse("account not found")
        finally:
            print("exception handled")
        try:
            to_account = Account.objects.get(Account_number = tacc)
        except:
            return HttpResponse("account not found")
        finally:
            print("exception handled")
        check_pin = account.pin - 111
        if int(check_pin) == int(pin):
            if int(account.balance) > int(amt):
                account.balance -= int(amt)
                to_account.balance += int(amt)
                account.save()
                to_account.save()

                reciver_email = account.email
                try:
                    send_mail(
                    "transaction Successful",
                    f"Dear ProBank User,Rs {amt} debited from A/C {account.Account_number} and credited to {to_account.Account_number} and available balance in your account INR {account.balance} ,\n thank you \n regards \n proBank manager ",
                    settings.EMAIL_HOST_USER,[reciver_email],fail_silently=False,
                    )
                    print("email sent")
                
                except Exception as e:
                    return HttpResponse(f'Error sending email: {e}')
                
                treciver_email = to_account.email
                try:
                    send_mail(
                    "Money Deposit Successful",
                    f"Dear ProBank User,your account is credited INR {amt} from {account.Account_number} ,available balance in your account {to_account.balance} ,\n thank you \n regards \n proBank manager ",
                    settings.EMAIL_HOST_USER,[treciver_email],fail_silently=False,
                    )
                    print("email sent")
                
                except Exception as e:
                    return HttpResponse(f'Error sending email: {e}')
            else:
                print("Not Enough balance")
        else:
            print("Incorrect PIN")
    return render(request,"Money_transfer.html")

# withdraw
def Withdrawl(request):
    if request.method == "POST":
        Acc_number = request.POST["account_number"]
        pin = request.POST["pin"]
        amount = request.POST["amount"]
        # print(Acc_number,pin,amount)
        try:
            account = Account.objects.get(Account_number = Acc_number)
        except:
            return HttpResponse("account not found")
        finally:
            print("exception is handled")
        check_pin = account.pin - 111
        # print(check_pin,pin)
        if int(check_pin) == int(pin):
            print("pin matched")
            if int(account.balance) >= int(amount) and int(amount)<=10000 and int(amount) >= 500:
                account.balance -= int(amount)
                account.save()

                reciver_email = account.email
                try:
                    send_mail(
                    "Money Withdraw Successful",
                    f"Dear ProBank User,your account is Debited INR {amount},available balance {account.balance} ,\n thank you \n regards \n proBank manager ",
                    settings.EMAIL_HOST_USER,[reciver_email],fail_silently=False,
                    )
                    print("email sent")
                
                except Exception as e:
                    return HttpResponse(f'Error sending email: {e}')
            else:
                return HttpResponse("please enter the valid amount")
        else:
            print("enter the valid pin")
    return render(request,"Money_withdrawl.html")

# otp 
