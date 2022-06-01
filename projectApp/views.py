from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from .forms import *
from datetime import datetime as dt
import uuid
import math
from django.http import HttpResponse
import json
from .filters import *


def main(request):#present main screen
    context = {}
    temp = dt.today().strftime('%Y-%m-%d')
    context['today'] = dt.strptime(temp, "%Y-%m-%d").strftime("%A %d %B")
    if 'date' in request.GET:
        if request.GET['date'] != "":
            temp = request.GET['date']
            converted_date = dt.strptime(request.GET['date'], "%Y-%m-%d").strftime("%A %d %B")
            context['date'] = converted_date
        else:
            converted_date = dt.strptime(temp, "%Y-%m-%d").strftime("%A %d %B")
            context['date'] = converted_date
    else:
        converted_date = dt.strptime(temp, "%Y-%m-%d").strftime("%A %d %B")
        context['date'] = converted_date
    show_list = Show.objects.filter(date=temp)
    if show_list.exists() == False: #if no showing are available.
        context['none'] = "There are no showings on this date!"
    if 'show' in request.GET:
        temp = request.GET['show']
        request.session['showId'] = temp
        return redirect('guestSelectTickets') #redirect once show is picked
    context['show_list'] = show_list
    return render(request, "main.html", context)

@transaction.atomic
@login_required()
def cinemaManagerDash(request):
    # filter out post request.
    if request.method == "POST":
        # Student club registration form processing
        if 'StudentClubFormSubmit' in request.POST:
            # get user input values
            club_form = StudentClubForm(request.POST or None)
            # validate the entered values
            if club_form.is_valid():
                # save the entered values if correct
                club_form.save()
                messages.success(request, "Registration successful.")
                return redirect('cinemaManagerDash')
            else:
                errors = club_form.errors
                return HttpResponse(json.dumps(errors), status=400)
        # Student club representative form processing
        elif 'ClubRepresentativeFormSubmit' in request.POST:
            # get user input values
            club_rep_form = ClubRepresentativeForm(request.POST or None)
            # validate the entered values
            if club_rep_form.is_valid():
                # save the entered values if correct
                club_rep_form.save()
                messages.success(request, "Club Representative registration successful!")
                return redirect('cinemaManagerDash')
            else:
                errors = club_rep_form.errors
                return HttpResponse(json.dumps(errors), status=400)
        # film form processing
        elif 'FilmFormSubmit' in request.POST:
            # get user input values
            film_form = FilmForm(request.POST or None)
            # validate the entered values
            if film_form.is_valid():
                # save the entered values if correct
                film_form.save()
                messages.success(request, "Film added successfully!")
                return redirect('cinemaManagerDash')
            else:
                errors = film_form.errors
                return HttpResponse(json.dumps(errors), status=400)
        # Add Screen form processing
        elif 'ScreenFormSubmit' in request.POST:
            # get user input values
            screen_form = ScreenForm(request.POST or None)
            # validate the entered values
            if screen_form.is_valid():
                # save the entered values if correct
                screen_form.save()
                messages.success(request, "Screen added successfully!")
                return redirect('cinemaManagerDash')
            else:
                errors = screen_form.errors
                return HttpResponse(json.dumps(errors), status=400)
        # Add show form processing
        elif 'ShowFormSubmit' in request.POST:
            # get user input values
            show_form = ShowForm(request.POST or None)
            if show_form.is_valid():
                # save the entered values if correct
                show_form.save()
                messages.success(request, "Show added successfully!")
                return redirect('cinemaManagerDash')
            else:
                errors = show_form.errors
                return HttpResponse(json.dumps(errors), status=400)
        elif 'DeleteShowFormSubmit' in request.POST:
            try:
                record = Show.objects.get(film__id=int(request.POST['film']))
                record.delete()
                messages.success(request, "Show deleted successfully!")
                return redirect('cinemaManagerDash')
            except:
                print("Record doesn't exists")
    # Loading all forms for get request
    return render(request, 'studentClub.html', {
        'StudentClubForm': StudentClubForm,
        'ClubRepresentativeForm': ClubRepresentativeForm,
        'FilmForm': FilmForm,
        'ScreenForm': ScreenForm,
        'ShowForm': ShowForm,
    })

