from .util import env
import uvicorn
from .controllers.runner import *



if __name__ == "__main__":
    if env.ENVIRONMENT == 'dev':
        print(env.ENVIRONMENT)
        uvicorn.run("app.__main__:app", reload=True, host="0.0.0.0", port=env.HTTP_PORT, log_level="info")
    elif env.ENVIRONMENT == 'prod':
        print(env.ENVIRONMENT)
        uvicorn.run("app.__main__:app", reload=False, host="0.0.0.0", port=env.HTTP_PORT, log_level="info")
    else:
        print("Ambiente não definido")
