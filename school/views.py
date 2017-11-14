from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib import auth
import datetime
import base64
from django.db import connection,transaction

now = datetime.datetime.now()

cur = connection.cursor()

def home(request):
    query = 'SELECT * FROM NOTICE ORDER BY NOTICE_DATE DESC'
    cur.execute(query)
    result = cur.fetchall()
    query = 'SELECT * FROM ACHIEVEMENTS WHERE TYPE = 1'
    cur.execute(query)
    result1 = cur.fetchall()
    x = []
    for res in result1:
        tmp = []
        tmp.append(res[0])
        tmp.append(base64.encodestring(res[1]))
        x.append(tmp)
    query = 'SELECT * FROM ACHIEVEMENTS WHERE TYPE = 2'
    cur.execute(query)
    result1 = cur.fetchall()
    y = []
    for res in result1:
        tmp = []
        tmp.append(res[0])
        tmp.append(base64.encodestring(res[1]))
        y.append(tmp)
    return render(request, 'home.html',{'notices':result,'acheivements':x,'events':y})


def curriculum(request):
    return render(request,'curriculum.html')


def admission(request):
    return render(request,'admission.html')


def contact(request):
    return render(request,'contact.html')

def founder_message(request):
    return render(request,'founder_message.html')

def introduction(request):
    return render(request,'introduction.html')


def detail(request):
    return render(request,'detail.html')

def pri_message(request):
    return render(request,'p_message.html')

def director(request):
    return render(request,'d_messaage.html')

def facilities(request):
    return render(request,'facilities.html')

def galary(request):
    query = 'SELECT * FROM ALBUM ORDER BY EVENT'
    cur.execute(query)
    result = cur.fetchall()
    x = []
    for res in result:
        tmp = []
        tmp.append(res[0])
        tmp.append(res[1])
        tmp.append(base64.encodestring(res[2]))
        x.append(tmp)
    return render(request,'galary.html',{'entries':x})

def achievement(request):
    type = request.session.get('type')
    if type == 1:
        x = request.POST.get('action')
        modify = request.session.get('modify')
        if modify or str(x) == "ADD":
            if modify:
                del request.session['modify']
            else:
                modify = False
            return render(request, 'add_achievement.html', {'modify': modify})
        else:
            query = "SELECT * FROM ACHIEVEMENTS WHERE TYPE = 1"
            cur.execute(query)
            result = cur.fetchall()
            x = []
            for res in result:
                tmp = []
                tmp.append(res[0])
                tmp.append(base64.encodestring(res[1]))
                x.append(tmp)
            query1 = 'select column_name from information_schema.columns where table_name="ACHIEVEMENTS" '
            cur.execute(query1)
            result1 = cur.fetchall()
            table = "ACHIEVEMENTS"
            return render(request, 'achievement_modify.html', {'result': x, 'result1': result1, 'table': table})
    else:
        return redirect('loginpage')


def event(request):
    type = request.session.get('type')
    if type == 1:
        x = request.POST.get('action')
        modify = request.session.get('modify')
        if modify or str(x) == "ADD":
            if modify:
                del request.session['modify']
            else:
                modify = False
            return render(request, 'add_event.html', {'modify': modify})
        else:
            query = "SELECT * FROM ACHIEVEMENTS WHERE TYPE = 2"
            cur.execute(query)
            result = cur.fetchall()
            x = []
            for res in result:
                tmp = []
                tmp.append(res[0])
                tmp.append(base64.encodestring(res[1]))
                x.append(tmp)
            query1 = 'select column_name from information_schema.columns where table_name="ACHIEVEMENTS" '
            cur.execute(query1)
            result1 = cur.fetchall()
            table = "ACHIEVEMENTS"
            return render(request, 'event_modify.html', {'result': x, 'result1': result1, 'table': table})
    else:
        return redirect('loginpage')




def login(request):
    if request.method == 'POST':
        if request.POST.get('ausername'):
            username = request.POST.get('ausername')
            password = request.POST.get('apassword')
            aa = 'SELECT ID FROM LOGIN WHERE TYPE = %d AND USERNAME = "%s" AND PASSWORD = "%s" ' % (1, username, password)
            cur.execute(aa)
            x = cur.fetchall()
            if not x:
                error = True
                return render(request,'login.html',{'aerror':error})
            else:
                request.session['id'] = int(x[0][0])
                request.session['type'] = 1
                site = "/1/" + str(int(x[0][0])) + "/";
                return redirect(site)
        elif request.POST.get('susername'):
            username = request.POST.get('susername')
            password = request.POST.get('spassword')
            aa = 'SELECT ID FROM LOGIN WHERE TYPE = %d AND USERNAME = "%s" AND PASSWORD = "%s" ' % (3, username, password)
            cur.execute(aa)
            x = cur.fetchall()
            if not x:
                error = True
                return render(request, 'login.html', {'serror': error})
            else:
                request.session['id'] = int(x[0][0])
                request.session['type'] = 3
                site = "/3/" + str(int(x[0][0])) + "/";
                return redirect(site)
        else:
            return render(request, 'login.html')

    else:
        return render(request,'login.html')


def admin_page(request, user_id):
    x = request.session.get('id')
    if x and int(x) == int(user_id):
        aa = ' SELECT * FROM LOGIN WHERE ID = "%d" ' % int(x)
        cur.execute(aa)
        x = cur.fetchall()
        return render(request, 'admin.html', {'username':x[0][1], 'password':x[0][2], 'user_id':user_id})
    else:
        return redirect('loginpage')

