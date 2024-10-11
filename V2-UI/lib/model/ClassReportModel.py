
class ClassReportModel:
    def __init__(self):
        self.title = ''
        self.class_name = ""
        self.student_amount = 0
        self.subject_scores = []
        self.subject_distributions = []
        self.level_a_lists = []

class SubjectStatScoreModel:
    def __init__(self, subject, average_score, top_score, bottom_score, median_score, stderr):
        self.subject = subject
        self.average_score = average_score
        self.top_score = top_score
        self.bottom_score = bottom_score
        self.median_score = median_score
        self.stderr = stderr



class SubjectDistributionModel:
    def __init__(self, subject, level_a_amount, level_b_amount, level_c_amount, level_d_amount, level_a_students, level_b_students, level_c_students, level_d_students):
        self.subject = subject
        self.level_a_amount = level_a_amount
        self.level_b_amount = level_b_amount
        self.level_c_amount = level_c_amount
        self.level_d_amount = level_d_amount
        self.level_a_students = level_a_students
        self.level_b_students = level_b_students
        self.level_c_students = level_c_students
        self.level_d_students = level_d_students


class StudentScore:
    def __init__(self, name, score):
        self.name = name
        self.score = score        