import zanbil.enum as enum
import re

class ObjectValidator():

    def __init__(self, validationData={}, *args, **kwargs):
        self.data = validationData
        self.statusCode = 200
        self.validationPipeline = []
        self.errors = {}
        self.invalidFields = []

    def flush(self):
        self = ObjectValidator()
        return self

    def setError(self, field, error):
        if field not in self.invalidFields:
            fieldErrors = self.errors.get(field, [])
            if error[0] not in fieldErrors:
                self.errors[field] = fieldErrors + [error[0]]
                self.statusCode = error[1]
                self.invalidFields.append(field)
    def getErrors(self):
        return self.errors

    def validate(self):
        for validation in self.validationPipeline:
            try:
                validation['validator'](validation['data'])
            except:
                self.setError(validation['data']['field'],enum.Error.INVALID_FIELD_DATA.value)

    def addValidation(self, data, validatorFunction):
        self.validationPipeline.append({
            'data': data,
            'validator': validatorFunction
        })

    def _check_with_authenticationValidator(self, data):
        if not data['user'].is_authenticated:
            self.setError(data['field'], enum.Error.UNAUTHORIZED.value)

    def _check_with_nonDuplicateObjectValidator(self, data):
        model = data['model']
        if model.objects.filter(**data['filter']):
            self.setError(data['field'], enum.Error.DUPLICATE_FIELDS.value)

    def _check_with_ObjectExistenceValidator(self, data):
        model = data['model']
        if not model.objects.filter(**data['filter']):
            self.setError(data['field'], enum.Error.GENERIC_OBJECT_NOT_FOUND.value)

    def checkNonDuplicateObject(self, field, model, **filter):
        self.addValidation({'field': field, 'model': model, 'filter': filter},
                           self._check_with_nonDuplicateObjectValidator)
        return self

    def checkObjectExistence(self, field, model, **filter):
        self.addValidation({'field': field, 'model': model, 'filter': filter},
                           self._check_with_ObjectExistenceValidator)
        return self

    def checkUserAuthentication(self, field, user):
        self.addValidation({'field': field, 'user': user},
                           self._check_with_authenticationValidator)
        return self


#\b(?!(\d)\1{3})[13-9]{4}[1346-9][013-9]{5}\b
# postal code validation