""""
def employee_page(request, user_id):
    x = request.session.get('id')
    if x and int(x) == int(user_id):
        aa = ' SELECT * FROM TEACHER WHERE LOGIN_ID = "%d" ' % int(x)
        cur.execute(aa)
        xx = cur.fetchone()
        query1 = 'SELECT ID FROM CLASS WHERE CLASS_TEACHER_ID = %d'%(xx[0])
        query = 'SELECT ID, FIRST_NAME, LAST_NAME, ROLL FROM STUDENT WHERE CLASS_ID IN (%s)'%(query1)
        cur.execute(query)
        result = cur.fetchall()
        query1 = 'select column_name from information_schema.columns where TABLE_NAME = "%s"'%("TEACHER")
        cur.execute(query1)
        result1 = cur.fetchall()
        return render(request, 'employee.html', {'columns':result1,'details':xx,'students':result})
    else:
        return redirect('loginpage')
"""

def student_page(request, user_id):
    x = request.session.get('id')
    if x and int(x) == int(user_id):
        aa = ' SELECT * FROM STUDENT WHERE LOGIN_ID = "%d" ' % int(x)
        try:
            cur.execute(aa)
            xx = cur.fetchone()
        except:
            pass
        aa = ' SELECT PRESENT, TOTAL_CLASS FROM ATTENDENCE WHERE SID = "%d" AND YEAR = 2017 ' % (int(xx[0]))
        try:
            cur.execute(aa)
            yy = cur.fetchall()
        except:
            pass
        aa = ' SELECT SUBJECT_ID,MAX_MARKS,MARKS_OBT,EXAM_DES FROM REPORT WHERE SID = "%d" AND YEAR = 2017 '%(int(xx[0]))
        try:
            cur.execute(aa)
            zz = cur.fetchall()
        except:
            pass
        xxx = "STUDENT"
        query1 = 'select column_name from information_schema.columns where table_name = "%s"'%(xxx)
        try:
            cur.execute(query1)
            result1 = cur.fetchall()
        except:
            pass
        return render(request, 'student.html', {'details':xx,'attendence':yy,'report':zz,'columns':result1})
    else:
        return redirect('loginpage')


def logout(request):
    del request.session['id']
    del request.session['type']
    return redirect('homepage')


def student(request):
    type = request.session.get('type')
    if type == 1:
        x = request.POST.get('action')
        modify = request.session.get('modify')
        if modify or str(x) == "ADD":
            query = "SELECT * FROM CLASS"
            cur.execute(query)
            result = cur.fetchall()
            query = "SELECT * FROM LOGIN WHERE TYPE = 3"
            cur.execute(query)
            result1 = cur.fetchall()
            if modify:
                del request.session['modify']
            else:
                modify = False
            return render(request, 'add_student.html',{'classes':result,'ids':result1,'modify':modify})
        else:
            query = "SELECT * FROM STUDENT"
            cur.execute(query)
            result = cur.fetchall()
            query1 = 'select column_name from information_schema.columns where table_name="STUDENT" '
            cur.execute(query1)
            result1 = cur.fetchall()
            table = "STUDENT"
            return render(request, 'modify.html', {'result': result, 'result1': result1,'table':table})
    else:
        return redirect('loginpage')

def picture(request):
    type = request.session.get('type')
    if type == 1:
        x = request.POST.get('action')
        modify = request.session.get('modify')
        if modify or str(x) == "ADD":
            if modify:
                del request.session['modify']
            else:
                modify = False
            return render(request,'add_image.html',{'modify':modify})
        else:
            query = "SELECT * FROM ALBUM"
            cur.execute(query)
            result = cur.fetchall()
            x = []
            for res in result:
                tmp = []
                tmp.append(res[0])
                tmp.append(res[1])
                tmp.append(base64.encodestring(res[2]))
                x.append(tmp)
            query1 = 'select column_name from information_schema.columns where table_name="ALBUM" '
            cur.execute(query1)
            result1 = cur.fetchall()
            table = "ALBUM"
            return render(request, 'img_modify.html',{'result': x, 'result1': result1, 'table': table})
    else:
        return redirect('loginpage')

def class_form(request):
    type = request.session.get('type')
    if type == 1:
        x = request.POST.get('action')
        modify = request.session.get('modify')
        if modify or str(x) == "ADD":
            query = 'SELECT * FROM TEACHER'
            cur.execute(query)
            teacher = cur.fetchall()
            if modify:
                del request.session['modify']
            else:
                modify = False
            return render(request, 'add_class.html',{'teachers':teacher,'modify':modify})
        else:
            query = "SELECT * FROM CLASS"
            cur.execute(query)
            result = cur.fetchall()
            query1 = 'select column_name from information_schema.columns where table_name="CLASS" '
            cur.execute(query1)
            result1 = cur.fetchall()
            table = "CLASS"
            return render(request, 'modify.html', {'result': result, 'result1': result1, 'table': table})
    else:
        return redirect('loginpage')


def teacher(request):
    type = request.session.get('type')
    if type == 1:
        modify = request.session.get('modify')
        x = request.POST.get('action')
        query = "SELECT * FROM LOGIN WHERE TYPE = 2"
        cur.execute(query)
        result11 = cur.fetchall()
        if modify or str(x) == "ADD":
            if modify:
                del request.session['modify']
            else:
                modify = False
            return render(request, 'add_teacher.html',{'modify':modify,'ids':result11})
        else:
            query = "SELECT * FROM TEACHER"
            cur.execute(query)
            result = cur.fetchall()
            query1 = 'select column_name from information_schema.columns where table_name="TEACHER" '
            cur.execute(query1)
            result1 = cur.fetchall()
            table = "TEACHER"
            return render(request, 'modify.html', {'result': result, 'result1': result1, 'table': table})

    else:
        return redirect('loginpage')


