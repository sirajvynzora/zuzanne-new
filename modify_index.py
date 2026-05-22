import re

with open('templates/frontend/index.html', 'r') as f:
    content = f.read()

# 1. Section titles (fade-up)
content = re.sub(r'(<div class="section-title2[^"]*">)', r'\1\n                <div class="wow fadeInUp">', content)
content = re.sub(r'(<!-- Section Title End -->)', r'</div>\n            \1', content)

# 2. Product cards with staggered delay
# This is tricky because we need to insert forloop logic inside the for loops.
# Let's just do it manually for the product cards since they are specific loops.

with open('templates/frontend/index.html', 'w') as f:
    f.write(content)
