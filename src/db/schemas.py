from pydantic import BaseModel

class ImportRecord(BaseModel):
    year: int
    month: int
    originName: str
    originTypeName: str
    destinationName: str
    destinationTypeName: str
    gradeName: str
    quantity: int

    class Config:
        from_attributes=True

    def to_dict(self) -> dict:
        """Summary:
            Convert self to dictionary
        Returns:
            dict: Same attributes
        """
        return {
            'year': self.year,
            'month': self.month,
            'originName': self.originName,
            'originTypeName': self.originTypeName,
            'destinationName': self.destinationName,
            'destinationTypeName': self.destinationTypeName,
            'gradeName': self.gradeName,
            'quantity': self.quantity
        }


class ImportRecordResponse(ImportRecord):
    id: int
