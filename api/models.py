from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tournaments(models.Model):
    name = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    openDate = models.DateField(null=True, blank=True)
    closeDate = models.DateField(null=True, blank=True)

    img = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Tournaments"


class TournamentsRules(models.Model):
    tournament = models.ForeignKey(Tournaments, on_delete=models.CASCADE)
    rule = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Tournaments Rules"


class TournamentsRegister(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournaments, on_delete=models.CASCADE)

    team_name = models.CharField(max_length=1000, null=True, blank=True)
    captain_first_name = models.CharField(max_length=1000, null=True, blank=True)
    captain_last_name = models.CharField(max_length=1000, null=True, blank=True)
    email = models.CharField(max_length=1000, null=True, blank=True)
    cell_number = models.CharField(max_length=1000, null=True, blank=True)


class Camps(models.Model):
    name = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    openDate = models.DateField(null=True, blank=True)
    closeDate = models.DateField(null=True, blank=True)

    img = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Camps"


class CampsRules(models.Model):
    camp = models.ForeignKey(Camps, on_delete=models.CASCADE)
    rule = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Camps Rules"


class CampsRegister(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    camp = models.ForeignKey(Camps, on_delete=models.CASCADE)

    parent_first_name = models.CharField(max_length=1000, null=True, blank=True)
    parent_last_name = models.CharField(max_length=1000, null=True, blank=True)
    email = models.CharField(max_length=1000, null=True, blank=True)
    cell_number = models.CharField(max_length=1000, null=True, blank=True)


class CampsChildRegister(models.Model):
    camp_register = models.ForeignKey(CampsRegister, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)


class Leagues(models.Model):
    name = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    openDate = models.DateField(null=True, blank=True)
    closeDate = models.DateField(null=True, blank=True)

    img = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Leagues"


class LeaguesRules(models.Model):
    league = models.ForeignKey(Leagues, on_delete=models.CASCADE)
    rule = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Leagues Rules"


class LeaguesRegister(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(Leagues, on_delete=models.CASCADE)

    team_name = models.CharField(max_length=1000, null=True, blank=True)
    captain_first_name = models.CharField(max_length=1000, null=True, blank=True)
    captain_last_name = models.CharField(max_length=1000, null=True, blank=True)
    email = models.CharField(max_length=1000, null=True, blank=True)
    cell_number = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name_plural = "League Team Registration"

    def __str__(self):
        return str(self.team_name)


class LeagueSchedule(models.Model):
    league = models.OneToOneField(Leagues, on_delete=models.CASCADE)
    img = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "League Schedule"

    def __str__(self):
        return str(self.league.name)


class LeagueTeamStats(models.Model):
    leagues_register = models.OneToOneField(LeaguesRegister, on_delete=models.CASCADE)
    wins = models.IntegerField(null=True, blank=True)
    losses = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "League Team Stats"

    def __str__(self):
        return str(self.leagues_register.league.name)


class LeagueTeamMembers(models.Model):
    leagues_register = models.ForeignKey(LeaguesRegister, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000, null=True, blank=True)
    points = models.IntegerField(default=0, null=True, blank=True)
    rebounds = models.IntegerField(default=0, null=True, blank=True)
    assists = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        verbose_name_plural = "League Team Members"

    def __str__(self):
        return str(self.name)