def cr(request):
    type = request.session.get('type')
    if type == 1:
        modify = request.session.get("modify")
        x = request.POST.get('action')
        if modify or str(x) == "ADD":
            query = "SELECT * FROM CLASS"
            cur.execute(query)
            result = cur.fetchall()
            query1 = "SELECT * FROM STUDENT"
            cur.execute(query1)
            result1 = cur.fetchall()
            if modify:
                del request.session["modify"]
            else:
                modify = False
            print modify
            return render(request, 'add_cr.html',{'classes':result,'students':result1,'modify':modify})
        else:
            query = "SELECT * FROM CR"
            cur.execute(query)
            result = cur.fetchall()
            query1 = 'select column_name from information_schema.columns where table_name="CR" '
            cur.execute(query1)
            result1 = cur.fetchall()
            table = "CR"
            return render(request, 'modify.html', {'result': result, 'result1': result1, 'table': table})
    else:
        return redirect('loginpage')

def notice(request):
    type = request.session.get('type')
    if type == 1:
        x = request.POST.get('action')
        modify = request.session.get("modify")
        if modify or str(x) == "ADD":
            if modify:
                del request.session['modify']
            else:
                modify = False
            return render(request,'add_notice.html',{'modify':modify})
        else:
            query = "SELECT * FROM NOTICE"
            cur.execute(query)
            result = cur.fetchall()
            query1 = 'select column_name from information_schema.columns where table_name="NOTICE" '
            cur.execute(query1)
            result1 = cur.fetchall()
            table = "NOTICE"
            return render(request, 'modify.html', {'result': result, 'result1': result1, 'table': table})
    else:
        return redirect('loginpage')

def marquee(request):
    type = request.session.get('type')
    if type == 1:
        x = request.POST.get('action')
        modify = request.session.get("modify")
        if modify or str(x) == "ADD":
            if modify:
                del request.session['modify']
            else:
                modify = False
            return render(request,'add_marquee.html',{'modify':modify})
        else:
            query = "SELECT * FROM MARQUEE"
            cur.execute(query)
            result = cur.fetchall()
            query1 = 'select column_name from information_schema.columns where table_name="MARQUEE" '
            cur.execute(query1)
            result1 = cur.fetchall()
            table = "MARQUEE"
            return render(request, 'modify.html', {'result': result, 'result1': result1, 'table': table})
    else:
        return redirect('loginpage')

def employee(request):
    type = request.session.get('type')
    if type == 1:
        x = request.POST.get('action')
        modify = request.session.get('modify')
        if modify or str(x) == "ADD":
            #modify = request.session.get('modify')
            if modify:
                del request.session['modify']
            else:
                modify = False
            return render(request, 'add_employee.html',{'modify':modify})
        else:
            query = "SELECT * FROM EMPLOYEE"
            cur.execute(query)
            result = cur.fetchall()
            query1 = 'select column_name from information_schema.columns where table_name="EMPLOYEE" '
            cur.execute(query1)
            result1 = cur.fetchall()
            table = "EMPLOYEE"
            return render(request, 'modify.html', {'result': result, 'result1': result1, 'table': table})
    else:
        return redirect('loginpage')

"""
def parent(request):
    type = request.session.get('type')
    if type == 1:
        x = request.POST.get('action')
        if not x or str(x) == "ADD":
            modify = request.session.get('modify')
            if modify:
                del request.session['modify']
            else:
                modify = False
            return render(request, 'add_parent.html',{'modify':modify})
        else:
            query = "SELECT * FROM PARENT"
            cur.execute(query)
            result = cur.fetchall()
            query1 = 'select column_name from information_schema.columns where table_name="PARENT" '
            cur.execute(query1)
            result1 = cur.fetchall()
            table = "PARENT"
            filter = []
            for col in result1:
                query = 'SELECT DISTINCT %s FROM PARENT' % (col)
                cur.execute(query)
                res = cur.fetchall()
                filter.append(res)
            return render(request, 'modify.html', {'filters':filter,'result': result, 'result1': result1, 'table': table})
    else:
        return redirect('loginpage')
"""

def report(request):
    type = request.session.get('type')
    if type == 1:
        x = request.POST.get('action')
        modify = request.session.get('modify')
        if modify or str(x) == "ADD":
            query1 = "SELECT * FROM STUDENT"
            cur.execute(query1)
            result1 = cur.fetchall()
            query = "SELECT * FROM SUBJECT"
            cur.execute(query)
            result = cur.fetchall()
            #modify = request.session.get('modify')
            if modify:
                del request.session['modify']
            else:
                modify = False
            return render(request, 'add_report.html',{'students':result1, 'subjects':result,'modify':modify})
        else:
            query = "SELECT * FROM REPORT"
            cur.execute(query)
            result = cur.fetchall()
            query1 = 'select column_name from information_schema.columns where table_name="REPORT" '
            cur.execute(query1)
            result1 = cur.fetchall()
            table = "REPORT"
            return render(request, 'modify.html', {'result': result, 'result1': result1, 'table': table})
    else:
        return redirect('loginpage')


def receipt(request):
    type = request.session.get('type')
    if type == 1:
        x = request.POST.get('action')
        modify = request.session.get('modify')
        if modify or str(x) == "ADD":
            query1 = "SELECT * FROM STUDENT"
            cur.execute(query1)
            result1 = cur.fetchall()
            query = "SELECT * FROM EMPLOYEE"
            cur.execute(query)
            result = cur.fetchall()
            #modify = request.session.get('modify')
            if modify:
                del request.session['modify']
            else:
                modify = False
            return render(request, 'add_receipt.html',{'students':result1,'employees':result,'modify':modify})
        else:
            query = "SELECT * FROM RECEIPT"
            cur.execute(query)
            result = cur.fetchall()
            query1 = 'select column_name from information_schema.columns where table_name="RECEIPT" '
            cur.execute(query1)
            result1 = cur.fetchall()
            table = "RECEIPT"
            return render(request, 'modify.html', {'result': result, 'result1': result1, 'table': table})
    else:
        return redirect('loginpage')


