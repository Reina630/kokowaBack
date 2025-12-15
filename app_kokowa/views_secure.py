import random
import uuid
import requests
import hashlib
import json
from django.utils import timezone
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from . import models
from . import serializers as sz
from .utils.hmac_helpers import compute_hmac_hex, verify_hmac

# ton mon_api_view et autres restent semblables...
@api_view(['GET'])
@permission_classes([AllowAny])
def mon_api_view(request):
    api_liens = {
        'liste': 'liste/taches',
        'Add': 'liste/taches',
    }
    return Response(api_liens)

# contribution add (public) — on accepte anonymes mais on applique throttle par IP
@api_view(['POST'])
@permission_classes([AllowAny])
def contribution_add_view(request):
    serializer = sz.ContributionS(data=request.data)
    if serializer.is_valid():
        contribution = serializer.save()
        # Préparer payload pour provider
        payload = {
            "id": str(contribution.id),
            "montant": str(contribution.montant),
            "monnaie": contribution.monnaie,
            "payment_method": contribution.payment_provider_method,
            "payment_ref": contribution.payment_ref,
            "cible": contribution.cible,
        }

        # sign payload to send to provider (HMAC) - if provider supports
        sig = compute_hmac_hex(settings.WEBHOOK_SECRET, json.dumps(payload).encode())

        try:
            url = "http://127.0.0.1:8000/api/v1/payment-simulator/"  # local simulator
            headers = {"X-Signature": sig, "Content-Type": "application/json"}
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response_data = response.json()

            statut = response_data.get("statut", "failed")
            contribution.statut = statut
            contribution.processed_at = timezone.now()
            contribution.save()

            # extract device info
            extract_device_info(request, contribution)

            models.PaymentInfo.objects.create(
                contribution=contribution,
                provider="ipaymoney",
                provider_ref=response_data.get("transaction_id", ""),
                info_transaction=str(response_data),
                statut=statut,
                montant=contribution.montant,
                monnaie=contribution.monnaie,
            )

            models.WebhookEvent.objects.create(
                provider="ipaymoney",
                event_id=response_data.get("event_id", str(uuid.uuid4())),
                payload=str(response_data)
            )

        except Exception as e:
            contribution.statut = "failed"
            contribution.save()

        return Response(sz.ContributionS(contribution).data)
    return Response(serializer.errors, status=400)


# webhook endpoint — provider -> appelle ce endpoint
@api_view(['POST'])
@permission_classes([AllowAny])  # le provider n'a pas de token ; on vérifie HMAC
def ipaymoney_webhook(request):
    signature = request.headers.get("X-Signature", "")
    payload_bytes = request.body

    # verification
    if not verify_hmac(settings.WEBHOOK_SECRET, payload_bytes, signature):
        return Response({"detail": "Invalid signature"}, status=401)

    try:
        data = json.loads(payload_bytes.decode())
    except:
        data = {}

    # traite l'event (id de transaction / contribution)
    event_id = data.get("event_id") or f"event_{uuid.uuid4()}"
    trans_id = data.get("transaction_id")
    statut = data.get("statut", "failed")

    # enregistrer
    models.WebhookEvent.objects.create(
        provider="ipaymoney",
        event_id=event_id,
        payload=str(data)
    )

    # Si tu veux propager l'update sur Contribution si id fourni
    contribution_id = data.get("id")
    if contribution_id:
        try:
            c = models.Contribution.objects.get(id=contribution_id)
            c.statut = statut
            c.payment_ref = trans_id or c.payment_ref
            c.processed_at = timezone.now()
            c.save()
        except models.Contribution.DoesNotExist:
            pass

    return Response({"status": "ok"})
