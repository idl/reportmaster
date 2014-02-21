from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from taggit.managers import TaggableManager

class IDLUser(User):
	class Meta:
		proxy = True

	def name(self):
		if self.first_name != "" and self.last_name != "":
			return " ".join([self.first_name, self.last_name])
		else:
			return self.username

# Create your models here.
class ReportItem(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(IDLUser)
	content = models.TextField()
	tags = TaggableManager(blank=True)
	last_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.created_by.name() + ": " + self.content


class Report(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(IDLUser)
	report_items = models.ManyToManyField(ReportItem)
	description = models.TextField('Description')
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name