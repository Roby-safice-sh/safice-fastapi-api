# Fichier : safice_api/main.py

from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
from models import Product, ProductBase # Importe les modèles de données
from auth_dependency import get_current_user_id # <-- Le Garde de Sécurité Firebase

app = FastAPI(
    title="Safice Marketplace API",
    version="v1",
    description="Backend Sécurisé pour l'application Safice"
)

# --- Base de données (Mock pour le test initial) ---
mock_products: List[Product] = [
    Product(id="1", name="Téléphone", description="Exemple", price=300.0, category="Electronics", image_url="url1", seller_id="seller1"),
]
# --- FIN Mock ---


@app.get("/")
def home():
    """Route de base pour vérifier que l'API est en cours d'exécution."""
    return {"message": "Safice API is running successfully!"}

@app.get("/api/v1/products", response_model=List[Product])
def get_all_products():
    """Route publique : n'importe qui peut voir les produits."""
    return mock_products

@app.post("/api/v1/products", response_model=Product, status_code=201)
def create_product(
    new_product: ProductBase, 
    # Le garde de sécurité est injecté ici. IL FAUT que le module s'appelle 'auth_dependency'
    current_user_id: str = Depends(get_current_user_id) 
):
    """
    Route SÉCURISÉE : Seuls les utilisateurs authentifiés peuvent créer un produit.
    """
    return Product(
        id=f"new_id_{len(mock_products) + 1}", 
        seller_id=current_user_id, 
        **new_product.model_dump()
    )