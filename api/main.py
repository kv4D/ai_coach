"""Entry point to the API."""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from exceptions import NotFoundError, AlreadyExistError
from routes import user, activity_levels, training_plan


app = FastAPI()


@app.get('')
def ping() -> str:
    """Test endpoint."""
    return 'Hello, User'

# include exception handlers here
@app.exception_handler(NotFoundError)
async def not_found_error_handler(request: Request, 
                                  exc: NotFoundError) -> JSONResponse:
    """
    Handle NotFoundError.
    This exception appears when no such resource or no data found.
    """
    return JSONResponse(status_code=404, 
                        content={"message": str(exc)})

@app.exception_handler(AlreadyExistError)
async def already_exists_error_handler(request: Request, 
                                       exc: AlreadyExistError) -> JSONResponse:
    """
    Handle AlreadyExistsError.
    This exception appears when you try to add already existing data.
    """
    return JSONResponse(status_code=409, 
                        content={"message": str(exc)})

# include routers here
app.include_router(user.router)
app.include_router(activity_levels.router)
app.include_router(training_plan.router)

# for launching
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)