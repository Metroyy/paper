from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.showdata, name='showdata'),
    path('choose/', views.choose, name='choose'),
    path('select/', views.select, name='select'),
    path('bar/', views.bar, name='bar'),
    path('insert/', views.insert, name='insert'),
    path('modifyselect/', views.modifyselect, name='modifyselect'),
    path('modify/', views.modify, name='modify'),
    path('speselect/', views.speselect, name='speselect'),
    path('speselid/', views.speselid, name='speselid'),
    path('modifyspe/', views.modifyspe, name='modifyspe'),
    path('insertspe/', views.insertspe, name='insertspe'),
    path('deletespe/', views.deletespe, name='deletespe'),
    path('writers/', views.writers, name='writers'),
    path('wriselid/', views.wriselid, name='wriselid'),
    path('modifywri/', views.modifywri, name='modifywri'),
    path('insertwri/', views.insertwri, name='insertwri'),
    path('deletewri/', views.deletewri, name='deletewri'),
    path('schselect/', views.schselect, name='schselect'),
    path('schselid/', views.schselid, name='schselid'),
    path('modifysch/', views.modifysch, name='modifysch'),
    path('insertspe/', views.insertspe, name='insertspe'),
    path('deletesch/', views.deletesch, name='deletesch'),
    path('ageselect/', views.ageselect, name='ageselect'),
    path('ageselid/', views.ageselid, name='ageselid'),
    path('modifyage/', views.modifyage, name='modifyage'),
    path('insertage/', views.insertage, name='insertage'),
    path('deleteage/', views.deleteage, name='deleteage'),
]
