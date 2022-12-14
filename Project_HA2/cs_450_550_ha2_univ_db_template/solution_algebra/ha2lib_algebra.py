#Cheema, Fatima
#Solution_Algebra
#CS550
##############################################################
##############################################################

from ast import Not
import sys
sys.path.append('..')

import lib.rel_algebra_calculus.rel_algebra_calculus as ra

def ha2(univDB):
    tables = univDB["tables"]
    department = tables["department"]
    course = tables["course"]
    prereq = tables["prereq"]
    # class may be a reserved word - check
    class_ = tables["class"]
    faculty = tables["faculty"]
    student = tables["student"]
    enrollment = tables["enrollment"]
    transcript = tables["transcript"]

    # ---------------------------------------------------------------
    # Your condition functions or other helper functions (if needed)


    # ---------------------------------------------------------------
    # Your queries

    # query_a
    transcript_proj = ra.proj(transcript, ['dcode', 'cno', 'ssn'])
    cs530_transcript = ra.sel(transcript_proj,  lambda x: x["dcode"] == "CS" and x["cno"] == 530 )
    student_transcript = ra.join(cs530_transcript, student)
    student_info_req = ra.proj(student_transcript, ['ssn', 'name', 'major', 'status'])
    query_a = student_info_req





    # query_b
    transcript_proj = ra.proj(transcript, ['dcode', 'cno', 'ssn'])
    cs530_transcript = ra.sel(transcript_proj,  lambda x: x["dcode"] == "CS" and x["cno"] == 530 )
    student_transcript = ra.join(cs530_transcript, student)
    student_John = ra.sel(student_transcript, lambda x: x["name"] == "John")
    student_info_req = ra.proj(student_John, ['ssn', 'name', 'major', 'status'])
    query_b = student_info_req



    # query_c
    class_enrollment = ra.join(enrollment,class_)
    class_preq = ra.join(class_enrollment, prereq)
    prereq_info = ra.proj(class_preq, ["ssn", "pcode", "pno"])
    Prereq_Rename = ra.ren(prereq_info, {"pcode": "dcode", "pno": "cno"} )
    # student prereqs over the schema (ssn, dcode, cno)

    cond_a_or_b = lambda t: (t["grade"] == "A" or t["grade"] == "B")
    A_B_grade = ra.sel(transcript, cond_a_or_b)
    Student_NTranscript = ra.proj(A_B_grade, ["ssn","dcode", "cno"])

    if_NOT = ra.proj( ra.diff(Prereq_Rename,Student_NTranscript),  ["ssn"] )
    if_YES = ra.diff( ra.proj(student, ["ssn"]),  if_NOT)
    query_c = ra.join(student, if_YES)
   
    # query_d
    query_d = ra.join(student, if_NOT)
   
    # query_e
    student_John = ra.sel(student, lambda x: x["name"] == "John") 
    query_e = ra.join(student_John, if_NOT)


    # query_f
    All_Courses = ra.proj(course, ["dcode", "cno"])
    Preq_of_All_Courses = ra.proj(prereq, ["dcode","cno"])
    Find_Diff = ra.diff(All_Courses, Preq_of_All_Courses)
    query_f = Find_Diff

    # query_g
    Find_Common = ra.join(All_Courses, Preq_of_All_Courses)
    query_g = Find_Common

    # query_h
    Find_Common_Class= ra.join(Find_Common, class_)
    Class_Info = ra.proj(Find_Common_Class, ["class","dcode","cno","instr"])
    query_h = Class_Info


    # query_i
    C_F_Grades = ra.sel(transcript, lambda t: (t["grade"] == "C" or t["grade"] == "F"))
    Student_with_C_F = ra.join(ra.proj(C_F_Grades, ["ssn"]), student)
    Find_A_B_Student = ra.diff(student,Student_with_C_F)  
    query_i = Find_A_B_Student


    # query_j
    Find_Prof_Brodsky = ra.proj(ra.sel(faculty, lambda x: x['name'] == 'Brodsky'), ["ssn"])
    Rename_Instr =  ra.ren(Find_Prof_Brodsky, {'ssn':'instr'})
    Classes_Taught = ra.join(ra.join(Rename_Instr,class_), enrollment)
    Student_Taught = ra.join(ra.proj(Classes_Taught, ["ssn"]),student)
    query_j = Student_Taught

    # query_k
    All_Classes_offered = ra.proj(class_, ['class'])
    Classes_with_Enrollment = ra.join(All_Classes_offered,enrollment)
    Student_enroll_in_allClasses = ra.div(Classes_with_Enrollment, All_Classes_offered, ['class'] )
    query_k = Student_enroll_in_allClasses


    #query_l
    All_Math_Classes = ra.proj(ra.sel(class_, lambda x: x['dcode'] == 'MTH'),['class'])
    CS_Major_Students = ra.proj(ra.sel(student, lambda x: x["major"] ==  "CS"),["ssn"])
    CS_Student_Enrollment = ra.join(CS_Major_Students, enrollment)
    CS_Student_Taking_AllMTH = ra.div(CS_Student_Enrollment, All_Math_Classes, ['class'] )
    query_l = CS_Student_Taking_AllMTH

    # ---------------------------------------------------------------
    # Some post-processing which you do not need to worry about
    # Do not change anything after this

    query_a = ra.distinct(query_a)
    query_b = ra.distinct(query_b)
    query_c = ra.distinct(query_c)
    query_d = ra.distinct(query_d)
    query_e = ra.distinct(query_e)
    query_f = ra.distinct(query_f)
    query_g = ra.distinct(query_g)
    query_h = ra.distinct(query_h)
    query_i = ra.distinct(query_i)
    query_j = ra.distinct(query_j)
    query_k = ra.distinct(query_k)
    query_l = ra.distinct(query_l)


    ra.sortTable(query_a,["ssn"])
    ra.sortTable(query_b,["ssn"])
    ra.sortTable(query_c, ['ssn'])
    ra.sortTable(query_d, ['ssn'])
    ra.sortTable(query_e, ['ssn'])
    ra.sortTable(query_f, ['dcode', 'cno'])
    ra.sortTable(query_g, ['dcode', 'cno'])
    ra.sortTable(query_h, ['class'])
    ra.sortTable(query_i, ['ssn'])
    ra.sortTable(query_j, ['ssn'])
    ra.sortTable(query_k, ['ssn'])
    ra.sortTable(query_l, ['ssn'])

    return({
        "query_a": query_a,
        "query_b": query_b,
        "query_c": query_c,
        "query_d": query_d,
        "query_e": query_e,
        "query_f": query_f,
        "query_g": query_g,
        "query_h": query_h,
        "query_i": query_i,
        "query_j": query_j,
        "query_k": query_k,
        "query_l": query_l
    })
