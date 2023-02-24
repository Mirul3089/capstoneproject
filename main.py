from typing import Union 
from fastapi import FastAPI
from orcl import RDB_client
from pydantic import BaseModel
from anyio import sleep, create_task_group, run


app = FastAPI()
db = RDB_client('test', 'test', 'localhost', 1521, 'orcl')

hk=[]
class Emp(BaseModel):
    table = "emp"
    id: int
    name: str

@app.get("/{table}")#endpoints
async def read_orcl(table: str): 
    sql = f'SELECT * FROM {table}'

    db.execute_sql(sql)
    await sleep(5)
    fields = db.get_field_names()
    datas = db.get_datas()

    if not datas:
        return 'no data'
    items = [{field:value for field, value in zip(fields, data)} for data in datas]
    return items

@app.post("/insert/")
async def insert_node(id:int,name:str):
    #tables=table
    config = []
    config.append(id)
    config.append(name)
    #return {tables,ids,names}
    sql= "INSERT INTO emp (id, name) VALUES (:1, 2)",
    db.execute(sql,config[0],config[1]),
    #await(2)
    #db.commit()
    return {"Data successfully inserted"}
   
#@app.delete("/emp/{id}")
#def del_orcl(table: str,id: int): 
#    sql1 =  f'DELETE * FROM emp WHERE id= {id} '
#
#    db.execute_sql(sql1)
#    return print('Data deleted successfully');
#    #fields = db.get_field_names()
#    #datas = db.get_datas()
