from django.db import models
from django.db.models import Q, Sum

# Create your models here.
class Filials(models.Model):
    name = models.CharField(max_length=50)

class Series(models.Model):
    name = models.CharField(max_length=50)
    stake = models.FloatField()

class MileageManager(models.Manager):

    def chart_data(self, date_from=None, date_to=None, filial=None, serie=None):
        q = Q()
        if date_from:
            q &= Q(date__gte=date_from)
        if date_to:
            q &= Q(date__lt=date_to)
        if filial:
            q &= Q(filial__in=filial)
        if serie:
            q &= Q(serie_name__in=serie)
        years_income = {}
        avg_stake = Series.objects.all().aggregate(Sum('stake'))['stake__sum']
        for r in self.filter(q).select_related('serie').order_by('date'):
            if r.serie is None:
                # some series have no stakes
                income = r.value * avg_stake
            else:
                income = r.value * r.serie.stake
            year = r.date.strftime('%Y')
            years_income[year] = years_income.setdefault(year, 0) + income
        result = {'years': [], 'income': []}
        for year in sorted(years_income):
            result['years'].append(year)
            result['income'].append(years_income[year])

        #mileage
        #for r in self.filter(q).values('date').annotate(Sum('value')).order_by('date'):
        #    result['years'].append(r['date'].strftime('%Y'))
        #    result['mileage'].append(r['value__sum'])
        return result

class Mileage(models.Model):
    objects = MileageManager()
    filial = models.ForeignKey(Filials, models.CASCADE)
    serie = models.ForeignKey(Series, models.CASCADE, null=True)
    serie_name = models.CharField(max_length=50)
    date = models.DateField()
    value = models.IntegerField()