from django.db import models
import uuid
from users.models import Profile


class Project(models.Model):
    """ Класс проектов """
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    demo_link = models.CharField(max_length=1000, null=True, blank=True)
    source_link = models.CharField(max_length=1000, null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True,
                                       default='default.jpg')
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True,
                          editable=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']

    @property
    def get_vote(self):
        # Отбор положительных голосов
        reviews = self.review_set.all()
        up_vote = reviews.filter(value='up').count()
        total_votes = reviews.count()

        # Подсчет процента положительных голосов
        ratio_votes = (up_vote / total_votes) * 100
        self.vote_total = total_votes
        self.vote_ratio = ratio_votes
        self.save()

    @property
    def review_owner(self):
        # Функция отвечает за то чтобы 1 юзер мог оставить не больше 1 комментария к проекту
        queryset = self.review_set.all().values_list('owner__id', flat=True)  # получение owner.id
        return queryset


class Review(models.Model):
    """ Класс комментариев и голосов """
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('Down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=250, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True,
                          editable=False)

    def __str__(self):
        return self.value


class Tag(models.Model):
    """ Класс скиллов """
    name = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True,
                          editable=False)

    def __str__(self):
        return self.name