@transaction.atomic
@login_required(login_url='login')
def clubRepresentative(request):
    # filter out post request.
    if request.method == "POST":
        # Student club registration form processing
        club_rep_form = ClubRepresentativeForm(request.POST or None)
        # validate the entered values
        if club_rep_form.is_valid():
            # save the entered values if correct
            club_rep_form.save()
            messages.success(request, "Club Representative registration successful!")
            return redirect('clubRepresentative')
        else:
            errors = club_rep_form.errors
            return HttpResponse(json.dumps(errors), status=400)

    return render(request, 'clubRepresentative.html', {
        'ClubRepresentativeForm': ClubRepresentativeForm(),
    })


@transaction.atomic
@login_required(login_url='login')
def addfilm(request):
    # filter out post request.
    if request.method == "POST":
        # Student club registration form processing
        film_form = FilmForm(request.POST or None)
        # validate the entered values
        if film_form.is_valid():
            # save the entered values if correct
            film_form.save()
            messages.success(request, "Film added successfully!")
            return redirect('addfilm')
        else:
            errors = film_form.errors
            return HttpResponse(json.dumps(errors), status=400)
    return render(request, 'addFilm.html', {
        'FilmForm': FilmForm
    })


@transaction.atomic
@login_required(login_url='login')
def addScreen(request):
    # filter out post request.
    if request.method == "POST":
        # Student club registration form processing
        screen_form = ScreenForm(request.POST or None)
        # validate the entered values
        if screen_form.is_valid():
            # save the entered values if correct
            screen_form.save()
            messages.success(request, "Screen added successfully!")
            return redirect('dashboard')
        else:
            errors = screen_form.errors
            return HttpResponse(json.dumps(errors), status=400)
    # Student club representative form processing
    return render(request, 'addScreen.html', {
        'ScreenForm': ScreenForm,
    })


@transaction.atomic
@login_required(login_url='login')
def addShow(request):
    context = {}
    # filter out post request.
    if request.method == "POST":
        form = ShowForm(request.POST or None)
        showId = request.session['showId']
        showing = Show.objects.get(id = showId)
        film = Film.objects.get(id = showing.film_id)
        screen = Screen.objects.get(id = showing.screen_id)
        if form.is_valid():
            context = {
            'film': film,
            'screen': screen,
            'selected_showing': showing
        }
            # save the entered values if correct
            form.save()
            messages.success(request, "Show added successfully!")
            return redirect('addShow')
        else:
            errors = form.errors
            return HttpResponse(json.dumps(errors), status=400)

    #context['form'] = form
    show_list = Show.objects.all()
    if show_list.exists() == False:
        context['none'] = "No showings exist."
    if 'show' in request.GET:
         temp = request.GET['show']
         request.session['showId'] = temp
         return redirect('addShow')
    context['showings_list'] = show_list
    return render(request, 'addShow.html', {
        'ShowForm': ShowForm,
        'changeTicketPricesForm' : changeTicketPricesForm
    })

def guestSelectTickets(request):
    context = {}

    if 'showId' not in request.session: #if no show id redirect to main
        return redirect('/')
    temp = request.session['showId']    
    show = Show.objects.get(id = temp)
    film = Film.objects.get(id = show.film_id)    
    
    context['film'] = film
    context['show'] = show
    context['duration'] = film.duration

    form = custTicketQuantityForm(request.POST or None) # call ticketquantity form

    if request.method == "POST":
        if form.is_valid():
            instance = form.save(commit=False)
            instance.show = show
            instance.save()
            booking = Booking.objects.latest('id')
            request.session['bookingId'] = booking.id
            request.session['showId'] = show.id # assign
            return redirect('/guestPurchaseTickets')

    context['form'] = custTicketQuantityForm()
    return render(request, "guestSelectTickets.html", context)

