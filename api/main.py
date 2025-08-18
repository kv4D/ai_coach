"""Entry point to the API."""
from fastapi import FastAPI
from exceptions import exception_handlers
from routes import user, activity_levels, training_plan


app = FastAPI(exception_handlers=exception_handlers)

# include routers here
app.include_router(user.router)
app.include_router(activity_levels.router)
app.include_router(training_plan.router)

# for launching
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)