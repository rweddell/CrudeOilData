from fastapi import APIRouter, Depends, Query, Request, Path
from sqlalchemy.orm import Session
from typing import List
from src.db.schemas import ImportRecord, ImportRecordResponse
from src.api.crud import get_imports, create_import, update_import, delete_import, find_record
from src.db.database import get_db


api_router = APIRouter()


@api_router.get("/imports", response_model=List[ImportRecordResponse])
def list_imports(
    country: str = Query(None),
    limit: int = Query(100, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
) -> List[ImportRecordResponse]:
    """Summary:
        Returns all records form the USCrudOilImports table based on provided filters.
    Args:
        country (str, optional): Country name.
        limit (int, optional): Limit to query result count. Defaults to 100.
        offset (int, optional): Previous result point. Defaults to 0.
    Returns:
        List[ImportRecordResponse]: Records matching the query filters.
    """

    return get_imports(db=db, country=country, limit=limit, offset=offset)


@api_router.get("/imports/find/{record_id}", response_model=ImportRecordResponse)
def find_import_record(record_id:int=Path(), db:Session=Depends(get_db)) -> ImportRecordResponse|None:
    """Summary:
        Retrieves record with id matching provided record_id.
    Args:
        record_id (int): Path parameter. ID of desired record.
    Returns:
        ImportRecordResponse|None: Matched record or None.
    """
    return find_record(record_id, db)


@api_router.post("/imports", response_model=ImportRecordResponse)
async def create_new_import(data:ImportRecord, db:Session=Depends(get_db)) -> ImportRecordResponse:
    """Summary:
        Parse incoming data into an ImportRecord, submit new record to database, and return response.
    Args:
        data (dict): Matches structure.
    Returns:
        ImportRecordResponse: Created record.
    """
    data = data.to_dict()
    result = create_import(data, db)
    return result


@api_router.put("/imports/update/{record_id}", response_model=ImportRecordResponse)
async def update_import_record(data:Request, record_id:int=Path(), db:Session=Depends(get_db)) -> ImportRecordResponse:
    """Summary:
        Update an existing record with new values. 
    Args:
        record_id (int): ID of record.
    Returns:
        ImportRecordResponse: Updated record data.
    """
    body = await data.json()
    return update_import(record_id, body, db)


@api_router.delete("/imports/delete/{record_id}", response_model=ImportRecordResponse)
def delete_import_record(record_id:int, db:Session=Depends(get_db)) -> ImportRecordResponse:
    """Summary:
        Delete the record associated with the record_id. 
    Args:
        record_id (int): ID of record to be deleted.
    Returns:
        ImportRecordResponse: Deleted record data.
    """
    return delete_import(record_id=record_id, db=db)
