from pydantic import BaseModel, Field, validator
from typing import Optional

class GameCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    genero: str = Field(..., min_length=2)
    plataforma: str
    ano_lancamento: int = Field(..., ge=1958, le=2025)
    nota_pessoal: float = Field(..., ge=0, le=10)
    
    @validator('nome')
    def nome_nao_pode_ser_vazio(cls, v):
        if not v.strip():
            raise ValueError('Bota um nome de verdade')
        return v.strip()

class GameResponse(BaseModel):
    id: int
    nome: str
    genero: str
    plataforma: str
    ano_lancamento: int
    nota_pessoal: float