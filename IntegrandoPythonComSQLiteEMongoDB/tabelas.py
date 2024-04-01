"""Código desenvolvido para obtenção de progresso na plataforma DIO, no
curso Formação Python Developer."""

from sqlalchemy.orm import (
    DeclarativeBase,
    relationship,
    mapped_column
    )

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    ForeignKey
    )

class Base(DeclarativeBase):
    pass

class TipoCliente(Base):
    __tablename__ = "lst_Cliente_Tipo"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    descricao = mapped_column(String)
    cadastro = mapped_column(String)

class Cliente(Base):
    __tablename__ = "cad_Cliente"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome = mapped_column(String)
    endereco = mapped_column(String)
    numero_cadastro = Column(String)

    id_tipo = mapped_column(Integer, ForeignKey("lst_Cliente_Tipo.id"))

    tipo = relationship("TipoCliente")

class Conta(Base):
    __tablename__ = "cad_Conta"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    agencia = mapped_column(Integer)
    numero = mapped_column(Integer, unique=True)
    id_cliente = mapped_column(Integer, ForeignKey("cad_Cliente.id"))

    cliente = relationship("Cliente")

class TipoTransacao(Base):
    __tablename__ = "lst_Transacao_Tipo"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    descricao = mapped_column(String)
    multiplicador = mapped_column(Integer)

class Transacao(Base):
    __tablename__ = "rel_Transacao"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    valor = mapped_column(Float)
    id_tipo = mapped_column(Integer, ForeignKey("lst_Transacao_Tipo.id"))
    id_conta = mapped_column(Integer, ForeignKey("cad_Conta.id"))

    tipo = relationship("TipoTransacao")
    conta = relationship("Conta")

#    cliente = relationship(
#        "Cliente", back_populates="tipo", cascade="all, delete-orphan"
#    )

#   conta = relationship(
#        "Conta", back_populates="cliente", cascade="all, delete-orphan"
#    )
    
#    transacao = relationship(
#        "Transacao", back_populates="conta", cascade="all, delete-orphan"
#    )

#    transacao = relationship(
#        "Transacao", back_populates="tipo", cascade="all, delete-orphan"
#    )