def principal(request):
    type = request.session.get('type')
    if type == 1:
        x = request.POST.get('action')
        modify = request.session.get('modify')
        if modify or str(x) == "ADD":
            query = "SELECT * FROM TEACHER"
            cur.execute(query)
            result = cur.fetchall()
            #modify = request.session.get('modify')
            if modify:
                del request.session['modify']
            else:
                modify = False
            return render(request, 'add_principal.html',{'teachers':result,'modify':modify})
        else:
            query = "SELECT * FROM PRINCIPAL"
            cur.execute(query)
            result = cur.fetchall()
            query1 = 'select column_name from information_schema.columns where table_name="PRINCIPAL" '
            cur.execute(query1)
            result1 = cur.fetchall()
            table = "PRINCIPAL"
            return render(request, 'modify.html', {'result': result, 'result1': result1, 'table': table})
    else:
        return redirect('loginpage')


def lab(request):
    type = request.session.get('type')
    if type == 1:
        x = request.POST.get('action')
        modify = request.session.get('modify')
        if modify or str(x) == "ADD":
            query = "SELECT * FROM TEACHER"
            cur.execute(query)
            result = cur.fetchall()
            #modify = request.session.get('modify')
            if modify:
                del request.session['modify']
            else:
                modify = False
            return render(request, 'add_lab.html',{'teachers':result,'modify':modify})
        else:
            query = "SELECT * FROM LAB"
            cur.execute(query)
            result = cur.fetchall()
            query1 = 'select column_name from information_schema.columns where table_name="LAB" '
            cur.execute(query1)
            result1 = cur.fetchall()
            table = "LAB"
            return render(request, 'modify.html', {'result': result, 'result1': result1, 'table': table})
    else:
        return redirect('loginpage')


def attendence(request):
    type = request.session.get('type')
    if type == 1:
        x = request.POST.get('action')
        modify = request.session.get('modify')
        if modify or str(x) == "ADD":
            query1 = "SELECT * FROM STUDENT"
            cur.execute(query1)
            result1 = cur.fetchall()
            #modify = request.session.get('modify')
            if modify:
                del request.session['modify']
            else:
                modify = False
            return render(request, 'add_attendence.html',{'students':result1,'modify':modify})
        else:
            query = "SELECT * FROM ATTENDENCE"
            cur.execute(query)
            result = cur.fetchall()
            query1 = 'select column_name from information_schema.columns where table_name="ATTENDENCE" '
            cur.execute(query1)
            result1 = cur.fetchall()
            table = "ATTENDENCE"
            return render(request, 'modify.html', {'result': result, 'result1': result1, 'table': table})
    else:
        return redirect('loginpage')


def subject(request):
    type = request.session.get('type')
    if type == 1:
        x = request.POST.get('action')
        modify = request.session.get('modify')
        if modify or str(x) == "ADD":
            query = "SELECT * FROM TEACHER"
            cur.execute(query)
            result = cur.fetchall()
            #modify = request.session.get('modify')
            if modify:
                del request.session['modify']
            else:
                modify = False
            return render(request, 'add_subject.html',{'teachers':result,'modify':modify})
        else:
            query = "SELECT * FROM SUBJECT"
            cur.execute(query)
            result = cur.fetchall()
            query1 = 'select column_name from information_schema.columns where table_name="SUBJECT" '
            cur.execute(query1)
            result1 = cur.fetchall()
            table = "SUBJECT"
            return render(request, 'modify.html', {'result': result, 'result1': result1, 'table': table})
    else:
        return redirect('loginpage')


def new_user(request):
    type = request.session.get('type')
    if type == 1:
        x = request.POST.get('action')
        modify = request.session.get('modify')
        if modify or str(x) == "ADD":
            #modify = request.session.get('modify')
            if modify:
                del request.session['modify']
            else:
                modify = False
            return render(request, 'add_user.html',{'modify':modify})
        else:
            query = "SELECT * FROM LOGIN"
            cur.execute(query)
            result = cur.fetchall()
            query1 = 'select column_name from information_schema.columns where table_name="LOGIN" '
            cur.execute(query1)
            result1 = cur.fetchall()
            table = "LOGIN"
            return render(request, 'modify.html', {'result': result, 'result1': result1, 'table': table})
    else:
        return redirect('loginpage')


def subject_add(request):
    if request.method == "POST":
        syl = str(request.POST.get("syllabus"))
        year = int(request.POST.get("year"))
        tid = int(request.POST.get("tid"))
        if int(year) < int(now.year):
            if request.POST.get("action") == "Submit":
                query = 'INSERT INTO SUBJECT (SYLLABUS, YEAR, TID) VALUES( "%s", "%d", "%d")' % (str(syl), int(year), int(tid))
            else:
                id = request.session.get("table_id")
                query = 'UPDATE SUBJECT SET SYLLABUS="%s", YEAR = "%d", TID = "%d" WHERE ID = "%d"' % (str(syl), int(year), int(tid),int(id))
            cur.execute(query)
            transaction.commit()
            return render(request, 'success.html')
        else:
            if request.POST.get("action") == "modify":
                request.session["modify"] = True
            return redirect('SUBJECT')
    else:
        return redirect("loginpage")


def class_add(request):
    if request.method == "POST":
        house = request.POST.get("house")
        room = request.POST.get("room_no")
        boys = request.POST.get("boys")
        girls = request.POST.get("girls")
        tid = request.POST.get("tid")
        if request.POST.get("action") == "Submit":
            query = 'INSERT INTO CLASS (HOUSE, ROOM_NO, BOYS, GIRLS, CLASS_TEACHER_ID) VALUES( "%s", "%d", "%d", "%d","%d")' % (str(house), int(room), int(boys), int(girls), int(tid))
        else:
            id = request.session.get("table_id")
            query = 'UPDATE CLASS SET HOUSE="%s", ROOM_NO="%d", BOYS="%d", GIRLS="%d", CLASS_TEACHER_ID="%d" WHERE ID = "%d" ' % (str(house), int(room), int(boys), int(girls), int(tid), int(id))
        cur.execute(query)
        transaction.commit()
        return render(request, 'success.html')
    else:
        if request.POST.get("action") == "modify":
            request.session["modify"] = True
        return redirect("CLASS")


