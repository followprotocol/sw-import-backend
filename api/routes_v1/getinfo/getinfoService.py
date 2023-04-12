import httpx, pyamf, re
from loguru import logger
from pyamf import remoting

class miniMania():
  def __init__(self, sessionID:str):
    self.sessionID = sessionID
    self.api = "https://api.minimania.app"
    self.gateway = "https://gateway.minimania.app/gateway/"
    self.headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) MiniMania/1.0.24 Chrome/85.0.4183.121 Electron/10.4.7 Safari/537.36",
    "content-type": "application/x-amf",
    "accept": "*/*",
    "origin": "https://cdn.minimania.app",
    "x-requested-with":	"ShockwaveFlash/20.0.0.306",
    "sec-fetch-site":	"cross-site",
    "sec-fetch-mode":	"no-cors",
    "sec-fetch-dest":	"embed",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US",
    }
    
    self.returnedData = {}

  async def get_player_info(self):
    try:
      self.headers["swsid"] = self.sessionID
      async with httpx.AsyncClient() as session:
          response = await session.get(f"{self.api}/api/user/me",
                                      headers=self.headers,
                                      timeout=30)
          if response.status_code == 200:
            response_json = response.json()
            defaultAvatar = response_json["defaultAvatar"]
            sex = response_json["sex"]
            goldBalance = response_json["goldBalance"]
            tokensBalance = response_json["tokensBalance"]
          else:
            raise Exception(f"MiniMania api user/me: {self.sessionID}-{response.status_code}-{response.text}")
          
          response = await session.get(f"{self.api}/api/avatar/{defaultAvatar}",
                                      headers=self.headers,
                                      timeout=30)
          if response.status_code == 200:
            response_json = response.json()
            snapUrl = "https://cdn.minimania.app/avatars/" + response_json["snapUrl"]
            firstName = response_json["firstName"]
            lastName = response_json["lastName"]
            cl = response_json["citizenLevel"]
            
          else:
            raise Exception(f"MiniMania api avatars: {response.status_code}-{response.text}")

          self.returnedData["defaultAvatar"] = defaultAvatar
          self.returnedData["snapUrl"] = snapUrl
          self.returnedData["firstName"] = firstName
          self.returnedData["lastName"] = lastName
          self.returnedData["sex"] = sex
          self.returnedData["cl"] = cl
          self.returnedData["goldBalance"] = goldBalance
          self.returnedData["tokensBalance"] = tokensBalance

          request = remoting.Request(target="item.inventory.getMyInventory", body=[])
          ev = remoting.Envelope(pyamf.AMF3)    
          ev["/0"] = request

          binMsg = remoting.encode(ev)
          binMsgValue = binMsg.getvalue()

          async with httpx.AsyncClient() as session:
            response = await session.post(f"{self.gateway}?jsessionid={self.sessionID}",
                                        data=binMsgValue, 
                                        headers=self.headers,
                                        timeout=30)

            content = remoting.decode(response.content)
            content = content["/0"]
            content = str(content)
            
            if response.status_code == 200:
              
              """
              unfortunately the response is not proper json
              so we have to handle it that way
              """
              itemsCount = len(re.findall("uid", content))
              if not itemsCount:
                raise Exception(f"could not parse itemsCount")
              
              goldValues = re.findall("(?<='valueGold':).?[0-9]+", content)
              if not goldValues:
                raise Exception(f"could not parse goldValues")
              totalItemsGoldValue=sum(int(i) for i in goldValues)

              tokensValues = re.findall("(?<='valueTokens':).?[0-9]+", content)
              if not tokensValues:
                raise Exception(f"could not parse tokensValues")
              totalItemsTokensValue=sum(int(i) for i in tokensValues)

              totalGoldNetworth = totalItemsGoldValue + goldBalance
              totalTokenNetworth = totalItemsTokensValue + tokensBalance

              self.returnedData["itemsCount"] = itemsCount
              self.returnedData["totalItemsGoldValue"] = totalItemsGoldValue
              self.returnedData["totalItemsTokensValue"] = totalItemsTokensValue

              self.returnedData["totalGoldNetworth"] = totalGoldNetworth
              self.returnedData["totalTokenNetworth"] = totalTokenNetworth

              return self.returnedData

            else:
              raise Exception(f"MiniMania Gateway (item.inventory.getMyInventory): {self.sessionID}-{response.status_code}-{content}")

    except Exception as e:
      logger.error(e)
      return False