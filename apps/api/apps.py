from django.apps import AppConfig


class LmsConfig(AppConfig):
    name = 'lms'
    verbose_name = 'LMS Integration'


class AppealsConfig(AppConfig):
    name = 'appeals'
    verbose_name = 'Grade Appeals'


class CredentialsConfig(AppConfig):
    name = 'credentials'
    verbose_name = 'Digital Credentials'


class CareersConfig(AppConfig):
    name = 'careers'
    verbose_name = 'Career Services'


class AlumniConfig(AppConfig):
    name = 'alumni'
    verbose_name = 'Alumni Network'


class WhatsappConfig(AppConfig):
    name = 'whatsapp'
    verbose_name = 'WhatsApp Integration'


class UssdConfig(AppConfig):
    name = 'ussd'
    verbose_name = 'USSD Channel'


class LibraryConfig(AppConfig):
    name = 'library'
    verbose_name = 'Library'


class ExamConfig(AppConfig):
    name = 'exam'
    verbose_name = 'Exam Management'


class SiwesConfig(AppConfig):
    name = 'siwes'
    verbose_name = 'SIWES'