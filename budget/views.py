from django.shortcuts import render
from django.views.generic import View
from budget.models import Transaction
from django import forms
from django.shortcuts import redirect         #to return to the another page
from django.contrib.auth.models import User   #to get the user and password
from django.contrib.auth import authenticate,login,logout     #to check the user name and passwrod(authenticate)
from django.utils import timezone #to get the month and year
from django.db.models import Sum
from django.utils.decorators import method_decorator 
from django.contrib import messages  # for viewing the messages
from django.views.decorators.cache import never_cache

# Create your views here.

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper       

decs=[signin_required,never_cache]

class TransactionForm(forms.ModelForm):
    class Meta:
        model=Transaction
        exclude=("created_date","user")   #---to remove selected items
        # fields="__all__" ----to get all the fields of transaction models
        # fields=["fields of trasaction models","fields of trasaction models"]----to get selected items only

        widgets={
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "amount":forms.NumberInput(attrs={"class":"form-control"}),
            "type":forms.Select(attrs={"class":"form-control form-select"}),
            "category":forms.Select(attrs={"class":"form-control form-select"})
        }


# (1)----list the all trasantionview
        # method get 
        # url - l:8000/transaction/all/

@method_decorator(decs,name="dispatch")
class TransationView(View):
    def get(self,request,*args,**kwargs):
        qs=Transaction.objects.filter(user=request.user)
        cur_month=timezone.now().month
        cur_year=timezone.now().year
        data=Transaction.objects.filter(
            user=request.user,
            created_date__month=cur_month,
            created_date__year=cur_year
        ).values("type").annotate(type_sum=Sum("amount"))
        cat_qs=Transaction.objects.filter(
            user=request.user,
            created_date__month=cur_month,
            created_date__year=cur_year
        ).values("category").annotate(cat_sum=Sum("amount"))
        # print(cat_qs)
                # qs=Transaction.objects.filter(user=request.user)
        # cur_month=timezone.now().month    #to get the month
        # cur_year=timezone.now().year      #to get the year
        # print(cur_month,cur_year)
        # expence_total=Transaction.objects.filter(
        #     user=request.user,
        #     type="expense",
        #     created_date__month=cur_month,
        #     created_date__year=cur_year,
        # ).aggregate(Sum("amount"))
        # print(expence_total)
        # income_total=Transaction.objects.filter(
        #     user=request.user,
        #     type="income",
        #     created_date__month=cur_month,
        #     created_date__year=cur_year,
        # ).aggregate(Sum("amount"))
        # print(income_total)
        return render(request,"transaction_list.html",{"data":qs,"type_total":data,"cat_total":cat_qs})

#  (2)----View for creation transactionView()
    # url - l:8000/transaction/add/
    # method get,post
    
@method_decorator(decs,name="dispatch")

class TransactionCreateView(View):
    def get(self,request,*args,**kwargs):
        form=TransactionForm()
        return render(request,"transaction_add.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=TransactionForm(request.POST)
        if form.is_valid():
            # form.instance.user=request.user
            # form.save()
            data=form.cleaned_data
            Transaction.objects.create(**data,user=request.user)
            messages.success(request,"transaction added successfully")

            return redirect("transaction-list")
        else:
           messages.error(request,"transaction added invalid")

           return render(request,"transaction_add.html",{"form":form})


# Transaction detail view
# url- lh:8000/transactions/(id)/
# method get
        
@method_decorator(signin_required,name="dispatch")

class TransactionDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Transaction.objects.get(id=id)
        return render(request,"transaction_detail.html",{"data":qs})
    

# Transaction delete view
# url - lh:8000/transaction/remove/
# method get
@method_decorator(decs,name="dispatch")

class TransactionDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Transaction.objects.filter(id=id).delete()
        messages.success(request,"transaction deleted successfully")
        return redirect("transaction-list")
    

# Transaction update view
# url-lh:8000/transactions/update/
# method post & get
@method_decorator(decs,name="dispatch")
   
class TransactionUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        transaction_objects=Transaction.objects.get(id=id)
        form=TransactionForm(instance=transaction_objects)
        return render (request,"transaction_update.html",{"form":form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        transaction_objects=Transaction.objects.get(id=id)
        data=request.POST
        form=TransactionForm(data,instance=transaction_objects)
        if form.is_valid():
            form.save()
            messages.success(request,"transaction updated succesfully")

            return redirect("transaction-list")
        else:
         messages.error(request,"transaction updation failed")
         return render (request,"transaction_update.html",{"form":form})


# form for registration
class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","email","password"]
        widgets={
            "username":forms.TextInput(attrs={"class":"form-control"}),
             "email":forms.EmailInput(attrs={"class":"form-control"}),
            "password":forms.PasswordInput(attrs={"class":"form-control"}),

        }

class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"signup.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            # form.save()
            User.objects.create_user(**form.cleaned_data)#to encrypt password (create_user)
            # print("recode hase been saved")
            return redirect("signin")
        else:
             return render(request,"signup.html",{"form":form})


# sign in
# localhost/8000/
# method =get and post
        
class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))                                                      


class SigninView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"signin_1.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            userobject=authenticate(request,username=u_name,password=pwd)
            if userobject:
                login(request,userobject)
                # print("valid")
                return redirect("transaction-list")
        # print("invalid")
        return render(request,"signin_1.html",{"form":form})

@method_decorator(decs,name="dispatch")

class SignOut(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")