def guestPurchaseTickets(request): #show prices based on quantity of tickets
    context = {}

    if 'showId' not in request.session:
        return redirect('main')

    booking = Booking.objects.get(id = request.session['bookingId'])
    show = Show.objects.get(id = request.session['showId'])
    child_total = booking.childQty * show.child_price  #child qty * the price of a child ticket
    adult_total = booking.adultQty * show.adult_price
    student_total = booking.studentQty * show.student_price
    total_price = adult_total + student_total + child_total
    context = {
        'child_total': "£{:,.2f}".format(child_total),
        'adult_total': "£{:,.2f}".format(adult_total),
        'student_total': "£{:,.2f}".format(student_total),
        'total_price': "£{:,.2f}".format(total_price),
        'adult_price': "£{:,.2f}".format(show.adult_price),
        'student_price': "£{:,.2f}".format(show.student_price),
        'child_price': "£{:,.2f}".format(show.child_price),
        'booking': booking,
        'show': show
    }

    if request.GET.get('advance') == 'Advance':
        return redirect('/guestMakePayment') #redirect to next page

    return render(request, "guestPurchaseTickets.html", context)

@login_required(login_url='login')

@transaction.atomic
@login_required(login_url='login')
def repRequestDiscount(request):
    context = {}
    user = request.user
    rep = ClubRepresentative.objects.get(userid = user.id)
    account = Account.objects.get(club_id = rep.club_id)
    context['currentDiscount'] = account.discountRate
    if account.requestedRate is None:
        form = requestDiscountForm(request.POST or None, instance=account)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                return redirect('repRequestDiscount')
        context['form'] = form
    else:
        context['existing'] = "existing"
    return render(request, "repRequestDiscount.html", context)

@transaction.atomic
@login_required(login_url='login')
def studentRequestDiscount(request):
    context = {}
    user = request.user
    student = Student.objects.get(user_id = user.id)
    if student.valid == 1:
            club = StudentClub.objects.get(id = student.club_id)
            account = Account.objects.get(club_id = club.id)
            context['currentDiscount'] = account.discountRate
            if account.requestedRate is None:
                form = requestDiscountForm(request.POST or None, instance=account)
                if request.method == "POST":
                    if form.is_valid():
                        form.save()
                        return redirect('studentRequestDiscount')
                context['form'] = form
            else:
                context['existing'] = "existing"
    return render(request, "studentRequestDiscount.html", context)


@transaction.atomic
@login_required(login_url='login')
def studentRepHome(request):
    context = {}
    temp = dt.today().strftime('%Y-%m-%d')
    context['today'] = dt.strptime(temp, "%Y-%m-%d").strftime("%A %d %B")

    if 'date' in request.GET:
        if request.GET['date'] != "":
            temp = request.GET['date']
            converted_date = dt.strptime(request.GET['date'], "%Y-%m-%d").strftime("%A %d %B")
            context['date'] = converted_date
        else:
            converted_date = dt.strptime(temp, "%Y-%m-%d").strftime("%A %d %B")
            context['date'] = converted_date
    else:
        converted_date = dt.strptime(temp, "%Y-%m-%d").strftime("%A %d %B")
        context['date'] = converted_date

    show_list = Show.objects.filter(date=temp)
    if show_list.exists() == False:
        context['none'] = "No shows on this date."
    if 'show' in request.GET:
        temp = request.GET['show']
        request.session['showId'] = temp
        return redirect('repSelectTickets')
    context['show_list'] = show_list

    return render(request, "studentRepHome.html", context)



@transaction.atomic
@login_required(login_url='login')
def settleAccounts(request):

    context = {}
    user = request.user
    rep = ClubRepresentative.objects.get(userid = user.id)
    account = Account.objects.get(club_id = rep.club_id)
    balance = account.balance
    club_name = account.title
    cardEnd = account.card_number
    cardEnd = cardEnd[-4:]
    if 'amount' in request.GET:
        amount = request.GET['amount']
        account.balance += float(amount)
        account.save()
        messages.success(request, "Credit successfully added")
        return redirect('settleAccounts')
    transactions = Transaction.objects.filter(account_id = account.id)
    myFilter = settleFilters(request.GET, queryset=transactions)
    transactions = myFilter.qs
    totalValue = 0
    for i in transactions:
        totalValue = totalValue + i.amount

    context['balance'] = "£{:,.2f}".format(balance)
    context['club_name'] = club_name
    context['cardEnd'] = cardEnd
    context['transactions'] = transactions
    context['myFilter'] = myFilter
    context['totalValue'] = "{:,.2f}".format(totalValue)
    
    return render(request, "settleAccounts.html" , context)


