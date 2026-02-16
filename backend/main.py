from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Permitir que el frontend hable con nosotros
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción esto se restringe
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de datos en memoria (para simplificar el ejemplo)
pedidos = [
    {"id": 1, "mesa": "Mesa 5", "plato": "Hamburguesa"},
    {"id": 2, "mesa": "Mesa 2", "plato": "Ensalada"}
]

class Pedido(BaseModel):
    mesa: str
    plato: str

@app.get("/api/pedidos")
def get_pedidos():
    return pedidos

@app.post("/api/pedidos")
def crear_pedido(pedido: Pedido):
    nuevo_pedido = pedido.dict()
    nuevo_pedido["id"] = len(pedidos) + 1
    pedidos.append(nuevo_pedido)
    return nuevo_pedido