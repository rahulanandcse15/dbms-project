from django.conf.urls import url
from . import views

urlpatterns =[
    url(r'^$', views.home, name='homepage'),
    url(r'^curriculum/$', views.curriculum, name='curriculum'),
    url(r'^admission/$', views.admission, name='admission'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^introduction/$', views.introduction, name='intro'),
    url(r'^principal_message/$',views.pri_message, name='principal_message'),
    url(r'^facilities/$',views.facilities, name='facility'),
    url(r'^galary/$',views.galary, name='galary'),
    url(r'^director/$',views.director,name='director'),
    url(r'^details/$',views.detail, name='detail'),
    url(r'^founder_message/$',views.founder_message,name='founder_message'),
    url(r'^login/$', views.login, name='loginpage'),
    url(r'^auser/$',views.login,name='admin'),
    url(r'^euser$',views.login,name='employee'),
    url(r'^suser/$',views.login,name='student'),
    url(r'^logout$',views.logout,name='logout'),
    url(r'^1/(?P<user_id>[0-9]+)/$',views.admin_page, name='admin_page'),
    url(r'^3/(?P<user_id>[0-9]+)/$',views.student_page, name='stu_page'),

    #add form

    url(r'^student/$',views.student, name="STUDENT"),
    url(r'^class/$',views.class_form, name="CLASS"),
    url(r'^teacher/$',views.teacher, name="TEACHER"),
    url(r'^cr/$',views.cr, name="CR"),
    url(r'^notice/$',views.notice, name="NOTICE"),
    url(r'^picture/$',views.picture, name="Picture"),
    url(r'^employee/$',views.employee, name="EMPLOYEE"),
    url(r'^report/$',views.report, name="REPORT"),
    url(r'^receipt/$',views.receipt, name="RECEIPT"),
    url(r'^principal/$',views.principal, name="PRINCIPAL"),
    url(r'^lab/$',views.lab, name="LAB"),
    url(r'^attendence/$',views.attendence, name="ATTENDENCE"),
    url(r'^subject/$',views.subject, name="SUBJECT"),
    url(r'^new_user/$',views.new_user, name="LOGIN"),
    url(r'^marquee/$',views.marquee, name="MARQUEE"),
    url(r'^achievement/$',views.achievement,name="ACHIEVEMENTS"),
    url(r'^events/$',views.event, name="EVENTS"),
    #submit add forms

    url(r'^add_class/$',views.class_add, name="add_CLASS"),
    url(r'^add_subject/$',views.subject_add, name="add_SUBJECT"),
    url(r'^add_teacher/$',views.teacher_add, name="add_TEACHER"),
    url(r'^add_user/$',views.user_add, name="add_LOGIN"),
    url(r'^add_student/$',views.student_add, name="add_STUDENT"),
    url(r'^add_cr/$',views.cr_add, name="add_CR"),
    url(r'^add_notice/$',views.notice_add, name="add_NOTICE"),
    url(r'^add_marquee/$',views.marquee_add, name="add_flash_message"),
    url(r'^add_galary/$',views.galary_add, name="add_galary"),
    url(r'^add_achievement/$',views.achievement_add, name="add_achievement"),
    url(r'^add_event/$',views.event_add, name="add_event"),
    url(r'^add_employee/$',views.employee_add, name="add_EMPLOYEE"),
    url(r'^add_report/$',views.report_add, name="add_REPORT"),
    url(r'^add_receipt/$',views.receipt_add, name="add_RECEIPT"),
    url(r'^add_principal/$',views.principal_add, name="add_PRINCIPAL"),
    url(r'^add_lab/$',views.lab_add, name="add_LAB"),
    url(r'^add_attendence/$',views.attendence_add, name="add_ATTENDENCE"),

    #modify_table
    url(r'^table_modify/$',views.modify_table, name="modify_table"),
    url(r'^album_modify/$',views.album_modify, name="album_modify"),
    url(r'^event_modify/$',views.event_modify, name="event_modify"),
    url(r'^achievement_modify/$',views.achievement_modify, name="achievement_modify"),

]