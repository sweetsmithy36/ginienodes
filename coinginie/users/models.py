from __future__ import absolute_import, unicode_literals

import datetime
import os
import random
from datetime import date, timedelta
from decimal import Decimal

# from cities_light.models import Country
from dateutil import relativedelta
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.humanize.templatetags import humanize
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import IntegrityError, OperationalError, transaction
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateField,
    DecimalField,
    EmailField,
    FileField,
    ForeignKey,
    GenericIPAddressField,
    ManyToManyField,
    OneToOneField,
    PositiveSmallIntegerField,
)
from django.db.models.fields.files import ImageField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import get_template, render_to_string
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField
from tinymce.models import HTMLField

from coinginie.contracts.models import Subscription

today = datetime.date.today()

MALE = "Male"
FEMALE = "Female"
OTHERS = "Others"
GENDER = (
    (MALE, "Male"),
    (FEMALE, "Female"),
    (OTHERS, "Others"),
)
MARRIED = "Married"
SINGLE = "Single"
DIVORCED = "Divorced"
SEPERATED = "Seperated"
MARITAL = (
    (MARRIED, "Married"),
    (SINGLE, "Single"),
    (DIVORCED, "Divorced"),
    (SEPERATED, "Seperated"),
)
FATHER = "Father"
MOTHER = "Mother"
UNCLE = "Uncle"
AUNTY = "Aunty"
BROTHER = "Brother"
SISTER = "Sister"
OTHER = "Other"
RELATIONSHIP = (
    (FATHER, "Father"),
    (MOTHER, "Mother"),
    (UNCLE, "Uncle"),
    (AUNTY, "Aunty"),
    (BROTHER, "Brother"),
    (SISTER, "Sister"),
    (OTHER, "Other"),
)

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def user_dp(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "dp/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )

def user_doc(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "dp/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )
   


SSN_REGEX = "^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4}\\d{4}$)"
NUM_REGEX = "^[0-9]*$"

class User(AbstractUser):
    """Default user for coinginie."""
    USER_TYPE_CHOICES = (
        (1, 'Investors'),
        (2, 'Brokers'),
    )
    #: First and last name do not cover name patterns around the globe
    middle_name = CharField(_("Middle Name"), max_length=255, blank=False, null=True)
    user_type = PositiveSmallIntegerField(_("User Account Type"), choices=USER_TYPE_CHOICES, default=3)

    investor_id = CharField(max_length=255, blank=True, null=True)

    consent = BooleanField(default=False, help_text=mark_safe("</br>By signing up you consent to our <a href='/privacy/'>privacy agreement</a> and <a href='/terms/'>terms of use</a>."))
    
    # Make firstname, middlename and lastname required for superuser signup
    REQUIRED_FIELDS = ["email", "first_name", "middle_name", "last_name"]

    is_verified = BooleanField(default=False)
    
    # registration complete
    """
    These just shows a progress bar for a student/teacher/guardian completing their respective profiles
    """
    profile_updated = BooleanField(default=False)
    settings_updated = BooleanField(default=False)
    payment_updated = BooleanField(default=False)

    def name(self):
        """Get firstname and lastname to attach as one.

        Returns:
            str: user full names.

        """
        if (self.first_name, self.middle_name, self.last_name):
            name = f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            name = self.username
        return name
    
    def __str__(self):
        return str(self.username)

    # user initials
    def initials(self):
        fname = self.first_name[0].upper()
        lname = self.last_name[0].upper()
        if fname is not None and lname is not None:
            return f"{fname} {lname}"
        return None

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    class Meta:
        managed = True
        verbose_name = "User Account"
        verbose_name_plural = "User Accounts"
        ordering = ["first_name", "middle_name", "last_name"]





class Investor(TimeStampedModel):
    user = OneToOneField("User", on_delete=CASCADE, related_name="investor")
    gender = CharField(max_length=50, choices=GENDER, blank=True)

    image = ImageField(upload_to=user_dp, blank=True)
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(240, 190)],
                                     format='JPEG',
                                     options={'quality': 70})

    doc = FileField(upload_to=user_doc, blank=True)

    address = CharField(max_length=500, blank=True)
    phone = PhoneNumberField(unique=False, blank=True, help_text=_("eg: +18012345678"))
    dob = DateField(_("Date of Birth"), blank=True, null=True)

    country = CountryField(blank_label="(Select Country)", null=True)

    can_withdraw = BooleanField(default=False)

    @property
    def age(self):
        TODAY = datetime.today()
        if self.dob:
            return "%s" % relativedelta.relativedelta(TODAY, self.dob).years
        else:
            return None

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} Investor Profile"

    class Meta:
        managed = True
        verbose_name = "Investor Profile"
        verbose_name_plural = "Investor Profiles"
        ordering = ["-created"]


