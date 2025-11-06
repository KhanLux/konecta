from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uvicorn

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="Konecta API REST",
    description="API REST completa construida con FastAPI",
    version="1.0.0"
)

# Modelos de datos usando Pydantic
class ItemBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del item")
    descripcion: Optional[str] = Field(None, max_length=500, description="Descripción del item")
    precio: float = Field(..., gt=0, description="Precio del item (debe ser mayor a 0)")
    disponible: bool = Field(True, description="Indica si el item está disponible")

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int = Field(..., description="ID único del item")
    fecha_creacion: datetime = Field(default_factory=datetime.now, description="Fecha de creación")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Laptop",
                "descripcion": "Laptop de alta gama",
                "precio": 1500.00,
                "disponible": True,
                "fecha_creacion": "2025-11-06T10:00:00"
            }
        }

# Base de datos simulada en memoria
items_db: List[Item] = [
    Item(
        id=1,
        nombre="Laptop HP",
        descripcion="Laptop para trabajo profesional",
        precio=1200.50,
        disponible=True,
        fecha_creacion=datetime.now()
    ),
    Item(
        id=2,
        nombre="Mouse Logitech",
        descripcion="Mouse inalámbrico ergonómico",
        precio=45.99,
        disponible=True,
        fecha_creacion=datetime.now()
    )
]

# Contador para IDs
next_id = 3

# Endpoints

@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raíz que retorna información de bienvenida
    """
    return {
        "mensaje": "Bienvenido a Konecta API REST",
        "version": "1.0.0",
        "documentacion": "/docs"
    }

@app.get("/health", tags=["Health"], status_code=status.HTTP_200_OK)
async def health_check():
    """
    Endpoint de health check para verificar el estado de la API
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/items", response_model=List[Item], tags=["Items"])
async def obtener_items(
    disponible: Optional[bool] = None,
    precio_min: Optional[float] = None,
    precio_max: Optional[float] = None
):
    """
    Obtener todos los items con filtros opcionales

    - **disponible**: Filtrar por disponibilidad
    - **precio_min**: Precio mínimo
    - **precio_max**: Precio máximo
    """
    items = items_db.copy()

    if disponible is not None:
        items = [item for item in items if item.disponible == disponible]

    if precio_min is not None:
        items = [item for item in items if item.precio >= precio_min]

    if precio_max is not None:
        items = [item for item in items if item.precio <= precio_max]

    return items

@app.get("/api/items/{item_id}", response_model=Item, tags=["Items"])
async def obtener_item(item_id: int):
    """
    Obtener un item específico por su ID
    """
    item = next((item for item in items_db if item.id == item_id), None)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item con ID {item_id} no encontrado"
        )

    return item

@app.post("/api/items", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["Items"])
async def crear_item(item: ItemCreate):
    """
    Crear un nuevo item
    """
    global next_id

    nuevo_item = Item(
        id=next_id,
        nombre=item.nombre,
        descripcion=item.descripcion,
        precio=item.precio,
        disponible=item.disponible,
        fecha_creacion=datetime.now()
    )

    items_db.append(nuevo_item)
    next_id += 1

    return nuevo_item

@app.put("/api/items/{item_id}", response_model=Item, tags=["Items"])
async def actualizar_item(item_id: int, item_actualizado: ItemCreate):
    """
    Actualizar un item existente
    """
    item_index = next((index for index, item in enumerate(items_db) if item.id == item_id), None)

    if item_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item con ID {item_id} no encontrado"
        )

    item_modificado = Item(
        id=item_id,
        nombre=item_actualizado.nombre,
        descripcion=item_actualizado.descripcion,
        precio=item_actualizado.precio,
        disponible=item_actualizado.disponible,
        fecha_creacion=items_db[item_index].fecha_creacion
    )

    items_db[item_index] = item_modificado

    return item_modificado

@app.patch("/api/items/{item_id}/disponibilidad", response_model=Item, tags=["Items"])
async def actualizar_disponibilidad(item_id: int, disponible: bool):
    """
    Actualizar solo la disponibilidad de un item
    """
    item = next((item for item in items_db if item.id == item_id), None)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item con ID {item_id} no encontrado"
        )

    item.disponible = disponible

    return item

@app.delete("/api/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Items"])
async def eliminar_item(item_id: int):
    """
    Eliminar un item
    """
    item_index = next((index for index, item in enumerate(items_db) if item.id == item_id), None)

    if item_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item con ID {item_id} no encontrado"
        )

    items_db.pop(item_index)

    return None

@app.get("/api/stats", tags=["Statistics"])
async def obtener_estadisticas():
    """
    Obtener estadísticas generales de los items
    """
    total_items = len(items_db)
    items_disponibles = len([item for item in items_db if item.disponible])
    items_no_disponibles = total_items - items_disponibles

    precios = [item.precio for item in items_db]
    precio_promedio = sum(precios) / len(precios) if precios else 0
    precio_minimo = min(precios) if precios else 0
    precio_maximo = max(precios) if precios else 0

    return {
        "total_items": total_items,
        "items_disponibles": items_disponibles,
        "items_no_disponibles": items_no_disponibles,
        "precio_promedio": round(precio_promedio, 2),
        "precio_minimo": precio_minimo,
        "precio_maximo": precio_maximo
    }

# Middleware para manejo de errores
@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "mensaje": "Error interno del servidor",
            "detalle": str(exc)
        }
    )

# Ejecutar la aplicación
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