@transaction.atomic
@login_required(login_url='login')
def studentHome(request):
    context = {}
    temp = dt.today().strftime('%Y-%m-%d')
    context['today'] = dt.strptime(temp, "%Y-%m-%d").strftime("%A %d %B")

    if 'date' in request.GET:
        if request.GET['date'] != "":
            temp = request.GET['date']
            converted_date = dt.strptime(request.GET['date'], "%Y-%m-%d").strftime("%A %d %B")
            context['date'] = converted_date
        else:
            converted_date = dt.strptime(temp, "%Y-%m-%d").strftime("%A %d %B")
            context['date'] = converted_date
    else:
        converted_date = dt.strptime(temp, "%Y-%m-%d").strftime("%A %d %B")
        context['date'] = converted_date

    showings_list = Show.objects.filter(date=temp)
    if showings_list.exists() == False:
        context['none'] = "No showings on this date."
    if 'show' in request.GET:
        temp = request.GET['show']
        request.session['showId'] = temp
        return redirect('studentSelectTickets')
    context['show_list'] = showings_list
    return render(request, "studentHome.html", context)

@transaction.atomic
@login_required(login_url='login')
def studentSelectTickets(request):
    context = {}
    if 'showingId' not in request.session:
        return redirect('studentHome')

    temp = request.session['showingId']
    showing = Show.objects.get(id = temp)
    film = Film.objects.get(id = showing.film_id)    
    
    context['film'] = film
    context['showing'] = showing
    context['duration'] = math.ceil(film.duration)
    if request.GET.get('proceed') == 'Buy Ticket':
        return redirect('studentPurchaseTickets')

    return render(request, "studentSelectTickets.html", context)

@transaction.atomic
@login_required(login_url='login')
def studentPurchaseTickets(request):
    context = {}
    if 'showingId' not in request.session:
        return redirect('studentHome')
    showing = Show.objects.get(id = request.session['showingId'])
    user = request.user
    student = Student.objects.get(user_id = user.id)
    request.session['studentId'] = student.id
    totalPrice = showing.studentPrice
    #Check if student is validated
    if student.validated == 1:
        club = StudentClub.objects.get(id = student.club_id)
        account = Account.objects.get(club_id = club.id)
        discountValue = account.discountRate
        discountRate = 1 - (discountValue / 100)
        discountPrice = totalPrice * discountRate
        finalPrice = discountPrice
        context['discountValue'] = discountValue
        context['discountPrice'] = "£{:,.2f}".format(discountPrice)
        request.session['discountPrice'] = discountPrice
    else:
        finalPrice = totalPrice

    context.update({
        'totalPrice': "£{:,.2f}".format(totalPrice),
        'showing': showing
    })

    screen = Screen.objects.get(id = showing.screen_id)

    if request.GET.get('proceed') == 'Proceed':
        request.session['price'] = finalPrice
        cinema = Cinema.objects.get(id=1)
        socialDistance = cinema.socialDist
        if socialDistance == True:
            capacity = float(screen.capacity/2)
        elif socialDistance == False:
            capacity = screen.capacity
        if 1 + showing.ticketsSold > capacity:
            messages.info(request, "Insufficient seats available for the selected showing. Please try another booking request.")
            return redirect('studentHome')
        elif student.balance - finalPrice < 0:
            messages.info(request, "You have insufficient credits to complete this booking.")
            return redirect('studentHome')
        else:
            booking = Booking.objects.create(studentQuantity=1, childQuantity=0, adultQuantity=0, 
            showing_id=showing.id)
            request.session['bookingId'] = booking.id
            showing.ticketsSold += 1
            showing.save()
            student.balance -= finalPrice
            student.save()
        return redirect('studentBookingConfirmation')
    return render(request, "studentPurchaseTickets.html", context)


