def error_boundary(func):
    from app.db.user import WrongPassword

    async def wrapper(*args, **kwargs) -> None:
        from app.db.db_setup import db

        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if e == "Bad password":
                raise WrongPassword
            print(e)
            db.rollback()
            db.commit()
    return wrapper
