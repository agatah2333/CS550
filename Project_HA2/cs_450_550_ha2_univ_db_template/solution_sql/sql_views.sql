--CheemaFatima, Ha2_SQL

-- query_a
drop view query_a;
create view query_a as
select distinct s.ssn as ssn, s.name as name, s.major as major, s.status as status
from student s, transcript t
where s.ssn = t.ssn and t.dcode = 'CS' and t.cno = 530
order by s.ssn;

-- query_b
drop view query_b;
create view query_b as
select distinct s.ssn as ssn, s.name as name, s.major as major, s.status as status
from student s, transcript t
where s.ssn = t.ssn and s.name = 'John' and t.dcode = 'CS' and t.cno = 530
order by s.ssn;

-- query_c
drop view query_c;
create view query_c as
select distinct s.ssn as ssn, s.name as name, s.major as major, s.status as status
from student s
where NOT EXISTS (
-- all prereqs
  ( select p.pcode as dcode, p.pno as cno
    from enrollment e, class c, prereq p
    where s.ssn = e.ssn and e.class = c.class and c.dcode = p.dcode and c.cno = p.cno
  )
  MINUS
-- all courses taken w/A or B
  ( select t.dcode, t.cno
    from transcript t
    where t.ssn = s.ssn and (t.grade = 'A' or t.grade = 'B')
  )
)
order by s.ssn;

-- query_d
drop view query_d;
create view query_d as
select distinct s.ssn as ssn, s.name as name, s.major as major, s.status as status
from student s
where EXISTS (
-- all prereqs
  ( select p.pcode as dcode, p.pno as cno
    from enrollment e, class c, prereq p
    where s.ssn = e.ssn and e.class = c.class and c.dcode = p.dcode and c.cno = p.cno
  )
  MINUS
-- all courses taken w/A or B
  ( select t.dcode, t.cno
    from transcript t
    where t.ssn = s.ssn and (t.grade = 'A' or t.grade = 'B')
  )
)
order by s.ssn;


-- query_e
drop view query_e;
create view query_e as
select distinct s.ssn as ssn, s.name as name, s.major as major, s.status as status
from student s, enrollment e, class c
where s.name = 'John' and s.ssn = e.ssn and  e.class = c.class and EXISTS (
-- all prereqs for this class
  ( select  p.pcode as dcode,  p.pno as cno
    from prereq p
    where c.dcode = p.dcode and c.cno = p.cno
  )
  MINUS
-- all courses taken w/A or B
  ( select t.dcode, t.cno
    from transcript t
    where t.ssn = s.ssn and (t.grade = 'A' or t.grade = 'B')
  )
)
order by s.ssn;








-- query_f
drop view query_f;
create view query_f as
select distinct c.dcode, c.cno
from course c
where NOT EXISTS (
  select p.pcode as dcode,  p.pno as cno
  from prereq p
  where p.dcode = c.dcode and p.cno = c.cno
)
order by c.dcode, c.cno;

-- query_g
drop view query_g;
create view query_g as
select distinct c.dcode, c.cno
from course c
where EXISTS (
  select p.pcode as dcode,  p.pno as cno
  from prereq p
  where p.dcode = c.dcode and p.cno = c.cno
)
order by c.dcode, c.cno;




-- query_h
drop view query_h;
create view query_h as
select c.class as class, c.dcode as dcode, c.cno as cno, c.instr as instr
from class c
where EXISTS (
  select p.pcode as dcode,  p.pno as cno
  from prereq p
  where p.dcode = c.dcode and p.cno = c.cno
)
order by c.class;




-- query_i
drop view query_i;
create view query_i as
select distinct s.ssn as ssn, s.name as name, s.major as major, s.status as status
from student s
where NOT EXISTS (

  select t.dcode, t.cno
    from transcript t
    where t.ssn = s.ssn and (t.grade = 'C' or t.grade = 'F')
  
)
order by s.ssn;




-- query_j
drop view query_j;
create view query_j as
select distinct s.ssn as ssn, s.name as name, s.major as major, s.status as status
from student s
where exists(
select f.name as name, c.instr as instr, e.ssn as ssn
from faculty f, class c, enrollment e
where f.name = 'Brodsky' and f.ssn = c.instr and c.class = e.class and e.ssn = s.ssn
)
order by s.ssn;


---query_k
-- Reference: Module06Slides-slide 22 and discussion board- subbed in data


drop view query_k;
create view query_k as
select distinct e.ssn
from enrollment e
where NOT EXISTS (
-- A: set of all  classes
    (
        select c.class 
        from class c
    )
    MINUS
-- B: set of all classes in which s.ssn is enrolled in 
    (
        select en2.class from enrollment en2
        where en2.ssn =  e.ssn   
    )
)
order by e.ssn;

  


-- query_l
-- Reference: Module06/07Slides-slide 06_22 and discussionboard- subbed in data


drop view query_l;
create view query_l as
select distinct e.ssn
from enrollment e, student s
where e.ssn = s.ssn and s.major = 'CS' and NOT EXISTS (
-- A: set of all math classes
    (
        select c.class 
        from class c
        where c.dcode = 'MTH'
    )
    MINUS
-- B: set of all classes in which s.ssn is enrolled in 
    (
        select en2.class from enrollment en2
        where en2.ssn =  s.ssn   
    )
)
order by e.ssn;
