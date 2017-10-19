from django.db import models
from datetime import datetime


class Account(models.Model):
    ballance = models.FloatField()
    version = models.IntegerField(default=0)

    def change_ballance(self, amount):
        if amount < 0 and abs(self.ballance) < abs(amount):
            return "Error ballance is too low"

        acc_qs = Account.objects.filter(
            id=self.id,
            version=self.version,
        )
        if acc_qs:
            acc = acc_qs[0]
            acc_qs.update(
                ballance=self.ballance + amount,
                version=self.version + 1,
            )
            BallanceHistory(
                ballance_change=amount,
                timestamp=datetime.now(),
                account=acc).save()
            return "Ballance updated"
        return "Cant update ballance"


class BallanceHistory(models.Model):
    ballance_change = models.FloatField()
    timestamp = models.DateTimeField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
