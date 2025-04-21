from django.db import models

# Create your models here.

from authentication.models import BaseClass

class CrimeCategoryChoices(models.TextChoices):
    CYBER_CRIME = "Cyber Crime", "Cyber Crime"
    FINANCIAL_FRAUD = "Financial Fraud", "Financial Fraud"
    THEFT = "Theft", "Theft"
    LOST_PROPERTY = "Lost Property/Documents", "Lost Property/Documents"
    ONLINE_HARASSMENT = "Online Harassment or Threats", "Online Harassment or Threats"
    DOMESTIC_VIOLENCE = "Domestic Violence", "Domestic Violence"
    STALKING = "Stalking", "Stalking"
    MISSING_PERSON = "Missing Person", "Missing Person"
    PUBLIC_DISTURBANCE = "Public Disturbance", "Public Disturbance"
    DRUG_RELATED = "Drug-related Complaints", "Drug-related Complaints"
    VANDALISM = "Vandalism or Property Damage", "Vandalism or Property Damage"
    TRAFFIC_VIOLATION = "Traffic Violation", "Traffic Violation"
    SCAM_CALLS = "Fake Calls/Scam Calls", "Fake Calls/Scam Calls"
    IMPERSONATION = "Impersonation", "Impersonation"
    SUSPICIOUS_ACTIVITY = "Suspicious Activity", "Suspicious Activity"
    SEXUAL_HARASSMENT = "Sexual Harassment", "Sexual Harassment"
    HACKING = "Hacking or Data Breach", "Hacking or Data Breach"
    ILLEGAL_CONTENT = "Illegal Content Sharing", "Illegal Content Sharing"
    CHILD_ABUSE = "Child Exploitation or Abuse", "Child Exploitation or Abuse"
    NOISE_COMPLAINT = "Noise Complaint", "Noise Complaint"

class StatusChoices(models.TextChoices):

    PENDING = 'Pending','Pending'

    APPROVE = 'Approve','Approve'

    REJECTED = 'Reject','Reject'

class PoliceStatusChoices(models.TextChoices):

    UNDER_INVESTIGATION = 'Under Investigation','Under Investigation'

    SOLVED = 'Solved','Solved'

    CLOSED = 'Closed','Closed'
    

class CrimeReports(BaseClass):

    user = models.ForeignKey('authentication.Profile',on_delete=models.CASCADE)

    location = models.CharField(max_length=50)

    type_of_crime = models.CharField(max_length=50,choices=CrimeCategoryChoices.choices)

    description = models.TextField()

    evidence_1 = models.FileField(upload_to='evidences/')

    evidence_2 = models.FileField(upload_to='evidences/',null=True,blank=True)

    evidence_3 = models.FileField(upload_to='evidences/',null=True,blank=True)

    status = models.CharField(max_length=15,choices=StatusChoices.choices,default=StatusChoices.PENDING)

    p_officer = models.ForeignKey('authentication.Profile',on_delete=models.CASCADE,related_name='police')

    p_status = models.CharField(max_length=25,choices=PoliceStatusChoices.choices,default=PoliceStatusChoices.UNDER_INVESTIGATION)

    def __str__(self):

        return f'{self.user.first_name}-{self.type_of_crime}-Crime Report'
    
    class Meta:

        verbose_name = 'Crime Reports'

        verbose_name_plural = 'Crime Reports'  