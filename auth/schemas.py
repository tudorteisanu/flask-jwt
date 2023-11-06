from marshmallow import fields, Schema
from marshmallow.validate import Length, Email


class LoginFormSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

    class Meta:
        fields = ("username", "password")


class RegisterFormSchema(Schema):
    username = fields.Str(required=True, validate=Length(min=2, max=128))
    password = fields.Str(required=True, validate=Length(min=8, max=256))
    email = fields.Str(required=True, validate=Email())
    bio = fields.Str(required=False, validate=Length(min=10, max=1024))

    class Meta:
        fields = ("username", "password", "email", "bio")


class CurrentUserSchema(Schema):
    class Meta:
        strict = True

    id = fields.String()
    username = fields.String()
    email = fields.String()
    createdOn = fields.String(attribute="created_on")
    updatedOn = fields.String(attribute="updated_on")
    bio = fields.String()
