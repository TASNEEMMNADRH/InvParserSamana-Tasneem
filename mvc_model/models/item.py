# models.py
from typing import List, Optional
from pytest import Session
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
# All models inherit from this base class
from base import Base
from models.invoice import get_invoice_by_id

class Item(Base):
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    InvoiceId = Column(String, ForeignKey('invoices.InvoiceId'))
    Description = Column(String)
    Name = Column(String)
    Quantity = Column(Float)
    UnitPrice = Column(Float)
    Amount = Column(Float)
    
    invoice = relationship("Invoice", back_populates="items")

def create_item(db: Session, item_data: dict) -> Item:
    invoice = get_invoice_by_id(db,item_data.get("InvoiceId"))
    if invoice :
        item = Item(
            InvoiceId = item_data.get("InvoiceId"),
            Description = item_data.get("Description"),
            Name =  item_data.get("Name"),
            Quantity =  item_data.get("Quantity"),
            UnitPrice =  item_data.get("UnitPrice"),
            Amount =  item_data.get("Amount")
        )
        db.add(item)
        db.commit()
        return item
    return None



def get_item_by_id(db: Session, item_id: int) -> Optional[Item]:
    item = db.query(Item).filter(Item.InvoiceId==item_id).first()
    return item


def get_items_by_invoice_id(db: Session, invoice_id: str) -> List[Item]:
    items = db.query(Item).filter(Item.InvoiceId==invoice_id).all()
    return items


def get_items(db: Session) -> List[Item]:
     items = db.query(Item).all()
     return items


def update_item(db: Session, item_id: int, update_data: dict) -> Optional[Item]:
    item = get_item_by_id(db, item_id)
    if not item:
        return None

    if "InvoiceId" in update_data:
        item.InvoiceId = update_data["InvoiceId"]
    if "Description" in update_data:
        item.Description = update_data["Description"]
    if "Name" in update_data:
        item.Name = update_data["Name"]
    if "Quantity" in update_data:
        item.Quantity = update_data["Quantity"]
    if "UnitPrice" in update_data:
        item.UnitPrice = update_data["UnitPrice"]
    if "Amount" in update_data:
        item.Amount = update_data["Amount"]

    db.commit()
    db.refresh(item)
    return item



def delete_item(db: Session, item_id: int) -> bool:
    item = get_item_by_id(db,item_id)
    if item : 
        db.delete(item)
        db.commit()
        return True
    return False