@transaction.atomic
@login_required(login_url='login')
def studentBookingConfirmation(request):
    context = {}

    if 'showingId' not in request.session:
        return redirect('studentHome')

    showing = Show.objects.get(id = request.session['showingId'])
    screen = Screen.objects.get(id = showing.screen_id)
    student = Student.objects.get(id = request.session['studentId'])
    balance = student.balance
    totalPrice = showing.studentPrice
    finalPrice = request.session['price']
    bookingId = request.session['bookingId']
    
    if student.validated == 1:
        discountPrice = request.session['discountPrice']
        context['discountPrice'] = "£{:,.2f}".format(discountPrice)

    balance = student.balance
    film = Film.objects.get(id = showing.film_id)
    screen = Screen.objects.get(id = showing.screen_id) 
    context.update({
        'totalPrice': "£{:,.2f}".format(totalPrice),
        'showing': showing,
        'film': film,
        'screen': screen,
        'balance': "£{:,.2f}".format(balance),
        'bookingId': bookingId
    })

    del request.session['showingId']

    return render(request, "studentBookingConfirmation.html", context)


@transaction.atomic
@login_required(login_url='login')
def studentAddCredit(request):
    context = {}
    user = request.user
    student = Student.objects.get(user_id = user.id)
    balance = student.balance

    context['balance'] = "£{:,.2f}".format(balance)
    if 'amount' in request.GET:
        amount = request.GET['amount']
        student.balance += float(amount)
        student.save()
        messages.success(request, "Credit successfully added")
        return redirect('studentAddCredit')
    return render(request, "studentAddCredit.html", context)


#STUDENT SELCTING TICKETS

def studentRegister(request):
    context = {}
    user_form = CreateUserForm(request.POST or None)
    student_form = StudentForm(request.POST or None)

    if request.method == "POST":
        if user_form.is_valid() and student_form.is_valid():
            # User
            user = user_form.save()
            user_name = user.username
            group = Group.objects.get(name='student')
            #user = User.objects.create_user(username=username, password=password)
            user.groups.add(group)
            #Student
            student = student_form.save(commit=False)
            valid = student.valid

            Student.objects.create(
                user=user,
                valid=valid,
                user_name=user_name,
            )
            print(user_name)
            return redirect('login')
            #messages.success(request, 'Account was created for ', user)

    context = {'user_form':user_form, 'student_form' : student_form,}
    return render(request, 'studentRegister.html', context)

@login_required(login_url='login')
def studentSelectTickets(request):
    context = {}
    if 'showId' not in request.session:
        return redirect('studentHome')
    temp = request.session['showId']   
    show = Show.objects.get(id = temp)
    film = Film.objects.get(id = show.film_id)    
    context['film'] = film
    context['show'] = show
    context['duration'] = film.duration

    if request.GET.get('advance') == 'Buy Ticket':
        return redirect('studentPurchaseTickets')

    return render(request, "studentSelectTickets.html", context)


@login_required(login_url='login')
def studentPurchaseTickets(request):
    context = {}

    if 'showId' not in request.session:
        return redirect('/studentHome')

    show = Show.objects.get(id = request.session['showId'])
    user = request.user
    student = Student.objects.get(user_id = user.id)
    request.session['studentId'] = student.id
    account_Id = student.account_id
    account = Account.objects.get(id = account_Id)
    total_price = show.student_price
    #Check if student is validated
    if student.valid == 1:
        discount_value = account.discount_rate
        discount_rate = 1 - (discount_value / 100)
        discount_price = total_price * discount_rate
        final_price = discount_price
        context['discount_value'] = discount_value
        context['discount_price'] = "£{:,.2f}".format(discount_price)
        request.session['discount_price'] = discount_price
    else:
        finalPrice = total_price
    context.update({
        'total_price': "£{:,.2f}".format(total_price),
        'show': show
    })

    screen = Screen.objects.get(id = show.screen_id)

    if request.GET.get('advance') == 'Advanced':
        request.session['price'] = final_price
        if 1 + show.ticketsSold > screen.capacity:
            messages.info(request, "There are no seats for this booking, please select another!")
            return redirect('/studentHome')
        elif student.balance - final_price < 0:
            messages.info(request, "You have insufficient credits to complete this booking.")
            return redirect('/studentHome')
        else:
            booking = Booking.objects.create(studentQty=1, childQty=0, adultQty=0, 
            showing_id=show.id)
            request.session['bookingId'] = booking.id
            show.ticketsSold += 1
            show.save()
            student.balance -= final_price
            student.save()
        return redirect('/studentBookingConfirmation')

    return render(request, "UWFX/studentPurchaseTickets.html", context)

