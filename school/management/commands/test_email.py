from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Test email functionality'

    def handle(self, *args, **options):
        try:
            subject = 'Test Email from School Management System'
            message = '''
            This is a test email to verify that the email functionality is working correctly.
            
            If you receive this email, the email configuration is working properly.
            
            Best regards,
            School Management System
            '''
            
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],  # Send to yourself
                fail_silently=False
            )
            
            self.stdout.write(
                self.style.SUCCESS('Test email sent successfully!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to send test email: {e}')
            ) 