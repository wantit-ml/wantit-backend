def error_boundary(func):
    async def wrapper(*args, **kwargs) -> None:
        from app.db.db_setup import db

        try:
            await func(*args, **kwargs)
        except Exception as e:
            print(e)
            db.rollback()
            db.commit()
    return wrapper