@transaction.atomic
@login_required(login_url='login')
def deleteObsoleteFilms(request):
    # filter out post request.
    if request.method == "POST":
        try:
            record = Film.objects.get(id=int(request.POST['id']))
            record.delete()
            messages.success(request, "Film deleted successfully!")
            return redirect('dashboard')
        except:
            print("Record doesn't exists")
    films = Film.objects.exclude(id__in=Show.objects.all().values_list('film__id', flat=True))
    return render(request, 'deleteObsoleteFilms.html', {
        'films': films,
    })


@transaction.atomic
@login_required(login_url='login')
def addAccount(request):
    if request.method == "POST":
        # Student club registration form processing
        if 'AccountFormSubmit' in request.POST:
            # get user input values
            acc_form = AccountForm(request.POST or None)
            # validate the entered values
            if acc_form.is_valid():
                # save the entered values if correct
                acc_form.save()
                messages.success(request, "Account added successfully.")
                return redirect('addAccount')
            else:
                errors = acc_form.errors
                return HttpResponse(json.dumps(errors), status=400)
    accounts = Account.objects.all()
    # Loading all forms for get request
    return render(request, 'AddAccount.html', {
        'AccountForm': AccountForm,
        'accounts': accounts
    })


@transaction.atomic
@login_required(login_url='login')
def editAccount(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Account, id=id)

    # pass the object as instance in form
    form = AccountForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        messages.success(request, "Account added successfully.")
        return redirect('registeredAccounts')

    # add form dictionary to context
    context["AccountForm"] = form
    return render(request, "editAccount.html", context)


@transaction.atomic
@login_required(login_url='login')
def registeredAccounts(request):
    if request.method == "POST":
        # Student club registration form processing
        if 'AccountFormSubmit' in request.POST:
            # get user input values
            acc_form = AccountForm(request.POST or None)
            # validate the entered values
            if acc_form.is_valid():
                # save the entered values if correct
                acc_form.save()
                messages.success(request, "Account added successfully.")
                return redirect('registeredAccounts')
            else:
                errors = acc_form.errors
                return HttpResponse(json.dumps(errors), status=400)
    accounts = Account.objects.all()
    # Loading all forms for get request
    return render(request, 'RegisteredAccounts.html', {
        'AccountForm': AccountForm,
        'accounts': accounts
    })


@transaction.atomic
@login_required(login_url='login')
def dailyTransactions(request):
    if request.method == "POST":
        # daily transactions
        if 'AccountFormSubmit' in request.POST:
            # get user input values
            acc_form = AccountForm(request.POST or None)
            # validate the entered values
            if acc_form.is_valid():
                # save the entered values if correct
                acc_form.save()
                messages.success(request, "Account added successfully.")
                return redirect('dailyTransactions')
            else:
                errors = acc_form.errors
                return HttpResponse(json.dumps(errors), status=400)
    accounts = Account.objects.all()
    # Loading all forms for get request
    return render(request, 'dailyTransactions.html', {
        'AccountForm': AccountForm,
        'accounts': accounts
    })


@transaction.atomic
@login_required(login_url='login')
def amendAcount(request):
    if request.method == "POST":
        # Alter account details
        if 'AccountFormSubmit' in request.POST:
            # get user input values
            acc_form = AccountForm(request.POST or None)
            # validate the entered values
            if acc_form.is_valid():
                # save the entered values if correct
                acc_form.save()
                messages.success(request, "Account amended successfully.")
                return redirect('amendAcount')
            else:
                errors = acc_form.errors
                return HttpResponse(json.dumps(errors), status=400)
    accounts = Account.objects.all()
    # Loading all forms for get request
    return render(request, 'AmendAccount.html', {
        'AccountForm': AccountForm,
        'accounts': accounts
    })


