from fastapi import Depends, FastAPI

from uw_design_class.database_setup import get_db
from uw_design_class.views import router as view_router

app = FastAPI()

# Include routers
app.include_router(view_router, dependencies=[Depends(get_db)])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)