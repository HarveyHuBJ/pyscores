import json
import os
from dotenv import load_dotenv

class AppSettings:
    
    def __init__(self):
        self.grade_config = {}
        self.load_defaults()        
    

    def load_defaults(self):
        load_dotenv()
        self.default_grade = os.getenv("INIT_GRADE", 7)
        self.default_school = os.getenv("INIT_SCHOOL", "xx学校")
        self.default_exam = os.getenv("INIT_EXAM", "测验")
        pass

    def load_grade_config(self, json_file):
    # 读取年级科目配置文件
        with open(json_file, 'r', encoding='utf-8') as f:
            self.grade_config = json.load(f)



    