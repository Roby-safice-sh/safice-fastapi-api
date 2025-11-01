# Fichier : safice_api/models.py

from pydantic import BaseModel, Field
from typing import List, Optional

# Modèle pour la création d'un produit (utilisé pour les requêtes entrantes)
class ProductBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str = Field(..., max_length=1000)
    price: float = Field(..., gt=0)
    category: str = Field(..., max_length=50)
    image_url: str 
    
# Modèle pour la réponse de l'API (incluant l'ID et le créateur)
class Product(ProductBase):
    id: str
    seller_id: str # L'ID Firebase de l'utilisateur vendeur