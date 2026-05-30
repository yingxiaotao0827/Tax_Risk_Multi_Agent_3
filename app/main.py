from fastapi import FastAPI

from tax_risk_ai.app.api.routes import router
from tax_risk_ai.app.core.logging import configure_logging

configure_logging()

app = FastAPI(title="Tax Risk AI", version="0.1.0")
app.include_router(router)

