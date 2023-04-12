import uvicorn
from api.app import create_app
from api.config import ENV, APP_PORT

api = create_app()

if __name__ == "__main__":
    signature = f"""
               __
             <(o )___
              ( ._> /
               `---'

            -- {ENV} --
            Live at port: {APP_PORT}
            """
    
    print(signature)

    if ENV == "PROD":
        uvicorn.run("main:api", host="0.0.0.0", port=int(APP_PORT), server_header=False)
    else:
        uvicorn.run("main:api", host="0.0.0.0", port=int(APP_PORT), reload=True)