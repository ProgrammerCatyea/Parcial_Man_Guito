from fastapi import HTTPException, status

def not_found(entity: str):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{entity} no encontrado")

def conflict(detail: str):
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)

def bad_request(detail: str):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
