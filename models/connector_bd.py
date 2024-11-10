import mysql.connector


#Class para fazer a conexao com o Banco de dados
#Database = authentication
#User = #####
#Senha = #######
class Connector_BD:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Connector_BD, cls).__new__(cls)
            cls._instance.mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Rps4303.",
                database="authentication"
            )
            cls._instance.mycursor = cls._instance.mydb.cursor()
        return cls._instance

    def commit(self):
        self.mydb.commit()

    def close(self):
        self.mycursor.close()
        self.mydb.close()