def teacher_add(request):
    if request.method == "POST":
        if request.POST.get("action") == "Submit":
            id = request.POST.get("id")
            ids = request.POST.get("ids")
        else:
            id = request.session.get("table_id")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        gender = request.POST.get("gender")
        quali = request.POST.get("qualification")
        exp = request.POST.get("experience")
        p_contact = request.POST.get("p_contact")
        s_contact = request.POST.get("sec_contact")
        salary = request.POST.get("salary")
        doj = request.POST.get("doj")
        area = request.POST.get("area")
        place = request.POST.get("place")
        dist = request.POST.get("district")
        state = request.POST.get("state")
        pin = request.POST.get("pincode")
        if len(str(pin)) == 6 and doj <= str(now)[:10]:
            if request.POST.get("action") == "Submit":
                query = 'INSERT INTO TEACHER(FIRST_NAME, LAST_NAME, GENDER, QUALIFICATION, EXPERIENCE, PRIMARY_CONTACT, SECONDARY_CONTACT, SALARY, DOJ, AREA, PLACE, DIST, STATE , PIN,LOGIN_ID) VALUES( "%s","%s","%s","%s","%d","%s","%s","%d","%s","%s","%s","%s","%s","%s","%d")' % (str(fname), str(lname), str(gender), str(quali), int(exp), str(p_contact), str(s_contact), int(salary), str(doj), str(area), str(place), str(dist), str(state), str(pin),int(ids))
            else:
                query = 'UPDATE TEACHER SET FIRST_NAME="%s", LAST_NAME="%s", GENDER="%s", QUALIFICATION="%s", EXPERIENCE="%d", PRIMARY_CONTACT="%s", SECONDARY_CONTACT="%s", SALARY="%d", DOJ="%s", AREA="%s", PLACE="%s", DIST="%s", STATE="%s", PIN="%s" WHERE ID = "%d" ' % (
                str(fname), str(lname), str(gender), str(quali), int(exp), str(p_contact), str(s_contact), int(salary),
                str(doj), str(area), str(place), str(dist), str(state), str(pin),int(id))
            cur.execute(query)
            transaction.commit()
            return render(request, 'success.html')
        else:
            if request.POST.get("action") == "modify":
                request.session["modify"] = True
            return redirect("TEACHER")
    else:
        return redirect("loginpage")


