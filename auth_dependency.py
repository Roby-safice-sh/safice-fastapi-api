# Fichier : safice_api/auth_dependency.py

import firebase_admin
from firebase_admin import credentials, auth
from fastapi import Header, HTTPException, status
from typing import Optional

# Le nom du fichier de clé que vous avez téléchargé et renommé.
SERVICE_ACCOUNT_KEY = 'serviceAccountKey.json' 

# --- 1. Initialisation de Firebase Admin SDK ---
try:
    # Tente d'initialiser Firebase avec la clé de service
    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
    firebase_admin.initialize_app(cred)
except Exception as e:
    # Ceci est une alerte. Si cette erreur se produit (clé manquante ou invalide), 
    # la vérification de jeton échouera.
    print(f"ATTENTION: Échec de l'initialisation Firebase Admin SDK. Les endpoints sécurisés échoueront : {e}")


# --- 2. Fonction de Dépendance FastAPI (Le Garde de Sécurité) ---
async def get_current_user_id(Authorization: Optional[str] = Header(None)) -> str:
    """
    Vérifie le jeton d'authentification (Bearer Token) envoyé par l'application Flutter.
    Cette fonction est la 'Dépendance' utilisée dans les routes sécurisées de main.py.
    """
    
    # Vérifie si l'en-tête d'autorisation est présent et est au format 'Bearer <token>'
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Jeton d'authentification (Bearer Token) manquant ou invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extrait le jeton de la chaîne "Bearer <token>"
    id_token = Authorization.split("Bearer ")[1]
    
    try:
        # **Vérification du jeton par Firebase (Le cœur de la sécurité)**
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
        
        # Retourne l'ID unique Firebase de l'utilisateur
        return user_id 

    except Exception as e:
        # Le jeton est invalide (expiré, falsifié, etc.)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Jeton invalide: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )