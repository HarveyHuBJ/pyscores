class StudentReportModel:
    def __init__(self):
        # title , student_name, class_name, subject_scores , summary
        self.title = "" 
        self.student_name = ""
        self.class_name = ""
        self.subject_scores = []
        self.summary = []


class SubjectScoreModel:
    def __init__(self): 
        self.subject = ""
        self.score = 0
        self.score_level = ""
        self.score_level_bound = 0
        self.class_rank = ""
        self.class_rank_amount = 0
        self.grade_rank = ""
        self.grade_rank_amount = 0
        self.is_major = False

    def get_class_rank_desc(self):
        n,k = int(self.class_rank), self.class_rank_amount

        if(k<=1):
            return f'第{int(n)}名'
        else:
            return f'第{int(n)}名，共{k}人并列'
        
    def get_grade_rank_desc(self):
        n,k = int(self.grade_rank), self.grade_rank_amount

        if(k<=1):
            return f'第{n}名'
        else:
            return f'第{n}名，共{k}人并列'
    
    def get_level_desc(self):
        # 将A线 B线 C线 D线 改成 class_a, class_b, class_c, class_d
        level = self.score_level.replace('线','').lower()
        return f'class_{level}'

        

   