from django.db import models


class State(models.Model):

    class Meta:
        db_table = 'states'

    state_id = models.AutoField(primary_key=True)
    iso_a2 = models.CharField(max_length=2)
    name = models.CharField(max_length=14)


class Election(models.Model):

    class Meta:
        db_table = 'elections'

    election_id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=2)
    year = models.PositiveSmallIntegerField()


class StateElectionResult(models.Model):

    class Meta:
        db_table = 'state_election_results'

    election = models.OneToOneField('Election', primary_key=True)
    # election_id = models.OneToOneField('Election', primary_key=True)
    votes_dem = models.PositiveIntegerField()
    votes_rep = models.PositiveIntegerField()
    votes_other = models.PositiveIntegerField()
    votes_total = models.PositiveIntegerField()
    votes_wasted_dem = models.PositiveIntegerField()
    votes_wasted_rep = models.PositiveIntegerField()
    votes_wasted_net = models.PositiveIntegerField()
    efficiency_gap = models.DecimalField(max_digits=4, decimal_places=3)

class DistrictElectionResult(models.Model):

    class Meta:
        db_table = 'district_election_results'

    district_election_results_id = models.AutoField(primary_key=True)
    election_id = models.ForeignKey('Election')
    number = models.PositiveSmallIntegerField()
    votes_dem = models.PositiveIntegerField()
    votes_rep = models.PositiveIntegerField()
    votes_other = models.PositiveIntegerField()
    votes_total = models.PositiveIntegerField()
    votes_wasted_dem = models.PositiveIntegerField()
    votes_wasted_rep = models.PositiveIntegerField()
    votes_wasted_net = models.PositiveIntegerField()
