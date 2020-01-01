from django.db import models


class Categories(models.Model):
	Title = models.CharField(max_length=40, null=False)


class TagModel(models.Model):
	Title = models.CharField(max_length=20, null=False)


class Entries(models.Model):
	id = 0
	Title = models.CharField(max_length=80, null=False)
	Content = models.TextField(null=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	Category = models.ForeignKey(Categories, on_delete=models.CASCADE)

	Tags = models.ManyToManyField(TagModel)
	Comments = models.PositiveSmallIntegerField(default=0, null=True)


class Comments(models.Model):
	id = 0
	Name = models.CharField(max_length=20, null=True)
	Password = models.CharField(max_length=32, null=False)
	Content = models.CharField(max_length=200, null=False)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	Entry = models.ForeignKey(Entries, on_delete=models.CASCADE)

