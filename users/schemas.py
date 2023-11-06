from marshmallow import fields, Schema
from marshmallow.validate import Length, Email


class UserSchema(Schema):
    class Meta:
        strict = True

    id = fields.String()
    username = fields.String()
    email = fields.String()
    createdOn = fields.String(attribute="created_on")
    updatedOn = fields.String(attribute="updated_on")
    bio = fields.String()


class CreateUserFormSchema(Schema):
    username = fields.Str(required=True, validate=Length(min=2, max=128))
    email = fields.Str(required=True, validate=Email())
    bio = fields.Str(required=False, validate=Length(min=10, max=1024))

    class Meta:
        fields = ("username", "bio", "email")


class UpdateUserFormSchema(Schema):
    username = fields.Str(required=False, validate=Length(min=2, max=128))
    email = fields.Str(required=False, validate=Email())
    bio = fields.Str(required=False, validate=Length(min=10, max=1024))

    class Meta:
        fields = ("username", "bio", "email")
