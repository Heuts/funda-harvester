from dataclasses import dataclass
import decimal


@dataclass
class House:
    id: str
    streetAndHouseNumber: str
    postalCode: str
    city: str
    askingPrice: decimal
