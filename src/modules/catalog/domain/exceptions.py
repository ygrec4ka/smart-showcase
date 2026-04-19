class CatalogDomainError(Exception):
    """Базовое исключение для модуля каталога"""

    pass


class SkuAlreadyExistsError(CatalogDomainError):
    pass


class CategoryNotFoundError(CatalogDomainError):
    pass


class ProductNotFoundError(CatalogDomainError):
    pass
