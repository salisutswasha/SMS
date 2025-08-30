# admin.py
from django.contrib import admin
from .models import Attendance, StudentExtra, TeacherExtra, Notice, AdminExtra

@admin.action(description="Approve selected students")
def approve_students(modeladmin, request, queryset):
    queryset.update(status=True)

@admin.action(description="Approve selected teachers")
def approve_teachers(modeladmin, request, queryset):
    queryset.update(status=True)

class StudentExtraAdmin(admin.ModelAdmin):
    list_display = ("user", "cl", "mobile", "status")
    list_filter = ("status", "cl")
    search_fields = ("user__username", "user__first_name", "user__last_name", "mobile")
    actions = [approve_students]  # ← add this

admin.site.register(StudentExtra, StudentExtraAdmin)

class TeacherExtraAdmin(admin.ModelAdmin):
    list_display = ("username", "qualification", "mobile", "status")
    list_filter = ("status", "qualification")
    search_fields = ("username__username", "username__first_name", "username__last_name", "mobile")
    actions = [approve_teachers]  # ← and this

admin.site.register(TeacherExtra, TeacherExtraAdmin)

class AttendanceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Attendance, AttendanceAdmin)

class NoticeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Notice, NoticeAdmin)

class AdminExtraAdmin(admin.ModelAdmin):
    list_display = ("user", "status")
    list_filter = ("status",)
    search_fields = ("user__username",)

admin.site.register(AdminExtra, AdminExtraAdmin)
