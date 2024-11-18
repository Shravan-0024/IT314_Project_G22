from django.contrib import admin
from .models import Notify
from .models import Feedback
from .models import Fav_loc
from .models import Recent_loc

# Register your models here.
admin.site.register(Notify)
admin.site.register(Feedback)
admin.site.register(Fav_loc)
admin.site.register(Recent_loc)