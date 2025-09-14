from mangum import Mangum

from app.main import app

# API Gateway(HTTP API) → Lambda から FastAPI へブリッジ
handler = Mangum(app)
