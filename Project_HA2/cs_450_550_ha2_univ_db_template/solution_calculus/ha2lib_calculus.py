##Cheema, Fatima
#CS 550-DL1
#Assignment: HA2CALCULUS


import sys
from unittest import result
sys.path.append('..')

import lib.rel_algebra_calculus.rel_algebra_calculus as ra
# note: you can use ra.imply(a,b) which expresses a --> b (a implies b)

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
    # Your set creater functions or other helper functions (if needed)


    # ---------------------------------------------------------------
    # Your queries
    def studSatCourseAB(s,dcode,cno):
        # s took course (dcode,cno) and received A or B
        result = any([
                t["ssn"] == s["ssn"] and
                t["dcode"] == dcode and
                t["cno"] == cno and
                (t["grade"] == "A" or t["grade"] == "B")
                for t in transcript
        ])
        return result

    def studSatCourseCF(s,dcode,cno):
        # s took course (dcode,cno) and received C or F
        result = any([
                t["ssn"] == s["ssn"] and
                t["dcode"] == dcode and
                t["cno"] == cno and
                (t["grade"] == "C" or t["grade"] == "F")
                for t in transcript
        ])
        return result

    
    def studSatPrereqs(s, dcode, cno):
        # s sat'd all prereqs of (dcode,cno)
        # for every prereq (pcode,pno) of (dcode,cno), s sat'd it w/A or B
        result = all([
            #bool cond for a prereq
            studSatCourseAB(s,p["pcode"],p["pno"])
            for p in prereq
            if p["dcode"] == dcode and p["cno"] == cno
        ])
#        print("\n\ns :", s["ssn"], "dcode :", dcode, "cno :", cno, "result :", result)
        return result


    def preqtocourse( dcode, cno):
        result = any([
             p["pcode"] == dcode and p["cno"]== cno
            for p in prereq
            ])
        return result




    # query_a
    query_a = [
        s
        for s in student
        if any([
            (t["dcode"] == "CS" and t["cno"] == 530  and t["ssn"] == s["ssn"])
            for t in transcript
        ])
    ]


    # query_b
    query_b = [
        s
        for s in student
        if s["name"] == "John"
        if any([
            (t["dcode"] == "CS" and t["cno"] == 530  and t["ssn"] == s["ssn"])
            for t in transcript
        ])
    ]

    # query_c
    query_c = [
        s
        for s in student
        if not(any([
            e["ssn"] == s["ssn"] and
                e["class"] == c["class"] and
                not(studSatPrereqs(s, c["dcode"], c["cno"] ))     # s sat'd all  prereqs of class c  )
            for e in enrollment
            for c in class_
        ]))          # s is enrolled in a class
    ]



    # query_d
    query_d = [
        s
        for s in student
        if any([
            e["ssn"] == s["ssn"] and
                e["class"] == c["class"] and
               not ( studSatPrereqs(s, c["dcode"], c["cno"] ))     # s sat'd all  prereqs of class c  )
            for e in enrollment
            for c in class_
        ])          # s is enrolled in a class
    ]

    # query_e
    query_e = [
        s
        for s in student
        if s["name"] == "John"
        if any([
            e["ssn"] == s["ssn"] and
                e["class"] == c["class"] and
               not ( studSatPrereqs(s, c["dcode"], c["cno"] ))     # s sat'd all  prereqs of class c  )
            for e in enrollment
            for c in class_
        ])          # s is enrolled in a class
    ]

    # query_f
    query_f = [
        {"dcode":b["dcode"],"cno":b["cno"]}
        for b in course
        if not any([
            preqtocourse(b["dcode"], b["cno"])
        ])
    ]
    query_f.sort(key= lambda t: [t["dcode"],t["cno"]])


    # query_g
    query_g = [
        {"dcode":b["dcode"],"cno":b["cno"]}
        for b in course
        if any([
            preqtocourse(b["dcode"], b["cno"])
        ])
    ]
    query_g.sort(key= lambda t: [t["dcode"],t["cno"]])



    # query_h
    query_h = query_h = [
        c
        for c in class_
        if  any([
            c["dcode"] == p["dcode"] and c["cno"] == p["cno"] #p is a prereq
            for p in prereq
            #offered this semester and has prereqs
        ])
    ]
    '''
    def classKey(t):
        return [t["class"],t["dcode"],t["cno"]]
    query_h.sort(key= classKey )
    '''
    query_h.sort(key= lambda t: [t["class"],t["dcode"],t["cno"]])






    # query_i
    query_i = [
        s
        for s in student
        if not any([
            studSatCourseCF(s, t["dcode"] , t["cno"])
            for t in transcript
        ])
    ]

    # query_j
    query_j = [
        s
        for s in student
        if  any([
            s["ssn"]== e["ssn"] and
            e["class"] == c["class"] and
            c["instr"] == f["ssn"] and 
            f["name"] == "Brodsky"


            for e in enrollment
            for c in class_
            for f in faculty

        ])
    ]








    # query_k
    query_k = ra.distinct([
        { "ssn": e["ssn"]}
        for e in enrollment
        if all([
            any([
                ( e["ssn"] == e1["ssn"] and
                  e1["class"] == c["class"]
                )
               for e1 in enrollment
            ])
            for c in class_
        ])

    ])



    # query_l
    query_l = ra.distinct([
       { "ssn": s["ssn"]}
       for s in student
       if s["major"] == "CS"
       if any([
           e["ssn"] == s["ssn"]
           for e in enrollment
       ])
       if all([
           ra.imply(( c["dcode"] == "MTH"),
               any([
                   ( e1["ssn"] == s["ssn"] and
                     e1["class"] == c["class"]
                   )
                   for e1 in enrollment
               ]))
           for c in class_
       ])

  ])

    # ---------------------------------------------------------------
    # Some post-processing which you do not need to worry about
    # Do not change anything after this

    ra.sortTable(query_a,["ssn"])
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
        "query_l": query_l,

    })
