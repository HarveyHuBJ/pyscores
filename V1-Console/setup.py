from cx_Freeze import setup, Executable

setup(name="pyscore",
      version="1.0",
      description="Exam scores report for students",
      executables=[Executable("pyscore.py")]
      )