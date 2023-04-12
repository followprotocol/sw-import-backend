import uuid, httpx, jwt, time
from expiringdict import ExpiringDict
from random import choice
from ...utils.captcha_list import captcha_list
from loguru import logger

"""
captchaId will be saved in memory for 120 seconds
when this limit is reached the cache will start dumping items from itself to make room = memory safe
"""
cache = ExpiringDict(max_len=5000, max_age_seconds=120)

class captcha():
  def __init__(self):
    self.captchas = {}

  def generate(self, length:int):
    try:
      self.length = length
      if self.length is None:
        raise Exception("captcha length cannot be None") 

      while len(self.captchas) < self.length:
        self.random_captcha = choice(list(captcha_list.items()))
        self.captchas[self.random_captcha[0]] = self.random_captcha[1]

      self.captcha_solution = choice(list(self.captchas.keys()))
      self.solution_index_secret = list(self.captchas.keys()).index(self.captcha_solution)
      self.captchaId = str(uuid.uuid4().hex)
      cache[self.captchaId] = self.solution_index_secret

      base64_list = list(self.captchas.values())

      print(f"Adding to cache {self.captchaId}:{self.solution_index_secret}")

      # solution, id, base64
      return self.captcha_solution, self.captchaId, base64_list

    except Exception as e:
      logger.error(f"generate_captcha-> {e}")
      return False
    finally:
      del self.captchas

  """
  deletes an item from our cache
  """
  def delete(self, captchaId) -> None:
    cache.pop(captchaId)

  """
  checks whether an item exists or not
  """
  def check(self, captchaId, solution) -> bool:
    try:
      if int(cache.get(captchaId)) == int(solution):
        return True
      else:
        raise Exception()
    except:
      return False
    
"""
checks recaptcha v3
"""
def check_recpatcha_v3(token, secret_key, min_score) -> bool:
  try:
    response = httpx.post("https://www.google.com/recaptcha/api/siteverify", 
                            data = {"response": token,"secret": secret_key}, 
                            timeout=30)
    response_json = response.json()         
    success = response_json["success"]
    score = response_json["score"]
    if success == True and score >= min_score:
          return True
    else:
      raise Exception()
  except:
    return False
    
"""
jwt will expire after 30 seconds
"""    
def sign_jwt(jwt_secret, jwt_algorithm):
  payload = {
      "valid_until": time.time() + 30
  }
  token = jwt.encode(payload, jwt_secret, algorithm=jwt_algorithm)
  return token