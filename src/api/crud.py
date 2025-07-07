from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError
from src.db.models import USCrudeOilImport
from fastapi import HTTPException
import logging



logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)


def get_imports(db: Session, country: str=None, 
                limit: int=10, offset: int=0) -> list[USCrudeOilImport]:
    """Summary:
        Retrieve records from the USCrudeOilImport table
    Args:
        db (Session): 
        country (str, optional): . Defaults to None.
        limit (int, optional): . Defaults to 10.
        offset (int, optional): . Defaults to 0.
    Returns:
        list[USCrudeOilImport]: retrieved records based on the filters provided 
    """
    query = db.query(USCrudeOilImport)
    if country:
        query = query.filter(USCrudeOilImport.originName == country)
    return query.offset(offset).limit(limit).all()


def find_record(record_id:int, db:Session) -> USCrudeOilImport|None:
    """Summary:
        
    Args:
        record_id (int): 
        db (Session): 
    Returns:
        USCrudeOilImport|None: 
    """
    record = None
    try:
        record = db.query(USCrudeOilImport).get(record_id)
    except Exception as ex:
        logger.error(f'find_record record_id={record_id}: {ex}')
    if record is None:
        raise HTTPException(404, detail=f"Unable to find record matching id: {record_id}")
    return record


def create_import(data:dict, db:Session) -> USCrudeOilImport:
    """Summary:
        Parse data arg into a database record and insert 
    Args:
        data (dict): Match structure of ImportRecord
    Returns:
        USCrudeOilImport: newly created record if successful
    """
    try:
        logger.info(data)
        new_record = USCrudeOilImport(**data)
    except Exception as ex:
        logger.error(f'create_import -> {ex}')
        raise HTTPException(status_code=400, detail=f"Unable to parse request: {ex}")
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    logger.info(f'Created new record: {new_record.id}')
    return new_record


def update_import(record_id:int, data:dict, db:Session) -> USCrudeOilImport|None:
    """Summary:
        Check database for record_id and update if found
    Args:
        record_id (int): ID of record to be updated
        data (dict): new data to replace existing values
        db (Session): 
    Returns:
        USCrudeOilImport: Updated record
    """
    db_record = None
    try:
        print('checking records')
        logger.info(f'checking the dang records {data}')
        db_record = db.query(USCrudeOilImport).get(record_id)
        print('found the dang record')
    except Exception as ex:
        logger.error(f'update_import {ex}')
        raise HTTPException(status_code=404, detail=f"Record not found: {ex}")
    try:
        for key, value in data.items():
            setattr(db_record, key, value)
        db.commit()
        db.refresh(db_record)
    except Exception as ex:
        logger.error(f'update_import -> {ex}')
        raise HTTPException(status_code=500, detail=f"Unable to parse input: {ex}")
    return db_record


def delete_import(record_id:int, db:Session) -> USCrudeOilImport:
    """Summary:
        Delete the record matching to provided record_id
    Args:
        record_id (int): 
        db (Session): 
    Returns:
        USCrudeOilImport: 
    """
    db_record = None
    try:
        db_record = db.query(USCrudeOilImport).get(record_id)
        db.delete(db_record)
        logger.info(f'Deleted record: {db_record}')
        db.commit()
    except UnmappedInstanceError as ex:
        raise HTTPException(status_code=404, detail=f"Record {record_id} does not exist. {ex}")
    except Exception as ex:
        logger.error(f"delete_import: {ex}")
        raise HTTPException(status_code=500, detail=f"Unable to delete record {record_id}: {ex}")
    return db_record
