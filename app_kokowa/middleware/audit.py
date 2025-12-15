import json
import hashlib
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from .. import models

def generate_signature(payload: dict) -> str:
    s = json.dumps(payload, sort_keys=True, default=str).encode()
    return hashlib.sha256(s + settings.FIELD_ENCRYPTION_KEY.encode()).hexdigest()

class AuditMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        try:
            if request.method in ("POST", "PUT", "PATCH", "DELETE"):
                actor = str(getattr(request, "user", None)) if request.user and request.user.is_authenticated else "anonymous"
                payload = {}
                try:
                    payload = request.POST.dict() if request.POST else {}
                except:
                    try:
                        payload = json.loads(request.body.decode() or "{}")
                    except:
                        payload = {}
                signature = generate_signature({
                    "actor": actor,
                    "path": request.path,
                    "method": request.method,
                    "payload": payload
                })
                # Save log (read-only model, save only once)
                models.Log.objects.create(
                    actor=actor,
                    action=f"{request.method} {request.path}",
                    model_name=request.resolver_match.view_name if request.resolver_match else request.path,
                    model_id="",
                    payload=payload,
                    signature=signature
                )
        except Exception:
            # Journalisation interne mais n'empêche pas la réponse
            pass
        return response
