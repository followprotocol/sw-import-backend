from fastapi import APIRouter, HTTPException, Request, Response
from .captchaService import *
from ...config import CAPTCHA_LENGTH, RECAPTCHA_V3_SECRET_KEY, RECAPTCHA_V3_MINIMUM_SCORE, JWT_SECRET_KEY, JWT_ALGORITHM

router = APIRouter()

@router.get("/captcha", status_code=201)
async def get_captcha(response: Response):
    generated_captcha = captcha().generate(CAPTCHA_LENGTH)
    if generated_captcha:
        response.set_cookie(key="captcha_id", value=generated_captcha[1], httponly=True, samesite="none", secure=True)
        return {
            "success": "true",
            "solution": f"Please select the {generated_captcha[0]}:",
            "captchas": generated_captcha[2]
        }
    else:
        raise HTTPException(500, detail="Something went wrong, try again later")

@router.post("/captcha/{solution}/{recaptchav3Solution}", status_code=200)
async def check_captcha(request: Request, solution:int, recaptchav3Solution:str):
    captcha_id = request.cookies.get("captcha_id")
    if captcha_id:
        if captcha().check(captcha_id, solution):
            captcha().delete(captcha_id)
            if check_recpatcha_v3(recaptchav3Solution, RECAPTCHA_V3_SECRET_KEY, RECAPTCHA_V3_MINIMUM_SCORE):
                token = sign_jwt(JWT_SECRET_KEY, JWT_ALGORITHM)
                return {
                    "success": "true",
                    "token": token
                }
            else:
                return {
                    "success" : "false",
                    "detail": "invalid recaptcha"
                }
        else:
            captcha().delete(captcha_id)
            return {
                "success": "false",
                "detail": "captcha expired or invalid"
            }
    else:
        return {
                "success": "false",
                "detail": "invalid captcha_id"
            }