from django.db import models

class IdOrderingModelAbstract(models.Model):
    class Meta:
        abstract = True
        ordering = ('id',)

class Group(IdOrderingModelAbstract):
    OKR_CHOICES = (
        (0, 'bachelor'),
        (1, 'magister'),
        (2, 'specialist'),
    )

    TYPE_CHOICES = (
        (0, 'daily'),
        (1, 'extramural'),
    )

    name = models.CharField(max_length=20, unique=True)
    okr = models.IntegerField(choices=OKR_CHOICES)
    type = models.IntegerField(choices=TYPE_CHOICES)

    def __str__(self):
        return self.name

    class Meta(IdOrderingModelAbstract.Meta):
        permissions = (
            ('edit_group_timetable', 'Edit Group Timetable'),
        )

class Building(IdOrderingModelAbstract):
    name = models.CharField(unique=True, max_length=30)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return str(self.name)

class Room(IdOrderingModelAbstract):
    name = models.CharField(max_length=30)
    building = models.ForeignKey(Building)
    kpimaps_id = models.IntegerField(null=True, blank=True)

    def full_name(self):
        return '{0}-{1}'.format(self.name, self.building.name)

    def __str__(self):
        return self.full_name()

    class Meta(IdOrderingModelAbstract.Meta):
        unique_together = (('name', 'building'),)

class Discipline(IdOrderingModelAbstract):
    name = models.TextField()
    full_name = models.TextField(unique=True)

    def __str__(self):
        return self.name

class Teacher(IdOrderingModelAbstract):
    last_name = models.TextField()
    first_name = models.TextField(blank=True)
    middle_name = models.TextField(blank=True)
    degree = models.TextField(blank=True)

    def name(self):
        name = self.last_name
        if self.first_name:
            name += ' ' + self.first_name
        if self.middle_name:
            name += ' ' + self.middle_name
        return name

    def full_name(self):
        full_name = self.last_name
        if self.degree:
            full_name = self.degree + ' ' + full_name
        if self.first_name:
            full_name += ' ' + self.first_name
        if self.middle_name:
            full_name += ' ' + self.middle_name

        return full_name

    def short_name(self):
        short_name = self.last_name
        if self.first_name:
            short_name += ' ' + self.first_name[0] + '.'
        if self.middle_name:
            short_name += ' ' + self.middle_name[0] + '.'

        return short_name

    def short_name_with_degree(self):
        short_name = self.short_name()
        short_degree = ''
        if self.degree:
            degree_parts = self.degree.split()
            for part in degree_parts:
                short_degree += part[0:2]
                part = part[2:]
                for ch in part:
                    if ch not in 'aeiouyAEIOUYауоыиэяюёеіїєАУОЫИЭЯЮЁЕІЇЄ':
                        short_degree += ch
                    else:
                        break
                short_degree += '. '

            short_name = short_degree + short_name

        return short_name

    def __str__(self):
        return self.name()

    class Meta(IdOrderingModelAbstract.Meta):
        unique_together = (('last_name', 'first_name', 'middle_name', 'degree'))
        permissions = (
            ('edit_teacher_timetable', 'Edit Teacher Timetable'),
        )

class Lesson(IdOrderingModelAbstract):
    NUMBER_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
    )

    DAY_CHOICES = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
    )

    WEEK_CHOICES = (
        (1, 'Week 1'),
        (2, 'Week 2'),
    )

    TYPE_CHOICES = (
        (0, 'lecture'),
        (1, 'practical'),
        (2, 'laboratory'),
    )

    number = models.IntegerField(choices=NUMBER_CHOICES)
    day = models.IntegerField(choices=DAY_CHOICES)
    week = models.IntegerField(choices=WEEK_CHOICES)
    type = models.IntegerField(choices=TYPE_CHOICES, null=True, blank=True)
    discipline = models.ForeignKey(Discipline)
    groups = models.ManyToManyField(Group)
    teachers = models.ManyToManyField(Teacher, blank=True)
    rooms = models.ManyToManyField(Room, blank=True)

    def discipline_name(self):
        return self.discipline.name

    def groups_names(self):
        groups_names = []
        for group in self.groups.all():
            groups_names.append(group.name)
        return groups_names

    def teachers_short_names(self):
        teachers_short_names = []
        for teacher in self.teachers.all():
            teachers_short_names.append(teacher.short_name())
        return teachers_short_names

    def rooms_full_names(self):
        rooms_full_names = []
        for room in self.rooms.all():
            rooms_full_names.append(room.full_name())
        return rooms_full_names

    def __str__(self):
        return self.discipline.name