class FieldValidator():

    def __init__(self, validationData={}, *args, **kwargs):
        self.data = validationData
        self.validationPipeline = []
        self.statusCode = 200
        self.errors = {}
        self.invalidFields = []

    def flush(self):
        self = FieldValidator()

    def setError(self, field, error):
        if field not in self.invalidFields:
            fieldErrors = self.errors.get(field, [])
            if error[0] not in fieldErrors:
                self.errors[field] = fieldErrors + [error[0]]
                self.statusCode = error[1]
                self.invalidFields.append(field)

    def getErrors(self):
        return self.errors

    def validate(self):
        for validation in self.validationPipeline:
            try:
                validation['validator'](validation['data'])
            except:
                self.setError(validation['data']['field'],enum.Error.INVALID_FIELD_DATA.value)
        return self
    def addValidation(self, data, validatorFunction):
        if (data['value'] == 'unAssigned') and data['field'] in self.data.keys():
            data['value'] = self.data[data['field']]
        elif data['value'] == 'unAssigned' and data['field'] not in self.data.keys():
            data['value'] = None
        self.validationPipeline.append({
            'data': data,
            'validator': validatorFunction
        })

    def _check_with_typeValidator(self, data):
        if not isinstance(data['value'], data['type']):
            self.setError(data['field'], enum.Error.INVALID_FIELD_DATA.value)

    def _check_with_nationalLegalCodeValidator(self, data):
        nationalLegalCode = data['value']
        result = 0
        validationList = [29, 27, 23, 19, 17, 29, 27, 23, 19, 17]
        if len(nationalLegalCode) != 11:
            self.setError(data['field'], enum.Error.INVALID_NATIONAL_LEGAL_CODE.value)
            return
        for i in range(10):
            result += (int(nationalLegalCode[-2]) + 2 + int(nationalLegalCode[i])) * validationList[i]
        if result % 11 == 10:
            reminder = 0
        else:
            reminder = result % 11
        if reminder == int(nationalLegalCode[-1]):
            valid = True
        else:
            valid = False
        if valid is False:
            self.setError(data['field'], enum.Error.INVALID_NATIONAL_LEGAL_CODE.value)

    def _check_with_nationalCodeValidator(self, data):
        nCode = data['value']
        valid = True
        if len(nCode) != 10:
            valid = False
            self.setError(data['field'], enum.Error.INVALID_FIELD_DATA.value)
            return
        sum = 0
        for i in range(9):
            sum += int(nCode[i]) * (10 - i)
        r = sum % 11
        if (r < 2 and r == int(nCode[9])) or r >= 2 and r == 11 - int(nCode[9]):
            valid = valid and True
        if valid is False:
            self.setError(data['field'], enum.Error.INVALID_FIELD_DATA.value)
    def _check_with_officer1NationalCodeValidator(self, data):
        nCode = data['value']
        valid = True
        if len(nCode) != 10:
            self.setError(data['field'], enum.Error.INVALID_FIELD_DATA.value)
            return
        sum = 0
        for i in range(9):
            sum += int(nCode[i]) * (10 - i)
        r = sum % 11
        if (r < 2 and r == int(nCode[9])) or r >= 2 and r == 11 - int(nCode[9]):
            valid = valid and True
        if valid is False:
            self.setError(data['field'], enum.Error.INVALID_FIELD_DATA.value)
    def _check_with_officer2NationalCodeValidator(self, data):
        nCode = data['value']
        valid = True
        if len(nCode) != 10:
            valid = False
            self.setError(data['field'], enum.Error.INVALID_FIELD_DATA.value)
            return
        sum = 0
        for i in range(9):
            sum += int(nCode[i]) * (10 - i)
        r = sum % 11
        if (r < 2 and r == int(nCode[9])) or r >= 2 and r == 11 - int(nCode[9]):
            valid = valid and True
        if valid is False:
            self.setError(data['field'], enum.Error.INVALID_FIELD_DATA.value)

    def _check_with_featuresValidator(self, data):
        for i in data['value']:
            if i not in ["پلتفرم پرداخت در محل", "باشگاه مشتریان", "درگاه پرداخت اینترنتی"]:
                self.setError(data['field'], enum.Error.INVALID_FIELD_DATA.value)
                break

    def _check_with_userNameValidator(self, data):
        username = re.match(r"^[A-Za-z]+(?:[ _-][A-Za-z0-9]+)*$", data["value"])
        if 'admin' in data['value'] or 'zibal' in data['value'] or username is None:
            self.setError(data['field'], enum.Error.INVALID_USERNAME.value)

    def _check_with_phoneNumberValidator(self, data):
        if data['value'] is None or len(data) < 1:
            self.setError(data['field'], enum.Error.PHONE_INCORRECT_TEMPLATE.value)

    def _check_with_mobileValidator(self, data):
        mobileNumber = data['value']
        if mobileNumber is None:
            self.setError(data['field'], enum.Error.EMPTY_INPUT_FIELD.value)
            return
        match_object = re.match(r"(^09[0-9]{9}$)", mobileNumber)
        if match_object is None or mobileNumber is None:
            self.setError(data['field'], enum.Error.INVALID_FIELD_DATA.value)

    def _check_with_emailValidator(self, data):
        email = data['value']
        if email is None:
            self.setError(data['field'], enum.Error.EMPTY_INPUT_FIELD.value)
            return
        match_object = re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email)
        if match_object is None or email is None:
            self.setError(data['field'], enum.Error.INVALID_FIELD_DATA.value)

    def _check_with_noneValidator(self, data):
        if data['value'] is None or data['value'] == "":
            self.setError(data['field'], enum.Error.EMPTY_INPUT_FIELD.value)

    def _check_with_fileValidator(self, data):

        file = data['value']
        field = data['field']
        if file is None:
            self.setError(field, enum.Error.EMPTY_INPUT_FIELD.value)
            return
        elif file.size > enum.Limits.FILE_SIZE_LIMIT.value:
            self.setError(field, enum.Error.FILE_SIZE_EXCEED.value)
        types = data['options'].get('types', None)
        valid = False
        if types is not None:
            for type in types:
                valid = valid or type in file.content_type
        if valid is False:
            self.setError(field, enum.Error.REQUEST_TYPE_ERROR.value)

    def _check_with_IBANValidator(self, data):
        iban = data['value']
        if len(iban)!=26 or not iban.startswith("IR"):
            self.setError(data['field'], enum.Error.IBAN_ERROR.value)
            return
        code = iban[4:]+iban[:4]
        code = code.replace('I','18').replace('R','27')
        if int(code)%97!=1:
            self.setError(data['field'], enum.Error.IBAN_ERROR.value)

    def _check_with_subMerchantBankAccountValidator(self, data):
        if not SubMerchant.objects.filter(idsql=data['value']['userId'], ID=data['value']['subId'], status=1).exists():
            self.setError(data['field'], enum.Error.IMPOSSIBLE_BANK_ACCOUNT_DESTINATION.value)

    def _check_with_minDataLengthValidator(self, data):
        if data['value'] is None or len(data['value']) < data['length']:
            self.setError(data['field'],( enum.Error.MESSAGE_INSUFFICIENT_LENGTH.value[0].format(data['length']),enum.Error.MESSAGE_INSUFFICIENT_LENGTH.value[1]))

    def _check_with_maxDataLengthValidator(self, data):
            if data['value'] is None or len(data['value']) > data['length']:
                self.setError(data['field'], (enum.Error.MESSAGE_INSUFFICIENT_LENGTH.value[0].format(data['length']),
                                              enum.Error.MESSAGE_INSUFFICIENT_LENGTH.value[1]))

    def _check_with_equalDataLengthValidator(self, data):
            if data['value'] is None or len(data['value']) != data['length']:
                self.setError(data['field'], (enum.Error.MESSAGE_INSUFFICIENT_LENGTH.value[0].format(data['length']),
                                              enum.Error.MESSAGE_INSUFFICIENT_LENGTH.value[1]))

    def _check_with_inputValidator(self, data):
        if data['value'] is None or len(data['value']) < 1:
            self.setError(data['field'], enum.Error.EMPTY_INPUT_FIELD.value)

    def _check_with_IbanTransferable(self, data):
        if data['value'][4:7]=='062' and data['value'][-13:-10]=='080':
            self.setError(data['field'], enum.Error.NOT_IBAN_TRANSFERABLE.value)

    def _check_with_username(self, data):
        username = re.match(r"^[a-zA-Z0-9_.-]+$", data["value"])
        if username is None:
            self.setError(data['field'], enum.Error.INVALID_USERNAME.value)

    #############################################################################

    def checkType(self, field, type, value="unAssigned"):
        self.addValidation({'field': field, 'type': type, 'value': value}, self._check_with_typeValidator)
        return self

    def checkNationalLegalCode(self, field, code="unAssigned"):
        self.addValidation({'field': field, 'value': code}, self._check_with_nationalLegalCodeValidator)
        return self

    def checkOfficer1NationalCode(self, field, code="unAssigned"):
        self.addValidation({'field': field, 'value': code}, self._check_with_officer1NationalCodeValidator)
        return self

    def checkOfficer2NationalCode(self, field, code="unAssigned"):
        self.addValidation({'field': field, 'value': code}, self._check_with_officer2NationalCodeValidator)
        return self

    def checkNationalCode(self, field, code="unAssigned"):
        self.addValidation({'field': field, 'value': code}, self._check_with_nationalCodeValidator)
        return self

    def checkFeatures(self, field, features="unAssigned"):
        self.addValidation({'field': field, 'value': features}, self._check_with_featuresValidator)
        return self

    def checkUserName(self, field, username="unAssigned"):
        self.addValidation({'field': field, 'value': username}, self._check_with_userNameValidator)
        return self

    def checkPhone(self, field, data="unAssigned"):
        self.addValidation({'field': field, 'value': data}, self._check_with_phoneNumberValidator)
        return self

    def checkMobile(self, field, data="unAssigned"):
        self.addValidation({'field': field, 'value': data}, self._check_with_mobileValidator)
        return self

    def checkEmail(self, field, data="unAssigned"):
        self.addValidation({'field': field, 'value': data}, self._check_with_emailValidator)
        return self

    def checkNotNone(self, field, data="unAssigned"):
        self.addValidation({'field': field, 'value': data}, self._check_with_noneValidator)
        return self

    def checkFile(self, field, data, **options):
        self.addValidation({'field': field, 'value': data, 'options': options}, self._check_with_fileValidator)
        return self

    def checkIBAN(self, field, data="unAssigned"):
        self.addValidation({'field': field, 'value': data}, self._check_with_IBANValidator)
        return self

    def checkBankAccountDestinationForSubmerchant(self, field, userId, subId):
        data = {
            'userId': userId,
            'subId': subId
        }
        self.addValidation({'field': field, 'value': data}, self._check_with_subMerchantBankAccountValidator)
        return self

    def checkDataLength(self, field, length,mode='equal', data="unAssigned"):
        if mode == 'equal':
            validatorFunction = self._check_with_equalDataLengthValidator
        if mode == 'min':
            validatorFunction = self._check_with_minDataLengthValidator
        if mode == 'max':
            validatorFunction = self._check_with_minDataLengthValidator

        self.addValidation({'field': field, 'value': data, 'length': length}, validatorFunction)

        return self

    def checkInputData(self, field, data="unAssigned"):
        self.addValidation({'field': field, 'value': data}, self._check_with_inputValidator)
        return self

    def checkTelephone(self, field, data="unAssigned"):  ##TODO
        self.addValidation({'field': field, 'value': data}, self._check_with_phoneNumberValidator)
        return self

    def checkIsIbanTransferable(self, field, data="unAssigned"):
        self.addValidation({'field': field, 'value': data}, self._check_with_IbanTransferable)
        return self

    def checkUsername(self, field, data="unAssigned"):
        self.addValidation({'field': field, 'value': data}, self._check_with_username())


