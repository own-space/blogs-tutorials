from django.utils.text import slugify

import random
import string

# below method generate random string
def generate_random_string(N):
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))
    return res


def generate_slug(text):
    new_slug = slugify(text)
    print("New Slug : ", new_slug)
    from blog_app.models import Post
    
    if Post.objects.filter(slug = new_slug).first():
        return generate_slug(text +  generate_random_string(5))
    return new_slug