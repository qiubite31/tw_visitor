from django.db import models


class ArrivalRecord(models.Model):
    report_year = models.IntegerField(default=0000)
    report_month = models.IntegerField(default=00)
    continent = models.CharField(max_length=100)
    area_cht = models.CharField(max_length=200)
    area_eng = models.CharField(max_length=200)
    purpose_cht = models.CharField(max_length=300)
    purpose_eng = models.CharField(max_length=300)
    visitor_num = models.IntegerField(default=0)

    def __str__(self):
        str_text = str(self.report_month)
        str_text = str_text + ' ' + str(self.area_cht)
        str_text = str_text + ' ' + str(self.purpose_cht)
        str_text + str_text + ' ' + str(self.visitor_num)
        return str_text
