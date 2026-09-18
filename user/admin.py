from django.contrib import admin
from .models import User, EmailVerificationToken, PasswordResetToken

admin.site.register(User)
admin.site.register(EmailVerificationToken)
admin.site.register(PasswordResetToken)

