import uuid

from django.core.exceptions import ValidationError
from django.db import models
from encrypted_model_fields.fields import EncryptedTextField
from django.contrib.auth import get_user_model
from pycparser.ply.yacc import default_lr

User = get_user_model()


class Donateur(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = EncryptedTextField(null=True, blank=True)
    pays = models.CharField(max_length=2)
    anonymat = models.BooleanField(default=False)
    cree_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donateur {self.id} - {self.nom} - {self.pays} - {self.anonymat} - Créé le : {self.cree_le}"


class Lutteur(models.Model):
    REGIONS = [
        ('Agadez', 'Agadez'),
        ('Diffa', 'Diffa'),
        ('Dosso', 'Dosso'),
        ('Maradi', 'Maradi'),
        ('Niamey', 'Niamey'),
        ('Tahoua', 'Tahoua'),
        ('Tillaberi', 'Tillaberi'),
        ('Zinder', 'Zinder'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)
    region = models.CharField(max_length=18, choices=REGIONS, default="Tahoua")
    poids = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    toise = models.DecimalField(max_digits=6, decimal_places=2, default="1.60")
    photo = models.ImageField(upload_to="photos_lutteurs/", null=True, blank=True)
    total_soutiens = models.PositiveIntegerField(default=0)
    en_lisse = models.BooleanField(default=False)
    cree_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom


class Soutient(models.Model):
    Mes_choix = [

        ('Fairplay', 'Fairplay'),
        ('Charisme', 'Charisme'),
        ('Performance', 'Performance'),
    ]
    lutteur = models.ForeignKey(Lutteur, on_delete=models.CASCADE)
    raison = models.CharField(max_length=15, choices=Mes_choix, default="Fairplay")
    cree_le = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            self.lutteur.total_soutiens += 1
            self.lutteur.save()

class Utilisateur(models.Model):
    REGIONS = [
        ('Agadez', 'Agadez'),
        ('Diffa', 'Diffa'),
        ('Dosso', 'Dosso'),
        ('Maradi', 'Maradi'),
        ('Niamey', 'Niamey'),
        ('Tahoua', 'Tahoua'),
        ('Tillaberi', 'Tillaberi'),
        ('Zinder', 'Zinder'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=15, null=False, blank=False)
    favoris = models.ForeignKey(Lutteur, on_delete=models.CASCADE, null=True,blank=True)
    pays = models.CharField(max_length=2)
    region = models.CharField(max_length=18, choices=REGIONS, default="Tahoua")
    date_creation = models.DateTimeField(auto_now_add=True)


class Contribution(models.Model):
    CIBLES = [
        ('Kokowa', 'Kokowa'),
        ('Agadez', 'Agadez'),
        ('Diffa', 'Diffa'),
        ('Dosso', 'Dosso'),
        ('Maradi', 'Maradi'),
        ('Niamey', 'Niamey'),
        ('Tahoua', 'Tahoua'),
        ('Tillaberi', 'Tillaberi'),
        ('Zinder', 'Zinder')
    ]

    STATUTS = [
        ("pending", "En attente"),
        ("succeeded", "Réussie"),
        ("failed", "Échouée"),
    ]

    payment_methods = [
        ('MyNita', 'MyNita'),
        ('Amanata', 'Amanata'),
        ('Airtel Money', 'Airtel Money'),
        ('Flooz', 'Flooz'),
        ('ZamaniCash', 'ZamaniCash'),
        ('Visa/MasterCard', 'Visa/MasterCard'),
        ('Virement', 'Virement')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cible = models.CharField(max_length=20, choices=CIBLES, default="Kokowa")
    donateur = models.ForeignKey(Donateur, null=True, blank=True, on_delete=models.SET_NULL)
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    monnaie = models.CharField(max_length=10, default="XOF")
    pays = models.CharField(max_length=2)
    statut = models.CharField(max_length=15, choices=STATUTS, default="pending")
    payment_provider_method = models.CharField(max_length=50, choices=payment_methods, default="MyNita")
    payment_ref = models.CharField(max_length=100, null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)


class PaymentInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE)
    provider = models.CharField(max_length=50, default="ipaymoney")
    provider_ref = models.CharField(max_length=100)
    info_transaction = EncryptedTextField(null=True, blank=True)
    statut = models.CharField(max_length=20)
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    monnaie = models.CharField(max_length=10)
    cree_le = models.DateTimeField(auto_now_add=True)


class DeviceInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE)
    ip_hmac = models.CharField(max_length=128)
    ip_masked = models.CharField(max_length=50)
    user_agent = EncryptedTextField(null=True, blank=True)
    device_brand = models.CharField(max_length=255, null=True, blank=True)
    geo_country = models.CharField(max_length=2, null=True, blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)


class WebhookEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.CharField(max_length=50)
    event_id = models.CharField(max_length=255, unique=True)
    payload = EncryptedTextField(null=True, blank=True)
    received_at = models.DateTimeField(auto_now_add=True)


class Log(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255)
    model_id = models.CharField(max_length=255)
    payload = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)
    signature = models.CharField(max_length=128)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Audit Event"

    def save(self, *args, **kwargs):
        if self.pk:
            raise Exception("AuditEvent entries cannot be modified.")
        super().save(*args, **kwargs)

class Affrontement(models.Model):
    mes_types = [

        ('Eliminatoire', 'Eliminatoire'),
        ('8eme', '8eme'),
        ('1/4', '1/4'),
        ('1/2', '1/2'),
        ('Finale', 'Finale')

    ]

    STATUTS = [
        ("en cours", "en cours"),
        ("termine", "termine"),
        ("a_venir", "a_venir"),
    ]

    l1 = models.ForeignKey(Lutteur, on_delete=models.CASCADE, related_name="lutteur1")
    l2 = models.ForeignKey(Lutteur, on_delete=models.CASCADE, related_name="lutteur2")
    vote1 = models.PositiveIntegerField(default=0)
    vote2 = models.PositiveIntegerField(default=0)
    date = models.DateTimeField()
    etape = models.CharField(max_length=15, choices=mes_types, default="Eliminatoire")
    status = models.CharField(max_length=9, choices=STATUTS, default="a_venir")
    vainqueur = models.ForeignKey(Lutteur, on_delete=models.SET_NULL, null=True, blank=True, related_name="vainqueur_affrontement")
    cree_le = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Empêche de choisir un vainqueur qui n'est ni l1 ni l2
        if self.vainqueur and self.vainqueur not in [self.l1, self.l2]:
            raise ValidationError("Le vainqueur doit être soit l1 soit l2.")

    def __str__(self):
        return f"{self.l1.nom} ({self.l1.region}) vs {self.l2.nom} ({self.l2.region}) - {self.etape} - {self.status}"


