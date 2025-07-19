from fastapi import FastAPI
from routes import user, activity_levels, training_plan


app = FastAPI()

# include routers here
app.include_router(user.router)
app.include_router(activity_levels.router)
app.include_router(training_plan.router)

# for launching in development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)