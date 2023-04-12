import jwt, time
from fastapi import APIRouter, HTTPException, Depends, Request
from .getinfoService import miniMania
from uuid import UUID
from ...config import JWT_SECRET_KEY, JWT_ALGORITHM

router = APIRouter()

def check_uuid(id):
    try:
        UUID(str(id))
        return True
    except ValueError:
        return False

def verify_token(req: Request):
    try:
        token = req.headers["Authorization"]
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        if time.time() <= decoded_token["valid_until"]:
          return True
        else:
          raise Exception()
    except:
      return False    

@router.post("/getinfo/{sessionID}", status_code=200)
async def player_information(sessionID, authorized: bool = Depends(verify_token)):
    if authorized:
        if check_uuid(sessionID):
            response = await miniMania(sessionID).get_player_info()
            if response:
                return {
                    "success": "true",
                    "detail": response
                }
            else:
                raise HTTPException(500, detail="something went wrong, try again later")
        else:
            raise HTTPException(400, detail="invalid sessionID")
    else:
        return {
                    "success": "false",
                    "detail": "invalid or expired token"
                }