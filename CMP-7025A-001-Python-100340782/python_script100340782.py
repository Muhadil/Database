
import psycopg2
#import pandas as pd
#from re import match
#from typing import Match


def getConn():
    # function to retrieve the password, construct
    # the connection string, make a connection and return it.

    connStr = "host='localhost' \
               dbname= 'final_schema_db' user='postgres' password = '12345'"
    #connStr=("dbname='studentdb' user='dbuser' password= 'dbPassword' " )
    conn = psycopg2.connect(connStr)
    return conn



def writeOutput(out_put_file, output):
    with open(out_put_file, "a") as myfile:
        myfile.write(output)
        
#FOR THIS PYTHON SCRIP TO EXECUTE I NEED TO SPEICIFY THE INPUT AND OUTPUT FILE EACH TIME IN THE BELOW 2 VARIABLES
output_file = 'output3.txt'
input_file = 'testpart3.txt'

f = open(input_file, "r")
for x in f:
    x = x.rstrip('\n')
    split_value = x.split("      ")
    task = x.split("      ")[0]
    task_values = None
    if len(x.split("      ")) > 1:
        task_values = x.split("      ")[1]

    #cur.execute('SET SEARCH_PATH TO db_coursecork_2;')
####################################################################
    if task == 'A':
        conn = getConn()
        cur = conn.cursor()
        values = task_values.split('/')
        query = """INSERT INTO student (sno, sname, semail) VALUES (%s, %s, %s) """
        record = (int(values[0]), values[1], values[2])

        try:
            cur.execute(query, record)
            
            print(str(cur.rowcount) + 'Rows Effected\n')
            writeOutput(output_file, str(cur.rowcount) + ' ROWS INSERTED\n\n')
            conn.commit()

        except Exception as e:
            print(e)
            writeOutput(output_file, str(e) + '\n')
        conn.close()
################################################################
    elif task == 'B':
        conn = getConn()
        cur = conn.cursor()
        values = task_values.split('/')

        query = """INSERT INTO exam (excode, extitle, exlocation, exdate, extime) VALUES (%s, %s, %s, %s, %s) """
        record = (values[0], values[1], values[2], values[3], values[4])
        try:
            cur.execute(query, record)
            writeOutput(output_file, str(cur.rowcount) + ' ROWS INSERTED\n\n')
            conn.commit()

        except Exception as e:
            writeOutput(output_file, str(e) + '\n')
        conn.close()
##########################################################################
    elif task == 'C':
        conn = getConn()
        cur = conn.cursor()
        values = task_values.split('/')
        query = 'DELETE FROM STUDENT WHERE sno=' + values[0]
        record = ()
        try:
            cur.execute(query)
            writeOutput(output_file, str(cur.rowcount) + ' ROWS HAS BEEN DELETED\n\n')
            conn.commit()
        except Exception as e:
            writeOutput(output_file, str(e) + '\n')
        conn.close()
########################################################################
    elif task == 'D':
        conn = getConn()
        cur = conn.cursor()
        values = task_values.split('/')
        query = "DELETE FROM EXAM WHERE excode='" + values[0] + "'"
        record = ()
        try:
            cur.execute(query)
            writeOutput(output_file, str(cur.rowcount) + ' ROWS HAS BEEN DELETED\n\n')
            conn.commit()

        except Exception as e:
            writeOutput(output_file, str(e) + '\n')
        conn.close()
####################################################################            
    elif task == 'E':
        conn = getConn()
        cur = conn.cursor()
        values = task_values.split('/')

        query = """INSERT INTO entry (eno, excode, sno) VALUES ((SELECT COALESCE(MAX(eno),0) FROM entry) + 1, %s, %s) """
        record = (values[0], values[1])
        try:
            cur.execute(query, record)
            writeOutput(output_file, str(cur.rowcount) + ' ROWS INSERTED\n\n')
            conn.commit()
        except Exception as e:
            writeOutput(output_file, str(e) + '\n')
        conn.close()
