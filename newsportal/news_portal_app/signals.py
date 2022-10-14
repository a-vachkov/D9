from .models import Post, Category
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if instance.category.first():
        print(instance.category.first())

        cat = instance.category.first()
        subscribers = cat.subscribers.all()
        subscribers_emails = cat.subscribers.all().values('email')
        subscribers_names = cat.subscribers.all().values('username')

        print(subscribers_emails)
        print(subscribers_names)

        user_emails = []
        user_names = []

        for subscriber in subscribers:
            user_emails.append(subscriber.email)
            user_names.append(subscriber.username)

            if created:
                subject = f'{subscriber.username}, новая публикация - {instance.title}, \
                в разделе {instance.category.first()} ... {instance.time.strftime("%d %m %Y")}'
            else:
                subject = f'{subscriber.username}, новая публикация - {instance.title}, \
                в разделе {instance.category.first()} ... {instance.time.strftime("%d %m %Y")}'

            msg = EmailMultiAlternatives(
                subject=subject,
                body=f'Привет {subscriber.username}, новая публикация - {instance.title}, \
                в разделе {instance.category.first()}',  # это то же, что и message
                from_email='subscribecategory@yandex.ru',
                to=[f'{subscriber.email}'],  # это то же, что и recipients_list
            )

            # получаем наш html
            html_content = render_to_string(
                'post_created.html',
                {
                    'post': instance,
                    'user': subscriber.username,
                }
            )

            msg.attach_alternative(html_content, "text/html")  # добавляем html

            msg.send()  # отсылаем

            print(subject)



        print(user_emails)
        print(user_names)