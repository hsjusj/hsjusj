from django.test import TestCase

# Create your tests here.

import re

filename = 'jsdkl.jpg'

print(type(hash(filename)))

ret = re.match('.*(\..*)', '')
print(ret.group(1))