from django.urls import path
# now import the views.py file into this code
from . import views

urlpatterns = [
    #path('', views.main, name="main"),
    path('', views.main, name="main"),
    path('cinemaManagerDash', views.cinemaManagerDash, name="cinemaManagerDash"),
    path('pickFilm', views.main, name="pickFilm"),
    path('guestSelectTickets', views.guestSelectTickets, name="guestSelectTickets"),
    path('guestPurchaseTickets', views.guestPurchaseTickets, name="guestPurchaseTickets"),
    path('guestMakePayment', views.guestMakePayment, name="guestMakePayment"),
    path('guestBookingConfirmation', views.guestBookingConfirmation, name="guestBookingConfirmation"),
    path('clubRe', views.clubRepresentative, name="clubRepresentative"),
    path('addfilm', views.addfilm, name="addfilm"),
    path('addScreen', views.addScreen, name="addScreen"),
    path('addShow', views.addShow, name="addShow"),
    path('ObsoleteFilm', views.deleteObsoleteFilms, name="deleteObsoleteFilm"),
    path('confirmLogout', views.man_logout, name="confirmLogout"),

    path('manager', views.addAccount, name="addAccount"),
    path('manager/<id>/update', views.editAccount, name="editAccount"),
    path('manager/registeredAccounts', views.registeredAccounts, name="registeredAccounts"),
    path('manager/dailyTransactions', views.dailyTransactions, name="dailyTransactions"),
    path('manager/amendAcount', views.amendAcount, name="amendAcount"),
    path('manager/accountStatements', views.accountStatements, name="accountStatements"),
    path('manager/logout', views.acc_logout, name="account-logout"),

    path('deleteScreen/', views.deleteScreen, name="deleteScreen"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('studentRegister', views.studentRegister, name="studentRegister"),
    path("studentSelectTickets", views.studentSelectTickets, name="studentSelectTickets"),
    path("studentPurchaseTickets", views.studentPurchaseTickets, name="studentPurchaseTickets"),
    path("studentBookingConfirmation", views.studentBookingConfirmation, name="studentBookingConfirmation"),
    path("studentAddCredit", views.studentAddCredit, name="studentAddCredit"),
    path("studentRequestDiscount", views.studentRequestDiscount, name="studentRequestDiscount"),
    path("studentHome", views.studentHome, name="studentHome"),
 
    path('studentRepHome', views.studentRepHome, name="studentRepHome"),
    path('settleAccounts', views.settleAccounts, name="settleAccounts"),
    path('repRequestDiscount', views.repRequestDiscount, name="repRequestDiscount"),


]
