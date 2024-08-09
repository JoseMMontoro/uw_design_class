from fastapi import FastAPI

import uw_design_class.database_connection as connection
from uw_design_class.routers import blog_entries

app = FastAPI()

connection.Base.metadata.create_all(bind=connection.engine)

app.include_router(blog_entries.router)

@app.get("/")
def read_root():
    return {"Hello": "Welcome to the Blog API"}