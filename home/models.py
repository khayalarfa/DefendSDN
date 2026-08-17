from django.db import models

# Create your models here.
class User_Data(models.Model):
        Protocol= models.BigIntegerField()
        FlowDuration= models.BigIntegerField()
        FPLengthTotal= models.BigIntegerField()
        FlowBytesPers= models.BigIntegerField()
        FlowPacketsPers= models.BigIntegerField()
        FwdIATTotal= models.BigIntegerField()
        PacketLengthMean= models.BigIntegerField()
        AvgPacketSize= models.BigIntegerField()
        AvgFwdSegmentSize= models.BigIntegerField()
        SourceIP= models.BigIntegerField()