def user_add(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        type = request.POST.get("type")
        aa = 'SELECT * FROM LOGIN WHERE USERNAME = "%s" '%(username)
        cur.execute(aa)
        x = cur.fetchall()
        if request.POST.get("action") == "Submit":
            if not x:
                query = 'INSERT INTO LOGIN(USERNAME, PASSWORD, TYPE) VALUES ("%s","%s","%d")'%(str(username), str(password), int(type))
                cur.execute(query)
                transaction.commit()
                return render(request, 'success.html')
            else:
                if request.POST.get("action") == "modify":
                    request.session["modify"] = True
                return redirect("LOGIN")
        else:
            if x:
                id = request.session.get("table_id")
                query = 'UPDATE LOGIN SET USERNAME = "%s",PASSWORD = "%s", TYPE = "%d" WHERE ID = "%d"' % (str(username), str(password), int(type) ,int(id))
                cur.execute(query)
                transaction.commit()
                print query
                return render(request, 'success.html')
            else:
                return redirect("admin")
    else:
        return redirect("loginpage")


def student_add(request):
    if request.method == "POST":
        if request.POST.get("action") == "Submit":
            id = request.POST.get("id")
            ids = request.POST.get("ids")
        else:
            id = request.session.get("table_id")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        roll = request.POST.get("roll")
        cid = request.POST.get("cid")
        doj = request.POST.get("doj")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")
        place = request.POST.get("place" )
        dist = request.POST.get("district")
        state =request.POST.get("state")
        pin = request.POST.get("pincode")
        p_contact =request.POST.get("p_contact")
        s_contact= request.POST.get("sec_contact")
        if len(str(pin)) == 6:
            if request.POST.get("action") == "Submit":
                query = 'INSERT INTO STUDENT(ID,FIRST_NAME, LAST_NAME, ROLL, CLASS_ID, DOJ, GENDER, DOB, PLACE, DIST, STATE, PIN, PRIMARY_CONTACT, SECONDARY_CONTACT,LOGIN_ID) VALUES("%d","%s", "%s", "%d", "%d", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s","%s","%d")'%(int(id),str(fname), str(lname), int(roll), int(cid), str(doj),str(gender),str(dob),str(place), str(dist),str(state),str(pin),str(p_contact), str(s_contact),int(ids))
            else:
                query = 'UPDATE STUDENT SET FIRST_NAME = "%s", LAST_NAME="%s", ROLL="%d", CLASS_ID="%d", DOJ="%s", GENDER="%s", DOB="%s", PLACE="%s", DIST="%s", STATE="%s", PIN="%s", PRIMARY_CONTACT="%s", SECONDARY_CONTACT="%s" WHERE ID = "%d"' % (
                str(fname), str(lname), int(roll), int(cid), str(doj), str(gender), str(dob), str(place),
                str(dist), str(state), str(pin), str(p_contact), str(s_contact),int(id))
            cur.execute(query)
            transaction.commit()
            return render(request, 'success.html')
        else:
            if request.POST.get("action") == "modify":
                request.session["modify"] = True
            return redirect("STUDENT")
    else:
        return redirect("loginpage")


def cr_add(request):
    if request.method == "POST":
        sid = request.POST.get("sid")
        if request.POST.get("action") == "Submit":
            cid = request.POST.get("cid")
            year =request.POST.get("Year")
        else:
            cid = request.session.get("table_id")
            year=request.session.get("table_id1")
        if int(year) < 2018:
            if request.POST.get("action") == "Submit":
                query = 'INSERT INTO CR(SID, CID, YEAR) VALUES("%d","%d","%d")'%(int(sid),int(cid), int(year))
            else:
                query = 'UPDATE CR SET SID="%d" WHERE CID = "%d" AND YEAR = "%d" ' % (int(sid), int(cid), int(year))
            cur.execute(query)
            transaction.commit()
            return render(request, 'success.html')
        else:
            if request.POST.get("action") == "modify":
                request.session["modify"] = True
            return redirect("CR")


    else:
        return redirect("loginpage")


def notice_add(request):
    if request.method == "POST":
        title = request.POST.get("title")
        body = request.POST.get("body")
        issuer = request.POST.get("issuer")
        date = request.POST.get("notice_date")
        designation = request.POST.get("designation")
        if request.POST.get("action") == "Submit":
            query = 'INSERT INTO NOTICE(TITLE, BODY, ISSUER, NOTICE_DATE, DESIGNATION) VALUES("%s","%s","%s","%s","%s")'%(str(title),str(body),str(issuer),str(date),str(designation))
        else:
            id = request.session.get("table_id")
            query = 'UPDATE NOTICE SET TITLE="%s", BODY="%s", ISSUER="%s", NOTICE_DATE = "%s", DESIGNATION ="%s" WHERE ID = "%d"' % (
            str(title), str(body), str(issuer), str(date), str(designation), int(id))
        cur.execute(query)
        transaction.commit()
        return render(request, 'success.html')
    else:
        return redirect("loginpage")

def marquee_add(request):
    if request.method == "POST":
        detail = request.POST.get("detail")
        link = request.POST.get("link")
        if request.POST.get("action") == "Submit":
            if link:
                query = 'INSERT INTO MARQUEE(DETAIL,LINK) VALUES("%s","%s")'%(detail,link)
            else:
                query = 'INSERT INTO MARQUEE(DETAIL) VALUES("%s")' % (detail)
        else:
            id = request.session.get("table_id")
            if link:
                query = 'UPDATE MARQUEE SET DETAIL="%s", LINK="%s" WHERE ID = %s ' % (detail,link,id)
            else:
                query = 'UPDATE MARQUEE   SET DETAIL="%s"  WHERE ID = %s ' % (detail,id)
        cur.execute(query)
        transaction.commit()
        return render(request, 'success.html')
    else:
        return redirect("loginpage")


"""
def parent_add(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        gender = request.POST.get("gender")
        p_contact = request.POST.get("p_contact" )
        s_contact = request.POST.get("sec_contact")
        e_mail = request.POST.get("email")
        if request.method == "POST":
            if request.POST.get("action") == "Submit":
                query = 'INSERT INTO PARENT(FIRST_NAME, LAST_NAME, GENDER, PRIMARY_CONTACT, SECONDARY_CONTACT, EMAIL) VALUES("%s","%s","%s","%s","%s","%s")'%(str(fname),str(lname),str(gender),str(p_contact),str(s_contact),str(e_mail))
            else:
                id = request.session.get("table_id")
                query ='UPDATE PARENT SET FIRST_NAME="%s", LAST_NAME="%s", GENDER="%s", PRIMARY_CONTACT="%s", SECONDARY_CONTACT="%s", EMAIL="%s" WHERE ID = "%d" ' % (
                str(fname), str(lname), str(gender), str(p_contact), str(s_contact), str(e_mail),int(id))
            cur.execute(query)
            transaction.commit()
            return render(request, 'success.html')
    else:
        return redirect("loginpage")

"""
def employee_add(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        gender = request.POST.get("gender")
        doj = request.POST.get("doj")
        p_contact = request.POST.get("p_contact")
        s_contact = request.POST.get("sec_contact")
        salary = request.POST.get("salary")
        job = request.POST.get("job")
        place = request.POST.get("place")
        dist = request.POST.get("district")
        state = request.POST.get("state")
        pin = request.POST.get("pincode")
        if len(str(pin)) == 6:
            if request.POST.get("action") == "Submit":
                query = 'INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, GENDER, DOJ, PRIMARY_CONTACT, SECONDARY_CONTACT, SALARY, JOB, PLACE, DIST, STATE, PIN) VALUES("%s","%s","%s","%s","%s","%s","%d","%s","%s","%s","%s","%s")'%(str(fname),str(lname),str(gender),str(doj),str(p_contact),str(s_contact),int(salary),str(job),str(place), str(dist), str(state),str(pin))
            else:
                id = request.session.get("table_id")
                query = 'UPDATE EMPLOYEE SET FIRST_NAME="%s", LAST_NAME="%s", GENDER="%s", DOJ="%s", PRIMARY_CONTACT="%s", SECONDARY_CONTACT="%s", SALARY="%d", JOB="%s", PLACE="%s", DIST="%s", STATE="%s", PIN="%s" WHERE ID = "%d"' % (
                str(fname), str(lname), str(gender), str(doj), str(p_contact), str(s_contact), int(salary), str(job),
                str(place), str(dist), str(state), str(pin),int(id))
            cur.execute(query)
            transaction.commit()
            return render(request, 'success.html')
        else:
            if request.POST.get("action") == "modify":
                request.session["modify"] = True
            return redirect("EMPLOYEE")
    else:
        return  redirect("loginpage")


def report_add(request):
    if request.method == "POST":
        sid = request.POST.get("sid")
        sub_id = request.POST.get("subject_id")
        max_marks = request.POST.get("maxx_marks")
        marks_obt = request.POST.get("marks_obtained")
        year = request.POST.get("year")
        exam = request.POST.get("exam")
        if int(marks_obt) <= int(max_marks) and int(year) < 2018:
            if request.POST.get("action") == "Submit":
                query = 'INSERT INTO REPORT(SID, SUBJECT_ID, MAX_MARKS, MARKS_OBT, YEAR, EXAM_DES) VALUES("%d","%d","%d","%d","%d","%s")'%(int(sid),int(sub_id),int(max_marks),int(marks_obt),int(year),str(exam))
            else:
                id = request.session.get("table_id")
                query = 'UPDATE REPORT SET SID="%d", SUBJECT_ID="%d", MAX_MARKS="%d", MARKS_OBT="%d", YEAR="%d", EXAM_DES="%s" WHERE ID ="%d"' % (
                int(sid), int(sub_id), int(max_marks), int(marks_obt), int(year), str(exam),int(id))
            cur.execute(query)
            transaction.commit()
            return render(request, 'success.html')
        else:
            if request.POST.get("action") == "modify":
                request.session["modify"] = True
            return redirect("REPORT")
    else:
        return redirect("loginpage")


def receipt_add(request):
    if request.method == "POST":
        sid = request.POST.get("sid")
        fee = request.POST.get("fee_type")
        amount = request.POST.get("amount")
        date = request.POST.get("payment_date")
        payer = request.POST.get("payer")
        collector_id = request.POST.get("collector_id")
        if request.POST.get("action") == "Submit":
            query = 'INSERT INTO RECEIPT(SID, FEE_TYPE, AMOUNT, PAYMENT_DATE, PAYER, COLLECTOR_ID) VALUES("%d","%s","%d","%s","%s","%d")'%(int(sid), str(fee), int(amount), str(date),str(payer),int(collector_id))
        else:
            id = request.session.get("table_id")
            query = 'UPDATE RECEIPT SET SID="%d", FEE_TYPE="%s", AMOUNT="%d", PAYMENT_DATE="%s", PAYER="%s", COLLECTOR_ID="%d" WHERE ID = "%d"' % (int(sid), str(fee), int(amount), str(date), str(payer), int(collector_id),int(id))
        cur.execute(query)
        transaction.commit()
        return render(request, 'success.html')
    else:
        return redirect("loginpage")


def principal_add(request):
    if request.method == "POST":
        tid = request.POST.get("tid")
        start = request.POST.get("start")
        last = request.POST.get("end")
        if not last:
            if request.POST.get("action") == "Submit":
                query = 'INSERT INTO PRINCIPAL(TID, START) VALUES("%d","%s")'%(int(tid),str(start))
            else:
                id = request.session.get("table_id")
                query = 'UPDATE PRINCIPAL SET TID="%d", START="%s" WHERE ID = "%d"' % (int(tid), str(start), int(id))
        else:
            if request.POST.get("action") == "Submit":
                query = 'INSERT INTO PRINCIPAL(TID, START, LAST_DATE) VALUES("%d","%s","%s")'%(int(tid),str(start),str(last))
            else:
                id = request.session.get("table_id")
                query = 'UPDATE PRINCIPAL SET TID="%d", START="%s",LAST_DATE="%s" WHERE ID = "%d"' % (int(tid), str(start), str(last),int(id))
        cur.execute(query)
        transaction.commit()
        return render(request, 'success.html')
    else:
        return redirect("loginpage")


def lab_add(request):
    if request.method == "POST":
        build = request.POST.get("house")
        room = request.POST.get("room_no")
        subject = request.POST.get("subject")
        incharge = request.POST.get("tid")
        if request.POST.get("action") == "Submit":
            query = 'INSERT INTO LAB(BUILDING, ROOM_NO, SUBJECT, INCHARGE) VALUES("%s","%d","%s","%d")' % (str(build),int(room),str(subject), int(incharge))
        else:
            id = request.session.get("table_id")
            query =  'UPDATE LAB SET BUILDING="%s", ROOM_NO="%d", SUBJECT="%s", INCHARGE="%d" WHERE ID = "%d" ' % (str(build), int(room), str(subject), int(incharge),int(id))
        cur.execute(query)
        transaction.commit()
        return render(request, 'success.html')
    else:
        return redirect("loginpage")


def attendence_add(request):
    if request.method == "POST":
        sid = request.POST.get("sid")
        year = request.POST.get("Year")
        present = request.POST.get("present")
        total = request.POST.get("total")
        if int(year) < 2018 and int(present) <= int(total):
            if request.POST.get("action") == "Submit":
                query = 'INSERT INTO ATTENDENCE(SID, YEAR, PRESENT, TOTAL_CLASS) VALUES("%d","%d","%d","%d")'%(int(sid),int(year),int(present),int(total))
            else:
                id = request.session.get("table_id")
                query = 'UPDATE ATTENDENCE SET SID="%d", YEAR="%d", PRESENT="%d", TOTAL_CLASS="%d" WHERE ID="%d"' % (
                int(sid), int(year), int(present), int(total),int(id))
            cur.execute(query)
            transaction.commit()
            return render(request, 'success.html')
        else:
            if request.POST.get("action") == "modify":
                request.session["modify"] = True
            return redirect("ATTENDENCE")
    else:
        return redirect("loginpage")


def galary_add(request):
    if request.method == "POST":
        event = request.POST.get("event")
        image = request.FILES["image"].read()
        if request.POST.get("action") == "Submit":
            args = (str(event), image,)
            query = 'INSERT INTO ALBUM(EVENT,IMAGE) VALUES(%s,%s)'
        else:
            id = request.session.get("table_id")
            args = (str(event), image, id,)
            print type(args[2])
            query = 'UPDATE ALBUM SET EVENT=%s, IMAGE =%s WHERE ID =%s '
        cur.execute(query,args)
        transaction.commit()
        return render(request, 'success.html')
    else:
        return redirect("loginpage")

def achievement_add(request):
    if request.method == "POST":
        image = request.FILES["image"].read()
        if request.POST.get("action") == "Submit":
            args = (image,)
            query = 'INSERT INTO ACHIEVEMENTS(IMAGE,TYPE ) VALUES(%s,1)'
        else:
            id = request.session.get("table_id")
            args = (image, id,)
            query = 'UPDATE ACHIEVEMENTS SET IMAGE =%s WHERE ID =%s '
        cur.execute(query,args)
        transaction.commit()
        return render(request, 'success.html')
    else:
        return redirect("loginpage")

def event_add(request):
    if request.method == "POST":
        image = request.FILES["image"].read()
        if request.POST.get("action") == "Submit":
            args = (image,)
            query = 'INSERT INTO ACHIEVEMENTS(IMAGE,TYPE) VALUES(%s,2)'
        else:
            id = request.session.get("table_id")
            args = (image, id,)
            query = 'UPDATE ACHIEVEMENTS SET IMAGE =%s WHERE ID =%s '
        cur.execute(query,args)
        transaction.commit()
        return render(request, 'success.html')
    else:
        return redirect("loginpage")


def modify_table(request):
    x = request.POST.get("action")
    if not x:
        return redirect("loginpage")
    elif str(x) == "delete":
        table = request.POST.get("table")
        id = request.POST.get("id")
        id1 = request.POST.get("id1")
        if str(table) == "CR":
            query = 'DELETE FROM %s WHERE CID = %d  AND YEAR = %d '%(str(table), int(id), int(id1))
        else:
            query = 'DELETE FROM %s WHERE ID = %d'%(str(table), int(id))
        try:
            print query
            cur.execute(query)
            transaction.commit()
        except:
            pass
        query11 = 'SELECT * FROM %s'%(str(table))
        cur.execute(query11)
        result = cur.fetchall()
        query1 = 'select column_name from information_schema.columns where table_name=  "%s" '%(str(table))
        cur.execute(query1)
        result1 = cur.fetchall()
        table = str(table)
        return render(request, 'modify.html', {'result': result, 'result1': result1, 'table': table})
    elif str(x) == "modify":
        table = request.POST.get("table")
        request.session["modify"] = True
        request.session["table_id"] = request.POST.get("id")
        request.session["table_id1"] = request.POST.get("id1")
        return redirect(str(table))
    else:
        return redirect("loginpage")


def album_modify(request):
    x = request.POST.get("action")
    if not x:
        return redirect("loginpage")
    elif str(x) == "delete":
        id = request.POST.get("id")
        query = 'DELETE FROM ALBUM WHERE ID = %d'%(int(id))
        try:
            print query
            cur.execute(query)
            transaction.commit()
        except:
            pass
        query = "SELECT * FROM ALBUM"
        cur.execute(query)
        result = cur.fetchall()
        x = []
        for res in result:
            tmp = []
            tmp.append(res[0])
            tmp.append(res[1])
            tmp.append(base64.encodestring(res[2]))
            x.append(tmp)
        query1 = 'select column_name from information_schema.columns where table_name="ALBUM" '
        cur.execute(query1)
        result1 = cur.fetchall()
        table = "ALBUM"
        return render(request, 'img_modify.html', {'result': x, 'result1': result1, 'table': table})
    elif str(x) == "modify":
        request.session["modify"] = True
        request.session["table_id"] = request.POST.get("id")
        request.session["table_id1"] = request.POST.get("id1")
        return redirect("Picture")
    else:
        return redirect("loginpage")


def achievement_modify(request):
    x = request.POST.get("action")
    if not x:
        return redirect("loginpage")
    elif str(x) == "delete":
        id = request.POST.get("id")
        query = 'DELETE FROM ACHIEVEMENTS WHERE ID = %d'%(int(id))
        try:
            cur.execute(query)
            transaction.commit()
        except:
            pass
        query = "SELECT * FROM ACHIEVEMENTS WHERE TYPE = 1"
        cur.execute(query)
        result = cur.fetchall()
        x = []
        for res in result:
            tmp = []
            tmp.append(res[0])
            tmp.append(base64.encodestring(res[1]))
            x.append(tmp)
        query1 = 'select column_name from information_schema.columns where table_name="ACHIEVEMENTS" '
        cur.execute(query1)
        result1 = cur.fetchall()
        table = "ACHIEVEMENTS"
        return render(request, 'achievement_modify.html', {'result': x, 'result1': result1, 'table': table})
    elif str(x) == "modify":
        request.session["modify"] = True
        request.session["table_id"] = request.POST.get("id")
        request.session["table_id1"] = request.POST.get("id1")
        return redirect("ACHIEVEMENTS")
    else:
        return redirect("loginpage")


def event_modify(request):
    x = request.POST.get("action")
    if not x:
        return redirect("loginpage")
    elif str(x) == "delete":
        id = request.POST.get("id")
        query = 'DELETE FROM ACHIEVEMENTS WHERE ID = %d'%(int(id))
        try:
            cur.execute(query)
            transaction.commit()
        except:
            pass
        query = "SELECT * FROM ACHIEVEMENTS WHERE  TYPE = 2"
        cur.execute(query)
        result = cur.fetchall()
        x = []
        for res in result:
            tmp = []
            tmp.append(res[0])
            tmp.append(base64.encodestring(res[1]))
            x.append(tmp)
        query1 = 'select column_name from information_schema.columns where table_name="ACHIEVEMENTS" '
        cur.execute(query1)
        result1 = cur.fetchall()
        table = "ACHIEVEMENTS"
        return render(request, 'event_modify.html', {'result': x, 'result1': result1, 'table': table})
    elif str(x) == "modify":
        request.session["modify"] = True
        request.session["table_id"] = request.POST.get("id")
        request.session["table_id1"] = request.POST.get("id1")
        return redirect("EVENTS")
    else:
        return redirect("loginpage")