class Broker(TimeStampedModel):
    user = OneToOneField("User", on_delete=CASCADE, related_name="broker")
    broker_id = CharField(max_length=255, blank=True)
    gender = CharField(max_length=50, choices=GENDER, blank=True)

    image = ImageField(upload_to=user_dp, blank=True)
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(240, 190)],
                                     format=['JPEG', 'PNG', 'JPG'],
                                     options={'quality': 70})

    address = CharField(max_length=500, blank=True)
    phone = PhoneNumberField(unique=True, blank=True, help_text=_("eg: 08012345678"))
    dob = DateField(_("Date of Birth"), blank=True, null=True)

    country = CountryField(blank_label="(Select Country)", null=True)

    @property
    def age(self):
        TODAY = datetime.today()
        if self.dob:
            return "%s" % relativedelta.relativedelta(TODAY, self.dob).years
        else:
            return None

    def __str__(self):
        return self.user.name + "Broker Profile"

    class Meta:
        managed = True
        verbose_name = "Broker Profile"
        verbose_name_plural = "Broker Profiles"
        ordering = ["-created"]




class AccountSettings(TimeStampedModel):
    BANKS = (
        ("", "Select Bank"),
        ("Arvest Bank", "Arvest Bank"),
        ("Ally Financial", "Ally Financial"),
        ("American Express", "American Express"),
        ("Amarillos National Bank", "Amarillos National Bank"),
        ("Apple bank for Savings", "Apple bank for Savings"),
        ("Bank of Hawaii", "Bank of Hawaii"),
        ("Bank of Hope", "Bank of Hope"),
        ("Bank United", "Bank United"),
        ("BOA", "Bank of America"),
        ("Bank United", "Bank United"),
        ("Brown Brothers Harriman & Co", "Brown Brothers Harriman & Co"),
        ("Barclays", "Barclays"),
        ("BMO Harris Bank", "BMO Harris Bank"),
        ("Bank OZK", "Bank OZK"),
        ("BBVA Compass", "BBVA Compass"),
        ("BNP Paribas", "BNP Paribas"),
        ("BOK Financial Corporation", "BOK Financial Corporation"),
        ("Cathay Bank", "Cathay Bank"),
        ("Chartway Federal Credit Union", "Chartway Federal Credit Union"),
        ("Capital One", "Capital One"),
        ("Capital City Bank", "Capital City Bank"),
        ("Chase Bank", "Chase Bank"),
        ("Charles Schwab Corporation", "Charles Schwab Corporation"),
        ("CG", "CitiGroup"),
        ("Credit Suisse", "Credit Suisse"),
        ("Comerica", "Comerica"),
        ("CIT Group", "CIT Group"),
        ("CapitalCity Bank", "CapitalCity Bank"),
        ("Credit Union Page", "Credit Union Page"),
        ("Citizens Federal Bank", "Citizens Federal Bank"),
        ("Chemical Financial Corporation", "Chemical Financial Corporation"),
        ("Discover Financial", "Discover Finacial"),
        ("Deutsche Bank", "Deutsche Bank"),
        ("Douglas County Bank & Trust", "Douglas County Bank & Trust "),
        ("Dime Savings Bank of Williamsburgh", "Dime Savings Bank of Williamsburgh"),
        ("East West Bank", "East West Bank"),
        ("Flagster Bank", "Flagster Bank"),
        ("First National of Nebraska", "First National of Nebraska"),
        ("FirstBank Holding Co", "FirstBank Holding Co"),
        ("First Capital Bank", "First Capital Bank"),
        ("First Commercial Bank", "First Commercial Bank"),
        (
            "First Federal Savings Bank of Indiana",
            "First Federal Savings Bank of Indiana",
        ),
        ("First Guaranty Bank of Florida", "First Guaranty Bank of Florida"),
        ("First Line Direct", "First Line Direct"),
        ("First USA Bank", "First USA Bank"),
        ("Fifth Third Bank", "Fifth Third Bank"),
        ("First Citizens BancShares", "First Citizens BancShares"),
        ("Fulton Financial Corporation", "Fulton Financial Corporation"),
        ("First Hawaiian Bank", "First Hawaiian Bank"),
        ("First Horizon National Corporation", "First Horizon National Corporation"),
        ("Frost Bank", "Frost Bank"),
        ("First Midwest Bank", "First Midwest Bank"),
        ("Goldman Sachs", "Goldman Sachs"),
        ("Grandeur Financials", "Grandeur Financials"),
        ("HSBC Bank USA", "HSBC Bank USA"),
        ("Home BancShares Conway", "Home BancShares Conway"),
        ("Huntington Bancshares", "Huntington Bancshares"),
        ("Investors Bank", "Investors Bank"),
        ("Íntercity State Bank", "Íntercity State Bank"),
        ("KeyCorp", "KeyCorp"),
        ("MB Financial", "MB Financial"),
        ("Mizuho Financial Group", "Mizuho Financial Group"),
        ("Midfirst Bank", "Midfirst Bank"),
        ("M&T Bank", "M&T Bank"),
        ("MUFG Union Bank ", "MUFG Union Bank"),
        ("Morgan Stanley", "Morgan Stanley"),
        ("Northern Trust", "Northern Trust"),
        ("New  York Community Bank", "New York Community Bank"),
        ("Old National Bank", "Old National Bank"),
        ("Pacwest Bancorp", "Pacwest Bancorp"),
        ("Pinnacle Financial Partners", "Pinnacle Financial Partners"),
        ("PNC Financial Services", "PNC Financial Services"),
        ("Raymond James Financial", "Raymond James Financial"),
        ("RBC Bank", "RBC Bank"),
        ("Region Financial Corporation", "Region Financial Corporation"),
        ("Satander Bank", "Satander Bank"),
        ("Synovus Columbus", "Synovus Columbus"),
        ("Synchrony Financial", "Synchrony Financial"),
        ("Sterling Bancorp", "Sterling Bancorp"),
        ("Simmons Bank", "Simmons Bank"),
        ("South State Bank", "South State Bank"),
        ("Stifel St. Louise", "Stifel St. Louise"),
        ("Suntrust Bank", "Suntrust Bank"),
        ("TCF Financial Corporation", "TCF Financial Corporation"),
        ("TD Bank", "TD Bank"),
        ("The Bank of New York Mellon", "The Bank of New York Mellon"),
        ("Texas Capital Bank", "Texas Capital Bank"),
        ("UMB Financial Corporation", "UMB Financial Corporation"),
        ("Utrecht-America", "Utrecht-America"),
        ("United Bank", "United Bank"),
        ("USAA", "USAA"),
        ("U.S Bank", "U.S Bank"),
        ("UBS", "UBS"),
        ("Valley National Bank", "Valley National Bank"),
        ("Washington Federal", "Washington Federal"),
        ("Western Alliance Banorporation", "Western Alliance Bancorporation"),
        ("Wintrust Financial", "Wintrust Finacial"),
        ("Webster Bank", "Webster Bank"),
        ("Wells Fargo", "Wells Fargo"),
        ("Zions Bancorporation", "Zions Bancorporation"),
        ("Other Bank", "Other Bank"),
    )
    """Provision to create a paystack account for students to receive money from handling student job roles in school"""

    user = OneToOneField("User", on_delete=CASCADE, related_name="account")
    account_name = CharField(max_length=500, blank=True)
    account_number = CharField(max_length=11, unique=False, blank=True, validators=[
            RegexValidator(
                regex=NUM_REGEX,
                message="Must Contain Numbers Only",
                code="Invalid_input, Only Integers",
            )
        ])
    swift_code = CharField(max_length=11, unique=False, blank=True, validators=[
            RegexValidator(
                regex=NUM_REGEX,
                message="Must Contain Numbers Only",
                code="Invalid_input, Only Integers",
            )
        ])
    bank_name = CharField(max_length=120, blank=True, choices=BANKS, default="")
    routing_no = CharField(
        _("Recipient Routing Number"),
        max_length=13,
        null=True,
        blank=True,
        unique=False,
        help_text="must be the recipients 9 digits routing number",
        validators=[
            RegexValidator(
                regex=NUM_REGEX,
                message="Must Contain Numbers Only",
                code="Invalid_input, Only Integers",
            )
        ],
    )
    
    
    bank_name_text = CharField(max_length=120, blank=True)
    
    
    def __str_(self):
        return f"{self.user.first_name} {self.user.last_name} Bank Account Detail"
    
    class Meta:
        managed = True
        verbose_name = "Bank Account"
        verbose_name_plural = "Bank Accounts"
        ordering = ["-created"]
    

