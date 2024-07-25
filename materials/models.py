from django.db import models

from config import settings
from users.models import User

NULLABLE = {"blank": True, "null": True}


# Курс: Viewsets
# название,
# превью (картинка),
# описание.
# Урок: Generic-классы.
# название,
# описание,
# превью (картинка),
# ссылка на видео.


class Course(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    preview = models.ImageField(
        upload_to="courses/photo",
        verbose_name="Превью курса",
        help_text="Загрузите картинку для превью курса",
        **NULLABLE
    )
    description = models.TextField(
        verbose_name="Описание курса", help_text="Укажите описание курса", **NULLABLE
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Владелец урока",
        related_name="course_owner",
        **NULLABLE,
        help_text="Выберите владельца курса"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Название урока",
        help_text="Укажите название урока",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        related_name="lessons",
        **NULLABLE
    )
    description = models.TextField(
        verbose_name="Описание урока", help_text="Укажите описание урока", **NULLABLE
    )
    preview = models.ImageField(
        upload_to="lessons/photo",
        verbose_name="Превью урока",
        help_text="Загрузите картинку для превью урока",
        **NULLABLE
    )
    video_link = models.URLField(
        verbose_name="Ссылка на видео",
        help_text="Укажите ссылку на видео урока",
        **NULLABLE
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Владелец урока",
        related_name="lessons_owner",
        **NULLABLE,
        help_text="Выберите владельца урока"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    """ Модель подписки пользователя """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="subscriptions",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="subscribers",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата подписки",
    )

    def get_user_email(self):
        return self.user.email

    def __str__(self):
        return f"Подписка {self.user.email} на курс {self.course.name}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ('user', 'course')


class Payment(models.Model):
    class Type_payment(models.TextChoices):
        cash = 'Наличные'
        transfer = 'Переводом'

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='пользователь', related_name='payment',
                              **NULLABLE)
    datetime_payment = models.DateTimeField(verbose_name='дата оплаты', auto_now_add=True)
    price = models.PositiveIntegerField(verbose_name='сумма оплаты', **NULLABLE)
    paid_course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, related_name='payment')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, **NULLABLE, related_name='payment')
    payment_type = models.CharField(choices=Type_payment.choices, max_length=16, verbose_name='способ оплаты')
    session_id = models.CharField(max_length=300, verbose_name=' id сессии', **NULLABLE)
    link = models.URLField(max_length=400, verbose_name='Ссылка на оплату', **NULLABLE)

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'

