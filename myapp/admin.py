from django.contrib import admin
from myapp.models import *


admin.site.register(User)
admin.site.register(Booking)
admin.site.register(Concert)
admin.site.register(Admin)
admin.site.register(Customer)
admin.site.register(Dev)
admin.site.register(Payment)
admin.site.register(Ticket)
admin.site.register(Feedback)
admin.site.register(Message_with_Dev)
admin.site.register(Message_with_Admin)

