class AppError(Exception):
    pass


class UserAlreadyExistsError(AppError):
    pass


class UserNotFoundError(AppError):
    pass


class IncorrectPasswordError(AppError):
    pass


class ProductNotFoundError(AppError):
    pass
