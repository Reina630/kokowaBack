import random
import uuid
import requests

import hashlib
import json

from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from django.utils import timezone
from . import models
from . import serializers as sz


# v1 start

@api_view(['GET'])
def mon_api_view(request):
    api_liens = {

        'liste': 'liste/taches',
        'Add': 'liste/taches',
        'Update': 'liste/taches/<int:id>',
        'Delete': 'liste/taches/<int:id>',
    }

    return Response(api_liens)

# Donateur
@api_view(['GET'])
def donateur_liste_view(request):
    donateurs = models.Donateur.objects.all()
    serialized_donors= sz.DonateurS(donateurs, many=True)
    return Response(serialized_donors.data)

@api_view(['POST'])
def donateur_add_view(request):
    new_donateur = sz.DonateurS(data=request.data)
    if new_donateur.is_valid():
        new_donateur.save()
        return Response(new_donateur.data)

    return Response(new_donateur.errors, status=400)


@api_view(['POST'])
def donateur_edit_view(request, id):
    try:
        mon_donateur = models.Donateur.objects.get(id=id)
    except models.Donateur.DoesNotExist:
        return Response({"error": "Donateur introuvable"}, status=404)

    serializer = sz.DonateurS(instance=mon_donateur, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def donateur_delete_view(request, id):
    try:
        mon_donateur = models.Donateur.objects.get(id=id)
    except models.Donateur.DoesNotExist:
        return Response({"error": "Donateur introuvable"}, status=404)

    mon_donateur.delete()
    return Response("Suppression effectuée avec succé !!!")

# Donateur Fin

# Lutteur

@api_view(['GET'])
def lutteur_liste_view(request):
    lutteurs = models.Lutteur.objects.all()
    serializer = sz.LutteurS(lutteurs, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def lutteur_add_view(request):
    new_lutteur = sz.LutteurS(data=request.data)
    if new_lutteur.is_valid():
        new_lutteur.save()
        return Response(new_lutteur.data)

    return Response(new_lutteur.errors, status=400)


@api_view(['POST'])
def lutteur_edit_view(request, id):
    try:
        mon_lutteur = models.Lutteur.objects.get(id=id)
    except models.Lutteur.DoesNotExist:
        return Response({"error": "Lutteur introuvable"}, status=404)

    serializer = sz.LutteurS(instance=mon_lutteur, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def lutteur_delete_view(request, id):
    try:
        mon_lutteur = models.Lutteur.objects.get(id=id)
    except models.Lutteur.DoesNotExist:
        return Response({"error": "Lutteur introuvable"}, status=404)

    mon_lutteur.delete()
    return Response("Suppression effectuée avec succé !!!")

# Lutteur Fin

# Soutien

@api_view(['GET'])
def soutien_liste_view(request):
    soutiens = models.Soutient.objects.all()
    serializer = sz.SoutientS(soutiens, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def soutien_add_view(request):
    new_soutien = sz.SoutientS(data=request.data)
    if new_soutien.is_valid():
        new_soutien.save()
        return Response(new_soutien.data)

    return Response(new_soutien.errors, status=400)


@api_view(['POST'])
def soutien_edit_view(request, id):
    try:
        mon_soutien = models.Soutient.objects.get(id=id)
    except models.Soutient.DoesNotExist:
        return Response({"error": "Soutien introuvable"}, status=404)

    serializer = sz.SoutientS(instance=mon_soutien, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def soutien_delete_view(request, id):
    try:
        mon_soutien = models.Soutient.objects.get(id=id)
    except models.Soutient.DoesNotExist:
        return Response({"error": "Soutien introuvable"}, status=404)

    mon_soutien.delete()
    return Response("Suppression effectuée avec succé !!!")

# Soutient Fin

# Contribution

@api_view(['GET'])
def contribution_liste_view(request):
    contributions = models.Contribution.objects.all()
    serializer = sz.ContributionS(contributions, many=True)
    return Response(serializer.data)

'''
def extract_device_info(request, contribution):

    # 1. Adresse IP du client
    ip = request.META.get("HTTP_X_FORWARDED_FOR")
    if ip:
        ip = ip.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    # 2. IP masquée
    ip_masked = ip[:3] + ".***.***.***"

    # 3. HMAC / hash IP
    ip_hmac = hashlib.sha256(ip.encode()).hexdigest()

    # 4. User agent
    user_agent = request.META.get("HTTP_USER_AGENT", "")

    # 5. Geo IP (ex: ipapi.co)
    try:
        geo = requests.get(f"https://ipapi.co/{ip}/json/").json()
        country = geo.get("country_code", None)
    except:
        country = None

    # 6. DeviceInfo en base
    models.DeviceInfo.objects.create(
        contribution=contribution,
        ip_hmac=ip_hmac,
        ip_masked=ip_masked,
        user_agent=user_agent,
        device_brand=geo.get("org", None) if country else None,
        geo_country=country
    )
'''

def extract_device_info(request, contribution):
    ip = request.META.get("HTTP_X_FORWARDED_FOR")
    if ip:
        ip = ip.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR", "0.0.0.0")

    ip_masked = ip.split(".")
    if len(ip_masked) >= 2:
        ip_masked = f"{ip_masked[0]}.{ip_masked[1]}.***.***"
    else:
        ip_masked = "0.***.***.***"

    ip_hmac = hashlib.sha256((ip + settings.FIELD_ENCRYPTION_KEY).encode()).hexdigest()
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    try:
        geo = requests.get(f"https://ipapi.co/{ip}/json/").json()
        country = geo.get("country_code", None)
        org = geo.get("org", None)
    except:
        country = None
        org = None

    models.DeviceInfo.objects.create(
        contribution=contribution,
        ip_hmac=ip_hmac,
        ip_masked=ip_masked,
        user_agent=user_agent,
        device_brand=org,
        geo_country=country
    )


@api_view(['POST'])
def payment_simulator(request):
    payload = request.data

    statut = random.choice(["succeeded", "failed"])

    return Response({
        "statut": statut,
        "transaction_id": str(uuid.uuid4()),
        "event_id": f"event_{uuid.uuid4()}",
        "received_payload": payload,
    })


@api_view(['POST'])
def contribution_add_view(request):
    serializer = sz.ContributionS(data=request.data)

    if serializer.is_valid():
        contribution = serializer.save()

        # 🔥 Step 1 : Appel API externe
        payload = {
            "id": str(contribution.id),
            "montant": str(contribution.montant),
            "monnaie": contribution.monnaie,
            "payment_method": contribution.payment_provider_method,
            "payment_ref": contribution.payment_ref,
            "cible": contribution.cible,
        }

        try:
            # FAKE API pour l’instant
            url = "http://127.0.0.1:8000/api/v1/payment-simulator"
            response = requests.post(url, json=payload, timeout=10)
            response_data = response.json()

            # 🔥 Step 2 : Traitement du retour
            statut = response_data["statut"]   # "succeeded" ou "failed"

            contribution.statut = statut
            contribution.processed_at = timezone.now()
            contribution.save()

            # Device info
            contribution = serializer.save()
            extract_device_info(request, contribution)

            # 🔥 Step 3 : Création PaymentInfo
            models.PaymentInfo.objects.create(
                contribution=contribution,
                provider="ipaymoney",
                provider_ref=response_data["transaction_id"],
                info_transaction=str(response_data),
                statut=statut,
                montant=contribution.montant,
                monnaie=contribution.monnaie,
            )

            # 🔥 Step 4 : Simulation webhook (optionnel)
            models.WebhookEvent.objects.create(
                provider="ipaymoney",
                event_id=response_data["event_id"],
                payload=str(response_data)
            )

        except Exception as e:
            contribution.statut = "failed"
            contribution.save()

        return Response(sz.ContributionS(contribution).data)

    return Response(serializer.errors, status=400)


'''
@api_view(['POST'])
def contribution_add_view(request):
    new_contribution = sz.ContributionS(data=request.data)
    if new_contribution.is_valid():
        new_contribution.save()
        return Response(new_contribution.data)

    return Response(new_contribution.errors, status=400)
'''

@api_view(['POST'])
def contribution_edit_view(request, id):
    try:
        mon_contribution = models.Contribution.objects.get(id=id)
    except models.Contribution.DoesNotExist:
        return Response({"error": "Contribution introuvable"}, status=404)

    serializer = sz.ContributionS(instance=mon_contribution, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def contribution_delete_view(request, id):
    try:
        mon_contribution = models.Contribution.objects.get(id=id)
    except models.Contribution.DoesNotExist:
        return Response({"error": "Contribution introuvable"}, status=404)

    mon_contribution.delete()
    return Response("Suppression effectuée avec succé !!!")

# Contribution Fin

# Affrontement

@api_view(['GET'])
def affrontement_liste_view(request):
    finales = models.Affrontement.objects.all()
    serializer = sz.AffrontementS(finales, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def affrontement_add_view(request):
    new_affrontement = sz.AffrontementS(data=request.data)
    if new_affrontement.is_valid():
        new_affrontement.save()
        return Response(new_affrontement.data)

    return Response(new_affrontement.errors, status=400)


@api_view(['POST'])
def affrontement_edit_view(request, id):
    try:
        mon_affrontement = models.Affrontement.objects.get(id=id)
    except models.Affrontement.DoesNotExist:
        return Response({"error": "Affrontement introuvable"}, status=404)

    serializer = sz.AffrontementS(instance=mon_affrontement, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


@api_view(['POST'])
def affrontement_voter_view(request, id):
    try:
        affrontement = models.Affrontement.objects.get(id=id)
    except models.Affrontement.DoesNotExist:
        return Response({"error": "Affrontement non trouvée"}, status=404)

    choix = request.data.get("choix")

    if choix == "l1":
        affrontement.vote1 += 1
        affrontement.save()
        return Response({"message": "Vote enregistré pour l1", "vote1": affrontement.vote1})

    elif choix == "l2":
        affrontement.vote2 += 1
        affrontement.save()
        return Response({"message": "Vote enregistré pour l2", "vote2": affrontement.vote2})

    else:
        return Response({"error": "Choix invalide. Envoyer 'f1' ou 'f2'."}, status=400)



@api_view(['DELETE'])
def affrontement_delete_view(request, id):
    try:
        mon_affrontement = models.Affrontement.objects.get(id=id)
    except models.Affrontement.DoesNotExist:
        return Response({"error": "Affrontement introuvable"}, status=404)

    mon_affrontement.delete()
    return Response("Suppression effectuée avec succé !!!")


@api_view(['POST'])
def affrontement_vainqueur_view(request, id):
    try:
        affrontement = models.Affrontement.objects.get(id=id)
    except models.Affrontement.DoesNotExist:
        return Response({"error": "Affrontement non trouvée"}, status=404)

    vainqueur = request.data.get("vainqueur")

    if vainqueur == "l1":
        affrontement.vainqueur = affrontement.l1
        affrontement.save()
        return Response({"message": "Vainqueur enregistré avec succés", "Vainqueur": affrontement.vainqueur.nom})

    elif vainqueur == "l2":
        affrontement.vainqueur = affrontement.l2
        affrontement.save()
        Response({"message": "Vainqueur enregistré avec succés", "Vainqueur": affrontement.vainqueur.nom})

    else:
        return Response({"error": "Choix invalide. Envoyer 'l1' ou 'l2'."}, status=400)


# Affrontement Fin

# User
@api_view(['POST'])
def register_view(request):

    request_data = request.data.copy()
    request_data["password"] = "12345"

    serializer = sz.RegisterS(data=request_data)

    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        '''
        # 🔥 récupérer le montant
        montant = user.montant_initial

        # 🔥 créer automatiquement la contribution
        contribution = models.Contribution.objects.create(
            cible="Kokowa",
            donateur=None,  # ou tu peux créer un donateur automatique si besoin
            montant=montant,
            monnaie="XOF",
            pays="NE",
            statut="pending",
            payment_provider_method="MyNita"
        )

        # 👉 déclencher le processus de paiement (comme contribution_add_view)
        # tu peux appeler directement ta logique interne :
        payload = {
            "id": str(contribution.id),
            "montant": str(contribution.montant),
            "monnaie": contribution.monnaie,
            "payment_method": contribution.payment_provider_method,
        }

        url = "http://127.0.0.1:8000/api/v1/payment-simulator"
        response = requests.post(url, json=payload).json()

        contribution.statut = response["statut"]
        contribution.processed_at = timezone.now()
        contribution.save()

        # enregistrer PaymentInfo
        models.PaymentInfo.objects.create(
            contribution=contribution,
            provider="ipaymoney",
            provider_ref=response["transaction_id"],
            info_transaction=str(response),
            statut=response["statut"],
            montant=contribution.montant,
            monnaie=contribution.monnaie,
        )
        '''

        return Response({
            "message": "Compte créé avec succés",
            "token": token.key,
            #"contribution": sz.ContributionS(contribution).data,
            "auto_login": True
        })
    return Response(serializer.errors, status=400)



# LOGIN
@api_view(['POST'])
def login_view(request):
    serializer = sz.LoginS(data=request.data)
    if serializer.is_valid():
        username = serializer.data["username"]
        password = serializer.data["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"message": "Connexion réussie", "token": token.key})

        return Response({"error": "Identifiants incorrects"}, status=401)
    return Response(serializer.errors, status=400)


# LOGOUT
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.user.auth_token.delete()
    return Response({"message": "Déconnexion réussie"})


# USER PROFILE INFO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    utilisateur = models.Utilisateur.objects.get(user=request.user)
    serializer = sz.UserProfileS(utilisateur)
    return Response(serializer.data)


# User Fin



# v1 end