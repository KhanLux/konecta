#!/bin/bash

# Ejemplos de uso de la API REST con curl

echo "=== Konecta API REST - Ejemplos de Uso ==="
echo ""

# 1. Health Check
echo "1. Health Check:"
curl -X GET "http://localhost:8000/health"
echo -e "\n"

# 2. Obtener todos los items
echo "2. Obtener todos los items:"
curl -X GET "http://localhost:8000/api/items"
echo -e "\n"

# 3. Obtener items disponibles
echo "3. Obtener items disponibles:"
curl -X GET "http://localhost:8000/api/items?disponible=true"
echo -e "\n"

# 4. Obtener items por rango de precio
echo "4. Obtener items entre $40 y $50:"
curl -X GET "http://localhost:8000/api/items?precio_min=40&precio_max=50"
echo -e "\n"

# 5. Obtener un item específico
echo "5. Obtener item con ID 1:"
curl -X GET "http://localhost:8000/api/items/1"
echo -e "\n"

# 6. Crear un nuevo item
echo "6. Crear nuevo item:"
curl -X POST "http://localhost:8000/api/items" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Teclado Mecánico",
    "descripcion": "Teclado RGB para gaming",
    "precio": 89.99,
    "disponible": true
  }'
echo -e "\n"

# 7. Actualizar un item completo
echo "7. Actualizar item con ID 1:"
curl -X PUT "http://localhost:8000/api/items/1" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Laptop HP Actualizada",
    "descripcion": "Laptop para trabajo profesional - Actualizada",
    "precio": 1350.00,
    "disponible": true
  }'
echo -e "\n"

# 8. Actualizar disponibilidad
echo "8. Actualizar disponibilidad del item 2:"
curl -X PATCH "http://localhost:8000/api/items/2/disponibilidad?disponible=false"
echo -e "\n"

# 9. Obtener estadísticas
echo "9. Obtener estadísticas:"
curl -X GET "http://localhost:8000/api/stats"
echo -e "\n"

# 10. Eliminar un item
echo "10. Eliminar item (comentado por seguridad):"
echo "# curl -X DELETE \"http://localhost:8000/api/items/3\""
echo -e "\n"

echo "=== Fin de los ejemplos ==="
echo "Para ver la documentación interactiva, visita: http://localhost:8000/docs"
