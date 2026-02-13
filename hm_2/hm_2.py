
import re
from pydantic import BaseModel, EmailStr, Field, ValidationError, field_validator, model_validator
import json


# -----------------------
# Модель Address
# -----------------------

class Address(BaseModel):
    city: str = Field(..., min_length=2)
    street: str = Field(..., min_length=3)
    house_number: int = Field(gt=0)


# -----------------------
# Модель User
# -----------------------

class User(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(ge=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address

    # Проверка: имя только из букв и пробелов
    @field_validator("name")
    @classmethod
    def name_must_contain_only_letters(cls, value):
        if not re.fullmatch(r"[A-Za-z\s]+", value):
            raise ValueError("Name must contain only letters and spaces")

        # for word in splitted_name:
        #     if not word.isalpha():
        #         raise ValueError("Name must contain only letters and spaces")
        return value   # функция должна возвращать значение - в противном случаи Ошибка

    # Кастомная валидация возраста и занятости
    @model_validator(mode="after")   # after (преобразованные) | before (сырые данные) - мы получим ДО преобразования, или ПОСЛЕ преобразования типа
    def check_employment_age(self):   # self - объект класса User
        if self.is_employed:
            if not (18 <= self.age <= 65):
                raise ValueError(
                    "If user is employed, age must be between 18 and 65"
                )
        return self


# -----------------------
# Функция обработки JSON
# -----------------------

def register_user(json_string: str) -> str:
    try:
        # Десериализация и валидация
        user = User.model_validate_json(json_string)

        # Сериализация обратно в JSON
        return user.model_dump_json(indent=4)

    except ValidationError as e:
        return f"Validation error:\n{e}"

# Успешная регистрация

valid_json = """
{
    "name": "John Doe",
    "age": 30,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "Berlin",
        "street": "Main Street",
        "house_number": 10
    }
}
"""

# Ошибка: возраст не соответствует занятости

invalid_age_json = """
{
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "Berlin",
        "street": "Main Street",
        "house_number": 10
    }
}
"""

# Ошибка: имя содержит цифры

invalid_name_json = """
{
    "name": "John123",
    "age": 25,
    "email": "john.doe@example.com",
    "is_employed": false,
    "address": {
        "city": "Berlin",
        "street": "Main Street",
        "house_number": 10
    }
}
"""