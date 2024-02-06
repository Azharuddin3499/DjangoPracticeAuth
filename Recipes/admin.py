from django.contrib import admin
from .models import *
from django.db.models import Sum
# Register your models here.

class RecipeAdmin(admin.ModelAdmin):
    list_display=['r_name','r_description','r_img']

admin.site.register(MyRecipes,RecipeAdmin)
admin.site.register(StudentID)
admin.site.register(Student)
admin.site.register(Department)


class SubjectAdmin(admin.ModelAdmin):
    list_display=['student','subject','marks']


class SubjectAdmin2(admin.ModelAdmin):
    list_display=['subject_name',]

admin.site.register(Subject,SubjectAdmin2)
admin.site.register(SubjectMarks,SubjectAdmin)

class ReportCardAdmin(admin.ModelAdmin):
    list_display=['student','student_rank','date_of_report_card_generation']

    def total_marks(self,obj):
        return obj.aggregate(Sum(''))
admin.site.register(ReportCard,ReportCardAdmin)