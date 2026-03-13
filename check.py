# Test de correspondance (check_keys.py)
from cryptography.hazmat.primitives import serialization

# Charger la clé privée
with open("scripts/private_key.pem", "rb") as f:
    priv = serialization.load_pem_private_key(f.read(), password=None)

# Charger la clé publique
with open("encryption/public_key.pem", "rb") as f:
    pub = serialization.load_pem_public_key(f.read())

# Vérifier si la clé publique extraite de la privée est la même que ton fichier .pem
match = priv.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
) == pub.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

print(f"Les clés correspondent : {match}")