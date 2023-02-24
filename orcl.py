import cx_Oracle
    
class RDB_client:
    def __init__(self, user_name, password, host_name, port_num, sid):
        self.user_name = user_name
        self.password = password
        self.host_name = host_name
        self.port_num = port_num
        self.service_name = sid

        self.host_info = f'{self.host_name}:{self.port_num}/{self.service_name}' 
        self.connection = cx_Oracle.connect(self.user_name, self.password, self.host_info) 
        self.cursor = self.connection.cursor()


    def execute_sql(self, sql: str):
        self.cursor.execute(sql)

    def get_field_names(self):
        return [col[0] for col in self.cursor.description]

    def get_datas(self):
        return self.cursor.fetchall()
