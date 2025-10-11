import re
import phonenumbers
from functools import wraps
from flask import request, jsonify
from email_validator import validate_email, EmailNotValidError
from marshmallow import Schema, fields, validate, ValidationError, pre_load
from datetime import datetime, timedelta

class BaseValidator:
    """Base validator class with common validation methods"""

    @staticmethod
    def validate_email_format(email):
        """Validate email format"""
        try:
            valid = validate_email(email)
            return valid.email
        except EmailNotValidError:
            raise ValidationError("Invalid email format")

    @staticmethod
    def validate_phone_number(phone, country_code='IN'):
        """Validate phone number format"""
        try:
            parsed_number = phonenumbers.parse(phone, country_code)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValidationError("Invalid phone number")
            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException:
            raise ValidationError("Invalid phone number format")

    @staticmethod
    def validate_password_strength(password):
        """Validate password strength"""
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")

        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter")

        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter")

        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one digit")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Password must contain at least one special character")

        return password

    @staticmethod
    def validate_indian_pincode(pincode):
        """Validate Indian pincode format"""
        if not re.match(r'^[1-9][0-9]{5}$', str(pincode)):
            raise ValidationError("Invalid pincode format")
        return str(pincode)

# User Registration Schema
class UserRegistrationSchema(Schema):
    full_name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    confirm_password = fields.Str(required=True)
    address = fields.Str(required=False, validate=validate.Length(max=500))
    pincode = fields.Str(required=False)
    city = fields.Str(required=False, validate=validate.Length(max=50))
    state = fields.Str(required=False, validate=validate.Length(max=50))
    role = fields.Str(load_default='user', validate=validate.OneOf(['user', 'service_provider']))
    terms_accepted = fields.Bool(required=True, validate=validate.Equal(True))

    @pre_load
    def validate_passwords_match(self, data, **kwargs):
        if data.get('password') != data.get('confirm_password'):
            raise ValidationError('Passwords do not match')
        return data

    def validate_email(self, value):
        return BaseValidator.validate_email_format(value)

    def validate_phone(self, value):
        return BaseValidator.validate_phone_number(value)

    def validate_password(self, value):
        return BaseValidator.validate_password_strength(value)

    def validate_pincode(self, value):
        if value:
            return BaseValidator.validate_indian_pincode(value)

# User Login Schema
class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=1))
    remember_me = fields.Bool(load_default=False)

# User Profile Update Schema
class UserProfileUpdateSchema(Schema):
    full_name = fields.Str(validate=validate.Length(min=2, max=100))
    phone = fields.Str()
    address = fields.Str(validate=validate.Length(max=500))
    pincode = fields.Str()
    city = fields.Str(validate=validate.Length(max=50))
    state = fields.Str(validate=validate.Length(max=50))
    avatar_url = fields.Url()

    def validate_phone(self, value):
        if value:
            return BaseValidator.validate_phone_number(value)

    def validate_pincode(self, value):
        if value:
            return BaseValidator.validate_indian_pincode(value)

# Password Change Schema
class PasswordChangeSchema(Schema):
    current_password = fields.Str(required=True)
    new_password = fields.Str(required=True, validate=validate.Length(min=8))
    confirm_password = fields.Str(required=True)

    @pre_load
    def validate_passwords_match(self, data, **kwargs):
        if data.get('new_password') != data.get('confirm_password'):
            raise ValidationError('New passwords do not match')
        return data

    def validate_new_password(self, value):
        return BaseValidator.validate_password_strength(value)

# Booking Creation Schema
class BookingCreateSchema(Schema):
    service_provider_id = fields.Str(required=True)
    waste_type = fields.Str(required=True, validate=validate.OneOf(['plastic', 'organic', 'paper', 'glass', 'metal', 'e-waste']))
    quantity = fields.Str(required=True)
    pickup_address = fields.Str(required=True, validate=validate.Length(min=10, max=500))
    scheduled_date = fields.DateTime(required=True)
    scheduled_time_slot = fields.Str(required=True)
    special_instructions = fields.Str(validate=validate.Length(max=500))
    contact_person = fields.Str(validate=validate.Length(max=100))
    contact_phone = fields.Str()

    def validate_scheduled_date(self, value):
        if value <= datetime.now():
            raise ValidationError("Scheduled date must be in the future")
        if value > datetime.now() + timedelta(days=30):
            raise ValidationError("Scheduled date cannot be more than 30 days in advance")

    def validate_contact_phone(self, value):
        if value:
            return BaseValidator.validate_phone_number(value)

# Service Provider Registration Schema
class ServiceProviderSchema(Schema):
    business_name = fields.Str(required=True, validate=validate.Length(min=2, max=200))
    business_type = fields.Str(required=True, validate=validate.OneOf(['NGO', 'Private', 'Government', 'Cooperative']))
    specialities = fields.List(fields.Str(validate=validate.OneOf(['plastic', 'organic', 'paper', 'glass', 'metal', 'e-waste'])), required=True)
    license_number = fields.Str(required=True, validate=validate.Length(min=5, max=50))
    address = fields.Str(required=True, validate=validate.Length(min=10, max=500))
    city = fields.Str(required=True, validate=validate.Length(max=50))
    state = fields.Str(required=True, validate=validate.Length(max=50))
    pincode = fields.Str(required=True)
    contact_email = fields.Email(required=True)
    contact_phone = fields.Str(required=True)
    operating_hours = fields.Str(required=True)
    capacity_per_day = fields.Str(required=True)
    website_url = fields.Url()
    description = fields.Str(validate=validate.Length(max=1000))

    def validate_pincode(self, value):
        return BaseValidator.validate_indian_pincode(value)

    def validate_contact_phone(self, value):
        return BaseValidator.validate_phone_number(value)

    def validate_contact_email(self, value):
        return BaseValidator.validate_email_format(value)

# Review Schema
class ReviewSchema(Schema):
    rating = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    title = fields.Str(required=True, validate=validate.Length(min=5, max=100))
    comment = fields.Str(required=True, validate=validate.Length(min=10, max=1000))
    service_quality = fields.Int(validate=validate.Range(min=1, max=5))
    punctuality = fields.Int(validate=validate.Range(min=1, max=5))
    cleanliness = fields.Int(validate=validate.Range(min=1, max=5))
    communication = fields.Int(validate=validate.Range(min=1, max=5))

# Payment Schema
class PaymentSchema(Schema):
    booking_id = fields.Str(required=True)
    amount = fields.Float(required=True, validate=validate.Range(min=1))
    payment_method = fields.Str(required=True, validate=validate.OneOf(['card', 'upi', 'netbanking', 'wallet']))
    currency = fields.Str(load_default='INR', validate=validate.OneOf(['INR']))

# Validation helper functions
def validate_json_request(schema_class):
    """Decorator to validate JSON request data"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                schema = schema_class()
                data = request.get_json()

                if not data:
                    return jsonify({'error': 'No JSON data provided'}), 400

                validated_data = schema.load(data)
                request.validated_data = validated_data
                return f(*args, **kwargs)

            except ValidationError as err:
                return jsonify({
                    'error': 'Validation failed',
                    'messages': err.messages
                }), 400
            except Exception as e:
                return jsonify({'error': 'Invalid JSON format'}), 400
        return decorated_function
    return decorator

def validate_query_params(schema_class):
    """Decorator to validate query parameters"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                schema = schema_class()
                validated_data = schema.load(request.args)
                request.validated_query = validated_data
                return f(*args, **kwargs)

            except ValidationError as err:
                return jsonify({
                    'error': 'Invalid query parameters',
                    'messages': err.messages
                }), 400
        return decorated_function
    return decorator
