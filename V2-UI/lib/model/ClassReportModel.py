
class ClassReportModel:
    def __init__(self):
        self.title = ''
        self.class_name = ""
        self.student_amount = 0
        self.subject_scores = []
        self.subject_distributions = []
        self.level_a_lists = []

class SubjectStatScoreModel:
    # 统计结果
    def __init__(self, subject, average_score, top_score, bottom_score, median_score, stderr):
        self.subject = subject
        self.average_score = average_score
        self.top_score = top_score
        self.bottom_score = bottom_score
        self.median_score = median_score
        self.stderr = stderr



class SubjectDistributionModel:
    # 统计结果
    def __init__(self, subject, level_a_amount, level_b_amount, level_c_amount, level_d_amount,level_f_amount
                 , level_a_students, level_b_students, level_c_students, level_d_students, level_f_students):
        self.subject = subject
        self.level_a_amount = level_a_amount
        self.level_b_amount = level_b_amount
        self.level_c_amount = level_c_amount
        self.level_d_amount = level_d_amount
        self.level_f_amount = level_f_amount
        self.level_a_students = [StudentScore(item) for item in level_a_students]
        self.level_b_students = [StudentScore(item) for item in level_b_students] 
        self.level_c_students = [StudentScore(item) for item in level_c_students] 
        self.level_d_students = [StudentScore(item) for item in level_d_students] 
        self.level_f_students = [StudentScore(item) for item in level_f_students] 

class LevelStatisticsModel:
    # 指定级别的学生人员列表
    def __init__(self, index, amount, students):
        self.index = index
        self.amount = amount
        self.students = students 

class ClassRankStudentModel:
    # 班级排名学生列表
    def __init__(self, class_rank, name, score, grade_rank):
        self.class_rank = int(class_rank)
        self.student_name = name
        self.score = score
        self.grade_rank = int(grade_rank)

class StudentScore:
    # 学生姓名和成绩
    def __init__(self, name_score):
        self.name = name_score[0]
        self.score = name_score[1]        