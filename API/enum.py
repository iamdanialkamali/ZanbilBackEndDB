from enum import Enum


class Error(Enum):
    ACCESS_DENIED = 'شما اجازه دسترسی به این قسمت را ندارید!', 403  #
    INTERNAL_SERVER_ERROR = 'خطای داخلی سرور، زیبال این خطا را بررسی و برطرف خواهد کرد', 500  #
    CAPTCHA_FAILED = 'لطفا مجددا تلاش کنید', 403  #
    UNAUTHORIZED = 'لطفا ابتدا وارد شوید', 401  #
    COMPLETED_STATUS = 'وضعیت شما تکمیل شده است', 400
    MESSAGE_INSUFFICIENT_LENGTH = 'طول پیام شما باید حداقل {} کاراکتر باشد', 400  #
    EMPTY_INPUT_FIELD = 'این فیلد الزامی است', 400  #
    GENERIC_OBJECT_NOT_FOUND = 'یافت نشد', 404  #
    PHONE_INCORRECT_TEMPLATE = 'تلفن ثابت را به فرمت 02122407556 و 11 رقمی وارد کنید', 400  #
    IMPOSSIBLE_BANK_ACCOUNT_DESTINATION = 'امکان واریز وجه به حساب انتخاب شده نیست. لطفا با پشتیبانی تماس بگیرید', 400  #
    BANK_ACCOUNT_CHANGE_IMPOSSIBLE = 'امکان تغییر حساب نیست. لطفا با پشتیبانی تماس بگیرید', 400
    IBAN_ERROR = 'شماره شبای وارد شده معتبر نیست. 26 کاراکتر و شروع با IR و بدون خط تیره (-) و فاصله', 400  #
    OBJECT_NOT_FOUND = '{} مورد نظر یافت نشد', 404 #
    FILE_SIZE_EXCEED = 'سایز فایل از حد مجاز بیشتر است', 400 #
    INVALID_FIELD_DATA = 'ورودی  نامعتبر است ', 400 #
    OFFICER_1_WRONG_NATIONALCODE =  'کدملی صاحب امضای اول نامعتبر است.',400
    OFFICER_2_WRONG_NATIONALCODE =  'کدملی صاحب امضای دوم نامعتبر است.',400
    SHAPARAK_DATA_COMPLETED = 'مشخصات کاربر تکمیل است', 400
    DUPLICATE_FIELDS = 'ورودی تکراری است', 400 #
    REQUEST_TYPE_ERROR = 'نوع داده ورودی اشتباه است ', 415 #
    INCORRECT_CURRENT_PASSWORD = 'رمز فعلی اشتباه است ', 406
    IN_ACTIVE_ACCOUNT = 'حساب کاربری شما غیر فعال است', 403
    NOT_IBAN_TRANSFERABLE = 'حساب قابلیت واریز ندارد (آینده ساز بانک آینده)',400
    INVALID_NATIONAL_LEGAL_CODE = 'شماره ملی شرکت معتبر نیست',400
    INVALID_USERNAME = "نام کاربری وارد شده معتبر نیست.",400
    REPETITIVE_DEPTARTMENT_ID = 'دپارتمان جدید نمیتواند دپارتمان فعلی باشد',400
    INSUFFICIENT_AMOUNT = 'مبلغ درخواستی از موجودی شما بیشتر می‌باشد',400
    PROBLEM_IN_DECHARGING = 'مشکلی در کم کردن موچودی پیش آمده است',400
    PROBLEM_IN_CHARGING = 'مشکلی اضافه کردن موچودی پیش آمده است',400
    NOT_OWNED_TICKET_MESSAGE = 'پیام متعلق به شما نیست',403

class Limits(Enum):
    FILE_SIZE_LIMIT = 5 * 1024 * 1000
    TURNING_BACK_TRANSACTION_PERCENT = 0.1
    TURNING_BACK_TRANSACTION_CONSTANT = 3
    FORGOT_PASSWORD_MINUTES = 20
