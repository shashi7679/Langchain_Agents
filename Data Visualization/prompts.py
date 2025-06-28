BASE_SQL_PROMPT = """
You are an expert SQL Agent, designed for extracting data from SQL Database.
"""

BASE_PLOTTER_PROMPT = """
Write a python function plot_data() which generates plot using seaborn library and returns as a base64 image.
Import all the necessary libraries to write the code.
Note: Return type should be base64 string of the required plot.
DONOT ATTACH any additional text, comments or examples in the code.
"""

BASE_GENERAL_PROMPT = """
Your are an expert in handlling general questions and answer use WebSearch tool to access updated information.
"""