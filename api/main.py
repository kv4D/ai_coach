from fastapi import FastAPI


app = FastAPI()

# include routers here

# for launching in development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)