@transaction.atomic
@login_required(login_url='login')
def accountStatements(request):
    if request.method == "POST":
        # Account statements
        if 'AccountFormSubmit' in request.POST:
            acc_form = AccountForm(request.POST or None)
            # validate the entered values
            if acc_form.is_valid():
                # save the entered values if correct
                acc_form.save()
                messages.success(request, "Account added successfully.")
                return redirect('accountStatements')
            else:
                errors = acc_form.errors
                return HttpResponse(json.dumps(errors), status=400)
    accounts = Account.objects.all()
    # Loading all forms for get request
    return render(request, 'ViewStatements.html', {
        'AccountForm': AccountForm,
        'accounts': accounts
    })


@transaction.atomic
@login_required(login_url='login')
def acc_logout(request):
    # Loading all forms for get request
    return render(request, 'logout.html', {
    })


@transaction.atomic
@login_required(login_url='login')
def man_logout(request):
    return render(request, 'man-logout.html')


@transaction.atomic
@login_required(login_url='login')
def deleteScreen(request):
    if request.method == "POST":
        try:
            record = Screen.objects.get(screen_number=int(request.POST['screen_number']))
            record.delete()
            messages.success(request, "Screen deleted successfully!")
            return redirect('dashboard')
        except:
            print("Screen doesn't exists")


def registerPage(request):
    # Check for authorized user
    if request.user.is_authenticated:
        return redirect('main')
    else:
        # Loading createUser form
        form = CreateUserForm()
        if request.method == 'POST':
            # adding post parameters to the form
            form = CreateUserForm(request.POST)
            # check form validation
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'register.html', context)

def guestMakePayment(request):
    context = {}
    if 'showId' not in request.session:
        return redirect('/')

    booking = Booking.objects.get(id = request.session['bookingId'])
    show = Show.objects.get(id = request.session['showId'])
    qtyTotal = booking.adultQty + booking.studentQty + booking.childQty 
    screen = Screen.objects.get(id = show.screen_id)
    if qtyTotal + show.sold_tickets > screen.seats: # total if seats are available
        booking.delete()
        messages.info(request, "Sorry! there are no more seats left, please select another viewing!")
        return redirect('/') # return to main if seats are not available
    else:
        form = custCardDetailsForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                instance = form.save(commit=False)
                instance.booking = booking
                instance.save()
                return redirect('/guestBookingConfirmation')
        context['form'] = form
    return render(request, "guestMakePayment.html", context)

def guestBookingConfirmation(request):
    context = {}
    booking = Booking.objects.get(id = request.session['bookingId'])
    show = Show.objects.get(id = request.session['showId'])
    #all tickets added together to make total quantity
    totalQty = booking.adultQty + booking.studentQty + booking.childQty
    show.sold_tickets += totalQty 
    show.save()
    adult_total = booking.adultQty * show.adult_price
    student_total = booking.studentQty * show.student_price
    child_total = booking.childQty * show.child_price
    total_price = adult_total + student_total + child_total
    film = Film.objects.get(id = show.film_id)
    screen = Screen.objects.get(id = show.screen_id) 
    context = {
        'total_price': "£{:,.2f}".format(total_price),
        'booking': booking,
        'show': show,
        'film': film,
        'screen': screen
    }

    del request.session['showId']

    return render(request, "guestBookingConfirmation.html", context)

# Login page function
def loginPage(request):
        form = loginForm(request.POST or None)
    # check for user authentication
        # If the request is post request
        if request.method == 'POST':
            # get user entered details
            username = request.POST.get('username')
            password = request.POST.get('password')
            # authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                display_username = user.username
                # create login session
                if request.user.groups.exists():
                    group = request.user.groups.all()[0].name
                    if group == 'cinema_manager':
                        #print("Test")
                        return redirect('/cinemaManagerDash') 
                    elif group == 'account_manager':
                        return redirect('/manager')
                    elif group == 'student_rep':
                        return redirect('/studentRepHome')
                    elif group == 'student':
                        return redirect('/studentHome')
                    login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

