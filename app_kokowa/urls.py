from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [

    #path('v1/', views.mon_api_view, name="kokowa_api"),
    path('v1/donateur_liste', views.donateur_liste_view, name="donateur_liste"),
    path('v1/donateur_add', views.donateur_add_view, name="donateur_add"),
    path('v1/donateur_edit/<uuid:id>', views.donateur_edit_view, name="donateur_edit"),
    path('v1/donateur_delete/<uuid:id>', views.donateur_delete_view, name="donateur_delete"),

    path('v1/lutteur_liste', views.lutteur_liste_view, name="lutteur_liste"),
    path('v1/lutteur_add', views.lutteur_add_view, name="lutteur_add"),
    path('v1/lutteur_edit/<uuid:id>', views.lutteur_edit_view, name="lutteur_edit"),
    path('v1/lutteur_delete/<uuid:id>', views.lutteur_delete_view, name="lutteur_delete"),

    path('v1/soutien_liste', views.soutien_liste_view, name="soutien_liste"),
    path('v1/soutien_add', views.soutien_add_view, name="soutien_add"),
    path('v1/soutien_edit/<int:id>', views.soutien_edit_view, name="soutien_edit"),
    path('v1/soutien_delete/<int:id>', views.soutien_delete_view, name="soutien_delete"),

    path('v1/contribution_liste', views.contribution_liste_view, name="contribution_liste"),
    path('v1/contribution_add', views.contribution_add_view, name="contribution_add"),
    path('v1/contribution_edit/<int:id>', views.contribution_edit_view, name="contribution_edit"),
    path('v1/contribution_delete/<int:id>', views.contribution_delete_view, name="contribution_delete"),
    path('v1/payment-simulator', views.payment_simulator, name="payment-simulator"),

    path('v1/affrontement_liste', views.affrontement_liste_view, name="affrontement_liste"),
    path('v1/affrontement_add', views.affrontement_add_view, name="affrontement_add"),
    path('v1/affrontement_edit/<int:id>', views.affrontement_edit_view, name="affrontement_edit"),
    path('v1/affrontement_delete/<int:id>', views.affrontement_delete_view, name="affrontement_delete"),

    path('v1/vote_affrontement/<int:id>', views.affrontement_voter_view, name="vote_affrontement"),

    path('v1/auth/register', views.register_view, name='register'),
    path('v1/auth/login', views.login_view, name='login'),
    path('v1/auth/logout', views.logout_view, name='logout'),
    path('v1/auth/profile', views.profile_view, name='profile'),

]