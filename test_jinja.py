from jinja2 import Template
template = Template("""
{% set status_color = 'green' if current_status == 'Clocked In' else 'gray' %}
<h2>Status: <span style="color: {{ status_color }};">{{ current_status }}</span></h2>
""")
print(template.render(current_status='Clocked In'))
