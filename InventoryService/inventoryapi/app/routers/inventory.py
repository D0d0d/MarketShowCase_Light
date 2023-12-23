from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from ..database import get_db

router = APIRouter()


@router.get('/', response_model=schemas.ListInventory)
def get_inventory(db: Session = Depends(get_db), limit: int = 10,
                  page: int = 1,
                  search: str = ''):
    skip = (page - 1) * limit

    inventory = db.query(
        models.Inventory).group_by(
            models.Inventory.id).filter(
                models.Inventory.name.contains(search)).limit(
                    limit).offset(skip).all()
    return {'status': 'success', 'results': len(inventory),
            'Inventory': inventory}


@router.post('/', status_code=status.HTTP_201_CREATED,
             response_model=schemas.InventoryResponse)
def create_inventory(inventory: schemas.CreateInventory,
                     db: Session = Depends(get_db)):
    new_inventory = models.Inventory(**inventory.dict())
    db.add(new_inventory)
    db.commit()
    db.refresh(new_inventory)
    return new_inventory


@router.put('/{id}', response_model=schemas.InventoryResponse)
def reserve_inventory(id: str, inventory: schemas.UpdateInventory,
                      db: Session = Depends(get_db)):
    inventory_query = db.query(models.Inventory).filter(
        models.Inventory.id == id)
    updated_inventory = inventory_query.first()

    if not updated_inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No inventory with this id: {id} found')
    inventory_query.update(inventory.dict(exclude_unset=True),
                           synchronize_session=False)
    db.commit()
    return updated_inventory


@router.patch('/{id}/', response_model=schemas.InventoryResponse)
def update_inventory(id: str, reserve: int = 0,
                     db: Session = Depends(get_db)):
    inventory_query = db.query(models.Inventory).filter(models.Inventory.id == id)
    updated_inventory = inventory_query.first()

    if not updated_inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No inventory with id "{id}" found')
    required = updated_inventory.reserved+reserve
    if required > updated_inventory.amount or required < 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Not enough in storage: max [{updated_inventory.amount}] and [{required}] is required')
    updated_inventory.reserved = required
    db.add(updated_inventory)
    db.commit()
    return updated_inventory


@router.get('/{id}', response_model=schemas.InventoryResponse)
def get_inventory_id(id: str, db: Session = Depends(get_db)):
    inventory = db.query(models.Inventory).filter(
        models.Inventory.id == id).first()
    if not inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No inventory with this id: {id} found")
    return inventory


@router.delete('/{id}')
def delete_inventory(id: str, db: Session = Depends(get_db)):
    inventory_query = db.query(models.Inventory).filter(
        models.Inventory.id == id)
    inventory = inventory_query.first()
    if not inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No inventory with this id: {id} found')

    inventory_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
