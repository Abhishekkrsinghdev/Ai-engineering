from pydantic import BaseModel, Field, EmailStr, field_validator

class User(BaseModel):
    id: int = Field(gt=0, description="The Positive integer ID of the user")
    name: str = Field(min_length=3, description="The name of the user")
    email: EmailStr
    age: int = Field(gt=0, lt=200, description="The age of the user")
    is_active: bool = True
    username: str = Field(alias="userName")

    @field_validator("username")
    @classmethod
    def validate_username_must_be_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("Username must be alphanumeric")
        return v.lower()

user = User(id=1, name="John Doe", email="john.doe@eample.com",age=100,userName="john1")

print(user)

print(user.name)
print(user.email)
print(user.is_active)

raw_data = {
    "id": 2,
    "name": "Adam",
    "email": "adam.smith@example.com",
    "is_active": False,
    "age": 45,
    "userName": "adam34"
}

# user2 = User(**raw_data)
user2 = User.model_validate(raw_data)
print(user2.model_dump_json(by_alias=True))