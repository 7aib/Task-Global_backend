import enum


class SalesChannel(str, enum.Enum):
    ONLINE = "online"
    RETAIL = "retail"
    EMAIL = "email"
    PHONE = "phone"
    SOCIAL_MEDIA = "social_media"
    OTHER = "other"

class InventoryStatus(enum.Enum):
    IN_STOCK = "in_stock"
    OUT_OF_STOCK = "out_of_stock"
    LOW_STOCK = "low_stock"
    DISCONTINUED = "discontinued"

class Quantity(enum.Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10