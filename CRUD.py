import mysql.connector

Conexao = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    database= "atendimentos",
)

if Conexao.is_connected():
    print("Conexão bem sucedida! \n")

Cursor = Conexao.cursor()



def Create (Nome, Valor):
    Cursor.execute(
        f"""
    insert into exames (Nome, Valor_Particular)
    values
    ('{Nome}', {Valor})
    """)

    Conexao.commit()
    print(f"Exame de {Nome} foi adicionado com sucesso!")


def Read(Nome):
        Cursor.execute(
        f"""
        Select *from exames
        where nome= "{Nome}"
        """)
        Dados = Cursor.fetchall()
        Nome = Dados[0][1]
        Valor = Dados[0][2]
        Situacao = Dados[0][3] 
        if Situacao == 1:
            Situacao = "Ativado"

        else:
            Situacao = "Desativado"

        print (f"Exame: {Nome} \nValor: R${Valor} \nSituação: {Situacao}")


def Update_Name (Nome, NovoNome):
        Cursor.execute(
            f"""
        Update exames
        set nome='{NovoNome}'
        where nome='{Nome}'
        limit 1
            """)
        Conexao.commit()
        print(f"Exame de {Nome} foi alterado para {NovoNome}.")   



def Verifica_Existencia (Nome):
        Cursor.execute(
        f"""
        SELECT EXISTS(SELECT 1 FROM exames 
        WHERE nome = '{Nome}')
        """
        )
        Valor = Cursor.fetchall()
        if Valor[0][0] == 0:
              Existencia = False

        else:
              Existencia= True

        return Existencia



def Update_Valor (Nome, NovoValor):
        Cursor.execute(
            f"""
        Update exames
        set Valor_Particular='{NovoValor}'
        where nome='{Nome}'
        limit 1
            """)
        Conexao.commit()
        print(f"O valor do exame de {Nome} foi alterado para R${NovoValor}.")       
         


def Delete (Nome):
        Cursor.execute(
        f"""
        Delete from exames
        where nome='{Nome}'
        limit 1
            """)
        Conexao.commit()
        print(f"Exame de {Nome} foi deletado!")



def Status(Nome,SituacaoDesejada):
    if SituacaoDesejada == False:
            Cursor.execute(
            f"""
            Update exames
            set Ativo=0
            where nome="{Nome}"
            limit 1
            """
            )
            Conexao.commit()
            print (f"O status do exame de {Nome} foi alterado para desativado.")


    else:
            Cursor.execute(
            f"""
            Update exames
            set Ativo=1
            where nome="{Nome}"
            limit 1
            """
            )
            Conexao.commit()
            print (f"O status do exame de {Nome} foi alterado para ativado.") 
         

def VerificaStatus(Nome):
    Cursor.execute(
    f"""
    Select Ativo from exames
    where nome= "{Nome}"
    """
    )   
    Valor = Cursor.fetchall()

    if Valor[0][0] ==1:
        Status = "ativado"
    else:
        Status = "desativado"
    
    return Status


print("*"*50)
Menu= int(input("[1] Adicionar novo exame \n[2] Ver exame \n[3] Editar exame \n[4] Excluir exame \n\nSelecione a opção desejada: "))


match Menu:
    case 1:
        Nome= str(input("Digite o nome do exame: "))

        if len(Nome) ==0:
            print ("O nome deve ter mais de um caractere.")

        else:
            Valor= float (input("Digite o valor do exame: "))
            if Valor < 0:
                print ("O valor não pode ser negativo.")        

            else:
                Create(Nome, Valor)

    case 2:
        Nome = str(input("Digite o nome do exame: "))

        if Verifica_Existencia(Nome) == False:
            print (f"O exame '{Nome}' não existe.")
        
        else:
            Read(Nome)


    case 3:
        Nome = str(input("Digite o nome do exame que deseja editar: "))

        if Verifica_Existencia(Nome) == False:
            print (f"O exame '{Nome}' não existe.")
        
        else:
            Ask_Alteracao = int(input("O que você deseja alterar? \n[1] Nome \n[2] Valor \n[3] Status \n: "))

            if Ask_Alteracao == 1:
                NovoNome = str(input(f"Digite o novo nome para {Nome}: "))

                if len(NovoNome) ==0:
                    print ("O nome deve ter mais de um caractere.")
                
                else:
                    Update_Name(Nome, NovoNome)


            elif Ask_Alteracao == 2:
                NovoValor = float(input(f"Digite um novo valor para {Nome}: "))

                if NovoValor < 0:
                    print ("O valor não pode ser negativo.")        

                else:
                    Update_Valor(Nome,NovoValor)


            elif Ask_Alteracao == 3:
                Status_Exame= VerificaStatus(Nome)

                if Status_Exame== "ativado":
                    Ask_Status = str(input(f"O exame {Nome} esta ativado. Você deseja desativar? [S/N] ")).upper()
                    if Ask_Status == "S":
                        Ask_Status=False
                        Status(Nome, Ask_Status)
                
                elif Status_Exame== "desativado":
                    Ask_Status = str(input(f"O exame {Nome} esta desativado. Você deseja ativar? [S/N] ")).upper()
                    if Ask_Status == "S":
                        Ask_Status=True
                        Status(Nome, Ask_Status)
    case 4:
        Nome= str(input("Digite o nome do exame que deseja deletar: "))

        if Verifica_Existencia(Nome) == False:
            print (f"O exame '{Nome}' não existe.")
        
        else:
            Confirmacao = str(input(f"Tem certeza que deseja excluir o exame {Nome}? [S/N] ")).upper()
            if Confirmacao == "S":
                Delete(Nome)


    case _:
        print ("Essa opção não existe.")


Cursor.close()
Conexao.close()