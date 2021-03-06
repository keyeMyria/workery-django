# -*- coding: utf-8 -*-
import logging
import phonenumbers
from datetime import datetime, timedelta
from dateutil import tz
from starterkit.drf.validation import (
    MatchingDuelFieldsValidator,
    EnhancedPasswordStrengthFieldValidator
)
from starterkit.utils import (
    get_random_string,
    get_unique_username_from_email,
    int_or_none
)
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.db.models import Q, Prefetch
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.http import urlquote
from rest_framework import exceptions, serializers
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from shared_api.custom_fields import PhoneNumberField
from shared_foundation.constants import ASSOCIATE_GROUP_ID
from shared_foundation.models import SharedUser
from tenant_foundation.models import (
    Comment,
    StaffComment,
    Staff
)


logger = logging.getLogger(__name__)


class StaffListCreateSerializer(serializers.ModelSerializer):
    # OVERRIDE THE MODEL FIELDS AND ENFORCE THE FOLLOWING CUSTOM VALIDATION RULES.
    given_name = serializers.CharField(
        required=True,
        allow_blank=False,
    )
    last_name = serializers.CharField(
        required=True,
        allow_blank=False,
    )
    address_country = serializers.CharField(
        required=True,
        allow_blank=False,
    )
    address_region = serializers.CharField(
        required=True,
        allow_blank=False,
    )
    address_locality = serializers.CharField(
        required=True,
        allow_blank=False,
    )
    postal_code = serializers.CharField(
        required=True,
        allow_blank=False,
    )
    street_address = serializers.CharField(
        required=True,
        allow_blank=False,
    )

    # We are overriding the `email` field to include unique email validation.
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=SharedUser.objects.all())],
        required=True,
    )

    # All comments are created by our `create` function and not by
    # `django-rest-framework`.
    # comments = StaffCommentSerializer(many=True, read_only=True, allow_null=True)

    # This is a field used in the `create` function if the user enters a
    # comment. This field is *ONLY* to be used during the POST creation and
    # will be blank during GET.
    extra_comment = serializers.CharField(write_only=True, allow_null=True)

    # This field is used to assign the user to the group.
    account_type = serializers.CharField(
        write_only=True,
        allow_null=False,
        required=True
    )

    # Custom formatting of our telephone fields.
    fax_number = PhoneNumberField(allow_null=True, required=False)
    telephone = PhoneNumberField(allow_null=True, required=False)
    other_telephone = PhoneNumberField(allow_null=True, required=False)

    # Add password adding.
    password = serializers.CharField(
        write_only=True,
        required=True,
        allow_blank=False,
        max_length=63,
        style={'input_type': 'password'},
        validators = [
            MatchingDuelFieldsValidator(
                another_field='password_repeat',
                message=_("Inputted passwords fields do not match.")
            ),
            EnhancedPasswordStrengthFieldValidator()
        ]
    )
    password_repeat = serializers.CharField(
        write_only=True,
        required=True,
        allow_blank=False,
        max_length=63,
        style={'input_type': 'password'}
    )
    is_active = serializers.BooleanField(
        write_only=True,
        required=True,
        error_messages={
            "invalid": _("Please pick either 'Yes' or 'No' choice.")
        }
    )

    # Meta Information.
    class Meta:
        model = Staff
        fields = (
            # Thing
            'id',
            'created',
            'last_modified',
            'account_type',
            'description',

            # Person
            'given_name',
            'middle_name',
            'last_name',
            'birthdate',
            'join_date',
            'gender',

            # Misc (Read/Write)
            'tags',
            'is_active',

            # # Misc (Read Only)
            # 'comments',

            # Misc (Write Only)
            'extra_comment',
            'password',
            'password_repeat',

            # Contact Point
            'area_served',
            'available_language',
            'contact_type',
            'email',
            'personal_email',
            'fax_number',
            # 'hours_available', #TODO: FIX
            'telephone',
            'telephone_extension',
            'telephone_type_of',
            'other_telephone',
            'other_telephone_extension',
            'other_telephone_type_of',

            # Postal Address
            'address_country',
            'address_locality',
            'address_region',
            'post_office_box_number',
            'postal_code',
            'street_address',
            'street_address_extra',

            # Geo-coordinate
            'elevation',
            'latitude',
            'longitude',
            # 'location' #TODO: FIX
        )

    def validate_telephone(self, value):
        """
        Include validation on no-blanks
        """
        if value is None:
            raise serializers.ValidationError("This field may not be blank.")
        return value

    def validate_account_type(self, value):
        """
        Include validation for valid choices.
        """
        if int_or_none(value) is None:
            raise serializers.ValidationError("Please select a valid choice.")
        return value

    def setup_eager_loading(cls, queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related(
            'owner',
            'created_by',
            'last_modified_by',
            # 'comments'
            'tags',
        )
        return queryset

    def create(self, validated_data):
        """
        Override the `create` function to add extra functinality:

        - Create a `User` object in the public database.

        - Create a `SharedUser` object in the public database.

        - Create a `Staff` object in the tenant database.

        - If user has entered text in the 'extra_comment' field then we will
          a `Comment` object and attach it to the `Staff` object.

        - We will attach the staff user whom created this `Staff` object.
        """
        # Format our telephone(s)
        fax_number = validated_data.get('fax_number', None)
        if fax_number:
            fax_number = phonenumbers.parse(fax_number, "CA")
        telephone = validated_data.get('telephone', None)
        if telephone:
            telephone = phonenumbers.parse(telephone, "CA")
        other_telephone = validated_data.get('other_telephone', None)
        if other_telephone:
            other_telephone = phonenumbers.parse(other_telephone, "CA")

        validated_data['fax_number'] = fax_number
        validated_data['telephone'] = telephone
        validated_data['other_telephone'] = other_telephone

        # Extract our "email" field.
        email = validated_data.get('email', None)
        personal_email = validated_data.get('personal_email', None)

        #-------------------
        # Create our user.
        #-------------------

        owner = SharedUser.objects.create(
            first_name=validated_data['given_name'],
            last_name=validated_data['last_name'],
            email=email,
            is_active=validated_data['is_active'],
            franchise=self.context['franchise'],
            was_email_activated=True
        )
        logger.info("Created shared user.")

        # Attach the user to the `group` group.
        account_type = int_or_none(validated_data.get('account_type', None))
        if account_type:
            owner.groups.set([account_type])

        # Update the password.
        password = validated_data.get('password', None)
        owner.set_password(password)
        owner.save()

        #---------------------------------------------------
        # Create our `Staff` object in our tenant schema.
        #---------------------------------------------------

        # Create an "Staff".
        staff = Staff.objects.create(
            created_by=self.context['created_by'],
            last_modified_by=self.context['created_by'],
            description=validated_data.get('description', None),

            # Person
            given_name=validated_data['given_name'],
            last_name=validated_data['last_name'],
            middle_name=validated_data['middle_name'],
            birthdate=validated_data.get('birthdate', None),
            join_date=validated_data.get('join_date', None),
            gender=validated_data.get('gender', None),

            # Misc
            created_from = self.context['created_from'],
            created_from_is_public = self.context['created_from_is_public'],
            # . . .

            # Contact Point
            area_served=validated_data.get('area_served', None),
            available_language=validated_data.get('available_language', None),
            contact_type=validated_data.get('contact_type', None),
            email=email,
            personal_email=personal_email,
            fax_number=fax_number,
            # 'hours_available', #TODO: IMPLEMENT.
            telephone=telephone,
            telephone_extension=validated_data.get('telephone_extension', None),
            telephone_type_of=validated_data.get('telephone_type_of', None),
            other_telephone=other_telephone,
            other_telephone_extension=validated_data.get('other_telephone_extension', None),
            other_telephone_type_of=validated_data.get('other_telephone_type_of', None),

            # Postal Address
            address_country=validated_data.get('address_country', None),
            address_locality=validated_data.get('address_locality', None),
            address_region=validated_data.get('address_region', None),
            post_office_box_number=validated_data.get('post_office_box_number', None),
            postal_code=validated_data.get('postal_code', None),
            street_address=validated_data.get('street_address', None),
            street_address_extra=validated_data.get('street_address_extra', None),

            # Geo-coordinate
            elevation=validated_data.get('elevation', None),
            latitude=validated_data.get('latitude', None),
            longitude=validated_data.get('longitude', None),
            # 'location' #TODO: IMPLEMENT.
        )
        logger.info("Created staff member.")

        # Update our staff again.
        staff.owner = owner
        staff.email = email
        staff.save()
        logger.info("Attached user object to staff member.")

        #------------------------
        # Set our `Tag` objects.
        #------------------------
        tags = validated_data.get('tags', None)
        if tags is not None:
            if len(tags) > 0:
                staff.tags.set(tags)

        #-----------------------------
        # Create our `Comment` object.
        #-----------------------------
        extra_comment = validated_data.get('extra_comment', None)
        if extra_comment is not None:
            comment = Comment.objects.create(
                created_by=self.context['created_by'],
                last_modified_by=self.context['created_by'],
                text=extra_comment,
                created_from = self.context['created_from'],
                created_from_is_public = self.context['created_from_is_public']
            )
            staff_comment = StaffComment.objects.create(
                about=staff,
                comment=comment,
            )

        # Update validation data.
        # validated_data['comments'] = StaffComment.objects.filter(staff=staff)
        validated_data['created_by'] = self.context['created_by']
        validated_data['last_modified_by'] = self.context['created_by']
        validated_data['extra_comment'] = None
        validated_data['id'] = staff.id

        # Return our validated data.
        return validated_data


class StaffRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    # owner = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    # We are overriding the `email` field to include unique email validation.
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=Staff.objects.all())],
        required=False
    )
    personal_email = serializers.EmailField(
        validators=[UniqueValidator(queryset=Staff.objects.all())],
        required=False
    )

    # Add password adding.
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        max_length=63,
        style={'input_type': 'password'},
        validators = [
            MatchingDuelFieldsValidator(
                another_field='password_repeat',
                message=_("Inputted passwords fields do not match.")
            ),
            EnhancedPasswordStrengthFieldValidator()
        ]
    )
    password_repeat = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        max_length=63,
        style={'input_type': 'password'}
    )
    is_active = serializers.BooleanField(
        write_only=True,
        required=True,
        error_messages={
            "invalid": _("Please pick either 'Yes' or 'No' choice.")
        }
    )

    # This field is used to assign the user to the group.
    account_type = serializers.CharField(
        write_only=True,
        allow_null=False,
        required=True
    )


    # All comments are created by our `create` function and not by
    # # `django-rest-framework`.
    # comments = StaffCommentSerializer(many=True, read_only=True)
    #
    # # This is a field used in the `create` function if the user enters a
    # # comment. This field is *ONLY* to be used during the POST creation and
    # # will be blank during GET.
    # extra_comment = serializers.CharField(write_only=True, allow_null=True)

    # Custom formatting of our telephone fields.
    fax_number = PhoneNumberField(allow_null=True, required=False)
    telephone = PhoneNumberField(allow_null=True, required=False)
    other_telephone = PhoneNumberField(allow_null=True, required=False)

    # Meta Information.
    class Meta:
        model = Staff
        fields = (
            # Thing
            'id',
            'created',
            'last_modified',
            # 'owner',
            'description',
            'account_type',

            # Person
            'given_name',
            'middle_name',
            'last_name',
            'birthdate',
            'join_date',
            'gender',

            # Misc (Read/Write)
            'tags',
            'is_active',
            # # 'is_senior',
            # # 'is_support',
            # # 'job_info_read',
            # 'how_hear',
            #
            # # Misc (Read Only)
            # 'comments',
            #
            # # Misc (Write Only)
            'password',
            'password_repeat',
            # 'extra_comment',

            # Contact Point
            'area_served',
            'available_language',
            'contact_type',
            'email',
            'personal_email',
            'fax_number',
            # 'hours_available', #TODO: FIX
            'telephone',
            'telephone_extension',
            'telephone_type_of',
            'other_telephone',
            'other_telephone_extension',
            'other_telephone_type_of',

            # Postal Address
            'address_country',
            'address_locality',
            'address_region',
            'post_office_box_number',
            'postal_code',
            'street_address',
            'street_address_extra',

            # Geo-coordinate
            'elevation',
            'latitude',
            'longitude',
            # 'location' #TODO: FIX
        )

    def setup_eager_loading(cls, queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related(
            'owner',
            'created_by',
            'last_modified_by',
            # 'comments'
            'tags',
        )
        return queryset

    def validate_account_type(self, value):
        """
        Include validation for valid choices.
        """
        if int_or_none(value) is None:
            raise serializers.ValidationError("Please select a valid choice.")
        return value

    def validate_personal_email(self, value):
        """
        Include validation for valid choices.
        """
        if value is None or value == '':
            raise serializers.ValidationError("This field may not be blank.")
        return value

    def update(self, instance, validated_data):
        """
        Override this function to include extra functionality.
        """
        # For debugging purposes only.
        # print(validated_data)

        # Get our inputs.
        email = validated_data.get('email', instance.email)
        personal_email = validated_data.get('personal_email', None)

        #-------------------------------------
        # Bugfix: Created `SharedUser` object.
        #-------------------------------------
        if instance.owner is None:
            owner = SharedUser.objects.filter(email=email).first()
            if owner:
                instance.owner = owner
                instance.save()
                logger.info("BUGFIX: Attached existing shared user to staff.")
            else:
                instance.owner = SharedUser.objects.create(
                    first_name=validated_data['given_name'],
                    last_name=validated_data['last_name'],
                    email=email,
                    is_active=validated_data['is_active'],
                    franchise=self.context['franchise'],
                    was_email_activated=True
                )
                instance.save()
                logger.info("BUGFIX: Created shared user and attached to staff.")

        #---------------------------
        # Update `SharedUser` object.
        #---------------------------
        # Update the password if required.
        password = validated_data.get('password', None)
        if password:
            instance.owner.set_password(password)
            logger.info("Updated the password.")

        # Update the account.
        if email:
            instance.owner.email = email
            instance.owner.username = get_unique_username_from_email(email)
        instance.owner.first_name = validated_data.get('given_name', instance.owner.first_name)
        instance.owner.last_name = validated_data.get('last_name', instance.owner.last_name)
        instance.owner.is_active = validated_data.get('is_active', instance.owner.is_active)
        instance.owner.save()
        logger.info("Updated the shared user.")

        # Attach the user to the `group` group.
        account_type = validated_data.get('account_type', None)
        if account_type != "NaN":
            account_type = int(account_type)
            instance.owner.groups.set([account_type])
            logger.info("Updated the group membership.")

        #---------------------------
        # Update `Staff` object.
        #---------------------------
        # Person
        instance.description=validated_data.get('description', None)
        instance.given_name=validated_data.get('given_name', None)
        instance.last_name=validated_data.get('last_name', None)
        instance.middle_name=validated_data.get('middle_name', None)
        instance.birthdate=validated_data.get('birthdate', None)
        instance.join_date=validated_data.get('join_date', None)
        instance.gender=validated_data.get('gender', None)

        # Misc
        instance.hourly_salary_desired=validated_data.get('hourly_salary_desired', 0.00)
        instance.limit_special=validated_data.get('limit_special', None)
        instance.dues_date=validated_data.get('dues_date', None)
        instance.commercial_insurance_expiry_date=validated_data.get('commercial_insurance_expiry_date', None)
        instance.police_check=validated_data.get('police_check', None)
        instance.drivers_license_class=validated_data.get('drivers_license_class', None)
        instance.how_hear=validated_data.get('how_hear', None)
        instance.last_modified_by = self.context['last_modified_by']
        instance.last_modified_from = self.context['last_modified_from']
        instance.last_modified_from_is_public = self.context['last_modified_from_is_public']
        # 'organizations', #TODO: IMPLEMENT.

        # Contact Point
        instance.area_served=validated_data.get('area_served', None)
        instance.available_language=validated_data.get('available_language', None)
        instance.contact_type=validated_data.get('contact_type', None)
        instance.email=email
        instance.personal_email=personal_email
        instance.fax_number=validated_data.get('fax_number', None)
        # 'hours_available', #TODO: IMPLEMENT.
        instance.telephone=validated_data.get('telephone', None)
        instance.telephone_extension=validated_data.get('telephone_extension', None)
        instance.telephone_type_of=validated_data.get('telephone_type_of', None)
        instance.other_telephone=validated_data.get('other_telephone', None)
        instance.other_telephone_extension=validated_data.get('other_telephone_extension', None)
        instance.other_telephone_type_of=validated_data.get('other_telephone_type_of', None)

        # Postal Address
        instance.address_country=validated_data.get('address_country', None)
        instance.address_locality=validated_data.get('address_locality', None)
        instance.address_region=validated_data.get('address_region', None)
        instance.post_office_box_number=validated_data.get('post_office_box_number', None)
        instance.postal_code=validated_data.get('postal_code', None)
        instance.street_address=validated_data.get('street_address', None)
        instance.street_address_extra=validated_data.get('street_address_extra', None)

        # Geo-coordinate
        instance.elevation=validated_data.get('elevation', None)
        instance.latitude=validated_data.get('latitude', None)
        instance.longitude=validated_data.get('longitude', None)
        # 'location' #TODO: IMPLEMENT.

        # Save our instance.
        instance.save()
        logger.info("Updated the staff member.")

        #------------------------
        # Set our `Tag` objects.
        #------------------------
        tags = validated_data.get('tags', None)
        if tags is not None:
            if len(tags) > 0:
                instance.tags.set(tags)

        #---------------------------
        # Attach our comment.
        #---------------------------
        extra_comment = validated_data.get('extra_comment', None)
        if extra_comment is not None:
            comment = Comment.objects.create(
                created_by=self.context['last_modified_by'],
                last_modified_by=self.context['last_modified_by'],
                text=extra_comment,
                created_from = self.context['last_modified_from'],
                created_from_is_public = self.context['last_modified_from_is_public']
            )
            staff_comment = StaffComment.objects.create(
                staff=instance,
                comment=comment,
            )

        #---------------------------
        # Update validation data.
        #---------------------------
        # validated_data['comments'] = StaffComment.objects.filter(staff=instance)
        validated_data['last_modified_by'] = self.context['last_modified_by']
        # validated_data['extra_comment'] = None

        # Return our validated data.
        return validated_data
