def error_boundary(func):
    async def wrapper(*args, **kwargs) -> None:
        from sqlalchemy.exc import OperationalError, DatabaseError
        from app.db.db_setup import db
        from app.db.user import UserAlreadyExists, WrongPassword

        try:
            return await func(*args, **kwargs)
        except UserAlreadyExists:
            raise UserAlreadyExists
        except WrongPassword:
            raise WrongPassword
        except OperationalError:
            db.rollback()
            db.commit()
        except DatabaseError:
            db.rollback()
            db.commit()
    return wrapper
