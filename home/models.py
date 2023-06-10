from django.db import models

from django.contrib.auth.models import Group
# Create your models here.

class Course(models.Model):
    """
    DEPARTMENT=(
        ('CSE', 'Computer Science'),
        ('ISE', 'Information Science'),
        ('AIML', 'Artificial Intelligence and Machine Learning'),
        ('ECE', 'Electronics and Communication'),
        ('DSC', 'Data Science'),
    )
    """

    SEM=(
        ('', 'Select Semester'),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
    )

    cname=models.CharField(max_length=200)
    ccode=models.CharField(max_length=200)
    #dept=models.CharField(max_length=200, choices=DEPARTMENT)
    dept=models.ForeignKey(Group, on_delete=models.CASCADE)
    sem=models.CharField(max_length=20, choices=SEM)
    date = models.DateTimeField(auto_now=True)
    #user_id=
    #modules=
    #papers=
    #include_asked=
    def __str__(self):
        return self.cname

class Module(models.Model):
    MOD_NO=(
        ('', 'Select Module No.'),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
    )

    modno=models.CharField(max_length=200, choices=MOD_NO)
    mname=models.CharField(max_length=200)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    #questions=
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['modno', 'course'], name="unique_course_module")
        ]

    def __str__(self):
        return self.mname
    

class Question(models.Model):
    DIFFICULTY_LEVEL=(
        ('', 'Select Difficulty Level'),
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    )

    COGNITIVE_LEVEL=(
        ('', 'Select Cognitive Level'),
        ('L1', 'L1'),
        ('L2', 'L2'),
        ('L3', 'L3'),
    )

    MARKS_RANGE=(
        ('', 'Select Marks'),
        ('8', '8'),
        ('16', '16'),
    )

    #QUESTION_TYPE=(('MCQ','MCQ'), ('Theory', 'Theory'))

    question=models.CharField(max_length=255)
    marks=models.CharField(max_length=200, choices=MARKS_RANGE)
    difficulty=models.CharField(max_length=200, choices=DIFFICULTY_LEVEL)
    rbt_level=models.CharField(max_length=200, choices=COGNITIVE_LEVEL)
    #qtype=models.CharField(max_length=200, choices=QUESTION_TYPE)
    #imp=
    #is_asked=
    module=models.ForeignKey(Module, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
    
class Mcq(models.Model):
    DIFFICULTY_LEVEL=(
        ('', 'Select Difficulty Level'),
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    )

    COGNITIVE_LEVEL=(
        ('', 'Select Cognitive Level'),
        ('L1', 'L1'),
        ('L2', 'L2'),
        ('L3', 'L3'),
    )

    MARKS_RANGE=(
        ('', 'Select Marks'),
        ('1', '1'),
        ('2', '2'),
    )

    #QUESTION_TYPE=(('MCQ','MCQ'), ('Theory', 'Theory'))

    question=models.CharField(max_length=255)
    option1=models.CharField(max_length=255)
    option2=models.CharField(max_length=255)
    option3=models.CharField(max_length=255)
    option4=models.CharField(max_length=255)
    marks=models.CharField(max_length=200, choices=MARKS_RANGE)
    difficulty=models.CharField(max_length=200, choices=DIFFICULTY_LEVEL)
    rbt_level=models.CharField(max_length=200, choices=COGNITIVE_LEVEL)
    #qtype=models.CharField(max_length=200, choices=QUESTION_TYPE)
    #imp=
    #is_asked=
    module=models.ForeignKey(Module, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class Paper(models.Model):
    SEM=(
        ('', 'Select Semester'),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
    )

    DIFFICULTY_LEVEL=(
        ('', 'Select Difficulty Level'),
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    )

    pname=models.CharField(max_length=255)
    #paper_logo=
    term=models.CharField(max_length=255)
    exam_date=models.CharField(max_length=255)
    #time_limit=
    #instructions=
    dept=models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)
    sem=models.CharField(max_length=20, choices=SEM)
    course=models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
    difficulty=models.CharField(max_length=20, choices=DIFFICULTY_LEVEL)
    qp=models.TextField()
    #mark=
    #paper_format=
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pname+" "+self.term
