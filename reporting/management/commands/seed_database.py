from django.core.management.base import BaseCommand, CommandError
from reporting.models import ReportItem, Report
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class Command(BaseCommand):
    args = ''
    help = 'Seeds the database'

    def handle(self, *args, **options):
        
        try:
            user_1 = User.objects.create_user('chris.boudreaux', 'chris.boudreaux@ssrc.msstate.edu', 'ssrc2014')
            user_1.save()
        except:
            user_1 = User.objects.get(username="chris.boudreaux")
        
        try:
            user_2 = User.objects.create_user('david.martin', 'david.martin@ssrc.msstate.edu', 'ssrc2014')
            user_2.save()
        except:
            user_2 = User.objects.get(username="david.martin")
        
        try:
            user_3 = User.objects.create_user('jake.gaylor', 'jake.gaylor@ssrc.msstate.edu', 'ssrc2014')
            user_3.save()
        except:
            user_3 = User.objects.get(username="jake.gaylor")

        report_item_1 = ReportItem(content="I killed Handsome Jack with a sniper rifle")
        report_item_1.created_by=user_2
        report_item_1.save()
        report_item_1.tags.add('Handsome Jack')

        report_item_2 = ReportItem(content="I got chased by skags all the way to Sanctuary")
        report_item_2.created_by=user_1
        report_item_2.save()
        report_item_2.tags.add('Sanctuary')

        report_item_3 = ReportItem(content="Scooter is afraid of Handsome Jack")
        report_item_3.created_by=user_1
        report_item_3.save()
        report_item_3.tags.add('Scooter', 'Handsome Jack')

        report_item_4 = ReportItem(content="I found a love letter from Scooter to Ellie")
        report_item_4.created_by=user_2
        report_item_4.save()
        report_item_4.tags.add('Scooter', 'Ellie')

        report_item_5 = ReportItem(content="Sanctuary is a flying city powered by Lillith")
        report_item_5.created_by=user_3
        report_item_5.save()
        report_item_5.tags.add('Sanctuary', 'Lillith')
