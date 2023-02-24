import cx_Oracle
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()


@app.get("/")
def test(): 
    return "Tomato"

@app.get("/{table}")
def read_orcl(table: str): 
    sql = f'SELECT * FROM {table}'
    connection = cx_Oracle.connect("test/test@127.0.0.1:1521/orcl")
    cursor = connection.cursor()
    try:
        cursor.execute(sql)
        emp = cursor.fetchall()

    except cx_Oracle.Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
    if emp is None:
        raise HTTPException(status_code=404, detail="employee not found")
    return {"data": emp}



@app.get("/read/")
def read_node(id: int):
    connection = cx_Oracle.connect("test/test@127.0.0.1:1521/orcl")
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM emp WHERE ID = :id", {"id": id})
        emp = cursor.fetchall()
    except cx_Oracle.Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
    if emp is None:
        raise HTTPException(status_code=404, detail="employee not found")
    return {"employee": emp}


@app.post("/insert/")
async def insert_data(id:str,name:str):
    config=[]
    config.append(id)
    config.append(name)
    connection = cx_Oracle.connect("test/test@127.0.0.1:1521/orcl")
    cursor = connection.cursor()
    
    insert_query = "INSERT INTO emp (id, name) VALUES (:1, :2)"
    
    cursor.execute(insert_query, (config[0], config[1]))
    
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Data inserted successfully"}

@app.post("/sp/")
async def sp_data(times:int,label:str):
    config1=[]
    config1.append(times)
    config1.append(label)
    connection = cx_Oracle.connect("test/test@127.0.0.1:1521/orcl")
    cursor = connection.cursor()
    
    #procedure = f'EXEC fast_test123({times},{label})'
        #cursor.execute("begin procedure(:1,:2); end;", (config1[0], config1[1]))
    cursor.callproc("fast_test",[times,label])

   # connection.commit()
    #cursor.close()
    connection.close()
    return {"message": "Data inserted successfully"}


@app.delete("/delete")
def delete_node(id: str):
    connection = cx_Oracle.connect("test/test@127.0.0.1:1521/orcl")
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM emp WHERE id = :id",
                       {"id": id})
        connection.commit()
        return {"DATA SUCCESSFULLY DELETED"}
    except cx_Oracle.Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()

@app.put("/update/")
def update_node(name:str,id:int):
    config2=[]
    config2.append(name)
    config2.append(id)
    connection = cx_Oracle.connect("test/test@127.0.0.1:1521/orcl")
    cursor = connection.cursor()
    update_query= "UPDATE emp SET name= :1 WHERE id = :2"
    try:
       cursor.execute(update_query,(config2[0], config2[1]))
       connection.commit()
       return {"DATA SUCCESSFULLY UPDATED"}
    except cx_Oracle.Error as e:
       raise HTTPException(status_code=400, detail=str(e))
    finally:
       cursor.close()  