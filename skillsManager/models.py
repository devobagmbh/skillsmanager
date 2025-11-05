from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.urls import reverse
from auditlog.registry import auditlog


class Profile(models.Model):
    given_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    active_since = models.DateField(default=now)
    active_until = models.DateField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("profile-view", kwargs={"pk": self.pk})

    def __str__(self):
        return "%s, %s (%s)" % (self.last_name, self.given_name, self.email)


auditlog.register(Profile)


class ProfileMeta(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    birthday = models.DateField()
    photo = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.profile.__str__()


auditlog.register(ProfileMeta)


class Skill(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    related_skills = models.ManyToManyField("self", symmetrical=False, blank=True)

    def get_absolute_url(self):
        return reverse("skill-view", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class ProfileSkillReference(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.IntegerField()
    favorite = models.IntegerField()
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s - %d/%d" % (self.skill.name, self.level, self.favorite)


class Customer(models.Model):
    name = models.CharField(max_length=200)
    parent_customer = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.SET_NULL
    )
    active_since = models.DateField(default=now)
    active_until = models.DateField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("customer-view", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class CustomerLog(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    notice = models.TextField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return "%s (%s)" % (self.customer.name, self.timestamp.isoformat())


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    active_since = models.DateField(default=now)
    active_until = models.DateField(blank=True, null=True)

    def __str__(self):
        return "%s/%s" % (self.customer.name, self.name)


class ProjectLog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    notice = models.TextField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return "%s (%s)" % (self.customer.name, self.timestamp.isoformat())


class CertificateVendor(models.Model):
    name = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse("vendor-view", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class Certificate(models.Model):
    vendor = models.ForeignKey(CertificateVendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s (%s)" % (self.name, self.vendor)


class ProfileCertificateReference(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)
    active_since = models.DateField(default=now)
    active_until = models.DateField(blank=True, null=True)

    def __str__(self):
        return "%s %s-%s" % (
            self.certificate.name,
            self.active_since,
            self.active_until,
        )


class Template(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    template = models.TextField()

    def get_absolute_url(self):
        return reverse("template-view", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name
