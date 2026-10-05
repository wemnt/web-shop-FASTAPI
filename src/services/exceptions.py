class AppError(Exception):
    pass


class UserAlreadyExistsError(AppError):
    pass


class UserNotFoundError(AppError):
    pass
