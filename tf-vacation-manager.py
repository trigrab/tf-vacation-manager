from jinja2 import Template, FileSystemLoader, Environment

templateLoader = FileSystemLoader(searchpath="./")
templateEnv = Environment(loader=templateLoader)
template_file = "vacation_template.txt"
template = templateEnv.get_template(template_file)
outputText = template.render(start_date="21.01.2019", end_date="27.01.2019", username="ntw")

print(outputText)
