from django.db import models
from accounts.models import Author


class Post(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def get_status(self):
        statuses = StatusType.objects.filter(post=self).values('rating')
        result = {}
        num = 0
        ser = 0
        for i in statuses:
            num = num + i['rating']
            ser = ser + 1
        if num != 0:
            result['оценка'] = num / ser
            return result
        result['оценка'] = num
        return result


class Comment(models.Model):
    comment_text = models.TextField()
    comment_created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.post


class StatusType(models.Model):
    RATING_CHOICE = (
        (0, 'nothing'),
        (1, 'Ok'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible'),
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICE, null=True, default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author} - {self.post} - {self.rating} '


class StatusPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    point = models.IntegerField()