##############################################################
    elif task == 'F':
        conn = getConn()
        cur = conn.cursor()
        values = task_values.split('/')

        query = "UPDATE entry SET egrade =" + \
            str(values[1]) + " where eno=" + str(values[0])
        record = ()
        try:
            cur.execute(query)
            writeOutput(output_file, str(cur.rowcount) + ' ROWS HAS BEEN UPDATED\n\n')
            conn.commit()
        except Exception as e:
            writeOutput(output_file, str(e) + '\n')
        conn.close()
##############################################################
    elif task == 'P':
        conn = getConn()
        cur = conn.cursor()
        values = task_values.split('/')
#SELECT s.sno,s.sname,ex.exlocation,ex.excode,ex.extitle,ex.exdate,ex.extime FROM student as s JOIN entry as ent ON
#s.sno=ent.sno JOIN exam as ex ON ex.excode=ent.excode WHERE s.sno=452 
        query = "select s.sname, ex.exlocation, ex.excode, ex.extitle ,ex.exdate, ex.extime FROM student as s JOIN entry as ent ON s.sno=ent.sno JOIN exam as ex ON ex.excode=ent.excode WHERE s.sno=" + \
            values[0]
        record = ()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            writeOutput(output_file, str(rows))
            writeOutput(output_file, ' QUERY EXECUTED SUCCESSFULY\n\n')
        except Exception as e:
            writeOutput(output_file, str(e) + '\n')
        conn.close()
###############################################################
    elif task == 'Q':
        conn = getConn()
        cur = conn.cursor()
        values = task_values.split('/')

        query = "SELECT ex.excode,s.sname, CASE when ent.egrade<50 then 'FAIL' when ent.egrade>=50 and ent.egrade<70 then 'PASS' when ent.egrade>=70 then 'DISTINCTION' when ent.egrade is null then 'NOT TAKEN' END AS results FROM entry as ent, student as s, exam as ex where s.sno = ent.sno and ent.excode = ex.excode order by ex.excode, s.sname"
        record = ()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            writeOutput(output_file, str(rows))
            writeOutput(output_file, '\n')
        except Exception as e:
            writeOutput(output_file, str(e) + ' \n')
        conn.close() 
###################################################################################################
    elif task == 'R':
        conn = getConn()
        cur = conn.cursor()
        values = task_values.split('/')

        query = "SELECT ex.excode,s.sname, CASE when ent.egrade<50 then 'FAIL' when ent.egrade>=50 and ent.egrade<70 then 'PASS' when ent.egrade>=70 then 'DISTINCTION' when ent.egrade is null then 'NOT TAKEN' END AS results FROM entry as ent, student as s, exam as ex where s.sno = ent.sno and ex.excode = '"+values[0]+"' and ent.excode = ex.excode order by ex.excode, s.sname"
        record = ()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            writeOutput(output_file, str(rows))
            writeOutput(output_file, ' \n')
        except Exception as e:
            writeOutput(output_file, str(e) + '\n')
        conn.close()
######################################################################################################
    elif task == 'S':
        conn = getConn()
        cur = conn.cursor()
        values = task_values.split('/')

        query = "SELECT s.sno,s.sname,ex.excode,ex.extitle,ent.egrade FROM student as s JOIN entry as ent ON\
                s.sno=ent.sno JOIN exam as ex ON ex.excode=ent.excode WHERE ent.egrade is not null and s.sno= " + values[0] +"order by ex.excode"
        record = ()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            writeOutput(output_file, str(rows))
            writeOutput(output_file, ' \n')

        except Exception as e:
            writeOutput(output_file, str(e) + '\n')
        conn.close()
###################################################################################################3
    elif task == 'T':
        conn = getConn()
        cur = conn.cursor()
        values = task_values.split('/')

        query = "select sname , membership_status(sno) from student where sno = " + \
            values[0]
        record = ()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            writeOutput(output_file, str(rows)+'\n')
            writeOutput(output_file, '\n\n')
        except Exception as e:
            writeOutput(output_file, str(e) + '\n')
        conn.close()
#####################################################################################
    elif task == 'V':
        conn = getConn()
        cur = conn.cursor()
        values = task_values.split('/')

        query = "SELECT * FROM cancel where sno=" + values[0]
        record = ()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            writeOutput(output_file, str(rows))
            writeOutput(output_file, '\n')
        except Exception as e:
            writeOutput(output_file, str(e) + '\n')
        conn.close()
#########################################################################################

