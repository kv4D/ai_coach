from fastapi import FastAPI
from routes import user


app = FastAPI()

# include routers here
app.include_router(user.router)

# for launching in development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)