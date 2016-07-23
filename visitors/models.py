from django.db import models


class Visitor(models.Model):
    report_month = models.CharField(max_length=100)
    area = models.CharField(max_length=200)
    reason = models.CharField(max_length=300)
    visitor_num = models.IntegerField(default=0)

    def __str__(self):
        str_text = str(self.report_month)
        str_text = str_text + ' ' + str(self.area)
        str_text = str_text + ' ' + str(self.reason)
        str_text + str_text + ' ' + str(self.visitor_num)
        return str_text