class DataValidator:

    def __init__(self, data={}):
        self.fieldValidator = FieldValidator(data)
        self.objectValidator = ObjectValidator()
        self.errors = {}
        self.statusCode = 200

    def getValidatorsErrors(self):
        self.objectValidator.validate()
        self.fieldValidator.validate()
        for key in self.fieldValidator.getErrors().keys():
            self.errors[key] = self.errors.get(key, []) + self.fieldValidator.getErrors()[key]
        self.statusCode = self.fieldValidator.statusCode
        for key in self.objectValidator.getErrors().keys():
            self.errors[key] = self.errors.get(key, []) + self.objectValidator.getErrors()[key]
        self.statusCode = self.objectValidator.statusCode if self.objectValidator.statusCode != 200 else self.statusCode
        return self.errors

    def generateMessage(self):
        messages = []
        errorKeys = self.errors.keys()
        if 'email' in errorKeys:
            messages.append(' آدرس ایمیل نامعتبر است')

        if "name" in  errorKeys :
            messages.append('نام را وارد کنید')

        if 'username' in errorKeys:
            messages.append('نام کاربری را وارد کنید')

        if 'password' in errorKeys:
            messages.append('رمز عبور را وارد کنید')

        if  'mobile' in errorKeys:
            messages.append('تلفن همراه خود را وارد کنید.')

        if 'phone' in errorKeys:
            messages.append('تلفن ثابت را به فرمت 02122407556 و 11 رقمی وارد کنید')
        if 'iban' in errorKeys or 'IBAN' in errorKeys:
            messages.append('شماره شبای وارد شده معتبر نیست. 26 کاراکتر و شروع با IR و بدون خط تیره (-) و فاصله')
        if 'user' in errorKeys:
            messages.append('لطفا وارد شوید')

        return messages