class PrivacyPolicies(TimeStampedModel):
    user = OneToOneField(User, on_delete=CASCADE, related_name="userprivacypolicy")
    cookies_and_tracking = BooleanField(default=True, help_text="This is a must have integration to enable us provide you with proper services and security. They do not create any security bridge for you and can only be used to login, signout and even ensure your sessions are still working. You hereby consent to the use and transfer of your Personal Information to countries outside the European Union.")
    google_ads = BooleanField(default=True, help_text="These is an advertising and devlivey network service, aimed solely to provide advert placements based on your browser informations. permiting this allows us provide you with adverts directly on our site. Be ensured that this does not constitute any security risk to you. You hereby consent to the use and transfer of your Personal Information to countries outside the European Union.")
    social_account_integration = BooleanField(default=True, help_text="Facebook, Instagram, Twitter, Google Plus, Linkedin, these providers are integrated into the website to ensure we have proper informations to provide for our social influence and lead generation. We do not share these information for any other purpose other than statistical analysis. You hereby consent to the use and transfer of your Personal Information to countries outside the European Union.")
    personal_information = BooleanField(default=True, help_text="These are personal informations we collect to provide quality and personalised services to you. They include (First Name, Last Name, Phone Number, Social Accounts, Addresses, Photo). You hereby consent to the use and transfer of your Personal Information to countries outside the European Union.")
    commercial_information = BooleanField(default=True, help_text="These are informations we collect for commercial purposes and are used for analysis as well as providing accurate data statistics of our services usage. You hereby consent to the use and transfer of your Personal Information to countries outside the European Union.")
    identifiers = BooleanField(default=True, help_text="These are informations we collect to prevent fraud, do analysis as well as utilize cloud services. They include Email address, device identifiers (User IDs, IP and Location). You hereby consent to the use and transfer of your Personal Information to countries outside the European Union.")
    internet_or_other_electronic_network_activity_information = BooleanField(default=True, help_text="These are informations we collect regarding the user interactions within the website. With this information we can provide cloud services such as Content Delivery Networks for static/asset and media files. You hereby consent to the use and transfer of your Personal Information to countries outside the European Union.")
    age_restriction = BooleanField(default=True, help_text="As a bid to ensure we do not share informations to individuals who are below legal age, we expect a concent to be taken, idemnifying us from any law suit involved with sharing certain or aiding a minor purchase goods and services without a concent from a legal guardian. You hereby consent to the use and transfer of your Personal Information to countries outside the European Union.")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} privacy policy"

    class Meta:
        managed = True
        verbose_name = "Privacy"
        verbose_name_plural = "Privacies"
        ordering = [ "-created"]






from coinginie.utils.rand_string import unique_number_generator
from coinginie.wallet.models import Wallet

today = datetime.date.today()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        Investor.objects.create(user=instance)
        Subscription.objects.create(user=instance)
        AccountSettings.objects.create(user=instance)
        PrivacyPolicies.objects.create(user=instance)
        Wallet.objects.create(user=instance, bitcoin_balance=0.00, litecoin_balance=0.00, ethereum_balance=0.00 )
        
        if instance.investor_id is None:
            instance.investor_id = unique_number_generator(instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        instance.investor.save()
        instance.subscription.save()
        instance.account.save()
        instance.wallet.save()
        instance.userprivacypolicy.save()

