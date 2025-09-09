"""Entry point to the API."""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from exceptions import BaseCustomException
from routes import user, activity_levels, training_plan


app = FastAPI()


@app.exception_handler(BaseCustomException)
async def handle_custom_exceptions(request: Request,
                                   exc: BaseCustomException) -> JSONResponse:
    """
    Handle all custom exceptions.

    All defined exceptions in `exceptions.py` will be handled here.
    """
    return JSONResponse(
        status_code=exc.status,
        content={
            "message": exc.message,
            "type": exc.__class__.__name__,
            "detail": str(exc)
        }
    )


# include routers here
app.include_router(user.router)
app.include_router(activity_levels.router)
app.include_router(training_plan.router)

# for launching
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
