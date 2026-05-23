from pydantic import BaseModel, validator
# validator überprüft, ob ein String z.B. Type-Case ist (mit Großbuchstaben anfängt)
from typing import Optional # enables optional attributes inside an object
from enum import Enum # good for dropdowns

class ProductCategory(str, Enum): # enum for product category. This is useful for providing a predefined set of values for the category attribute.
    FOOD = "food"
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"

class Product(BaseModel): # erbt von BaseModel, damit wir die Vorteile von Pydantic nutzen können, wie z.B. die Validierung der Daten und die automatische Generierung von Dokumentation.
    id: int
    name: str = "defaultproduct" # default value for name. This is useful for testing and for providing default values for the API.
    price: float
    tags: list[str] = []
    description: Optional[str] = None # optional field, can be None or a string. This is useful for providing additional information about the product without making it mandatory.
    category: ProductCategory # required field, must be one of the predefined values from the enum.
    @validator("name")
    def name_be_best_titlecase(cls, v): #class method nicht Instanz (self)
        if not v:
            raise ValueError("Name ist required")
        if not v[0].isupper():
            raise ValueError("Name muss titlecase sein")
        return v
#product = Product(id=1, name="stuhl", price=99.99, tags=[3, "woodwork"]) # validation error, no string conversion. 
#product = Product(id=1, name="stuhl", price=99.99, tags=["onsale", "woodwork"])
#product = Product(id=1, name="Apfel", price=1.99, category="food") # entweder string oder enum
product = Product(id=1, name="Apfel", price=1.99, category=ProductCategory.FOOD) # better to use enum values, because it provides better validation and documentation.
product_dict = product.dict() # produkt in dict. Konversion ist nur ein Layer tief. Für mehrere Layer braucht man eine Rekursion. 
# Code für Iteration, wenn das dict mehrere Layer hat, z.B. wenn ein Attribut selbst ein Objekt ist, das wiederum in ein dict konvertiert werden muss.
# https://github.com/pydantic/pydantic/discussions/4236
print(product_dict) # bietet Wrapper-Methode für Rückgabe der Werte

product2 = Product(**product_dict) # dict in produkt, ** unpackt die Werte aus dem dict und übergibt sie als Argumente an den Konstruktor der Klasse.
print(product2)

#__repr__ Wrapper: Dunder-Methode, die die String-Repräsentation eines Objekts definiert. Sie wird aufgerufen, 
# wenn man das Objekt in der Konsole ausgibt oder wenn man str() auf das Objekt anwendet. 
# In diesem Fall gibt die __repr__-Methode eine lesbare Darstellung des Product-Objekts zurück, die die Werte der Attribute enthält. 
# Dies ist besonders nützlich für Debugging-Zwecke, da es eine klare und informative Darstellung des Objekts bietet.    