import sys
import proccess_man as pm
import memory_man as mm
import file_man as fm

memory = None
file_man = None
# Dicionario para guardar PID -> Process (facilita busca)
proc_dict = {}
# Lista para guardar processos de fato criados (ordem)
proc_list = []


def usage():
    print("Usage: python dispatcher.py " +
          "<arquivo de processos> <arquivo de arquivos>")


def start_memory():
    global memory

    memory = mm.Memory()


def start_proccess(proccess_info):
    """
    Cria os processos a partir das info no arquivo proccess.txt
    """
    global memory
    global proc_dict
    global proc_list

    print("Proccess:")
    # Lista com informacoes de cada processo
    proc_list_info = [pm.Proccess(proc.split(',')) for proc in proccess_info]
    for proc in proc_list_info:
        try:
            is_system_proc = proc.prioridade == 0  # se eh processo do sistema
            memory.allocate(proc.blocos_mem, proc.pid, system=is_system_proc)
            proc.offset = memory.get_proc_offset(proc.pid)
            proc_dict[proc.pid] = proc
            proc_list.append(proc)
            proc.print_info()
            print()
        except Exception as e:
            print(e)


def start_file_man(files_info):
    """
    Inicia o sistema de arquivos com os arquivos de files.txt
    """
    global file_man

    print("Files")
    index_start_op = int(files_info[1])
    starting_files = [f.split(',') for f in files_info[2:index_start_op + 2]]
    file_man = fm.FileMan(int(files_info[0]), starting_files)
    # Run operations
    operations = [f for f in files_info[index_start_op+2:]]
    run_operations(operations)


def run_operations(operations):
    """
    Roda as operacoes de processos do arquivo files.txt
    """
    for i, op in enumerate(operations):
        op_info = [info.strip() for info in op.split(',')]
        proccess = int(op_info[0])
        operation = int(op_info[1])
        file_name = op_info[2]
        try:
            print("Operação " + str(i + 1) + " => ", end='')
            if proccess not in proc_dict:
                raise Exception("Não existe o processo.\n")
            if operation == 0:  # Criar novo
                block_size = int(op_info[3])
                blocks = file_man.create_file(file_name, block_size, proccess)
                print("Sucesso")
                print("O processo " + str(i) + " criou o arquivo " + file_name, end='')
                print(" (blocos " + ', '.join([str(num) for num in blocks]) + ").\n")
            elif operation == 1:
                file_man.delete_file(file_name, proccess)
                print("Sucesso")
                print("O processo " + str(i) + " deletou o arquivo " + file_name + ".\n")
        except Exception as e:
            print("Falha")
            print(e)


# TEMP
# Funcao que roda o SO
def run(proccess_info, files_info):
    global memory
    global proc_dict
    global proc_list
    global file_man

    start_memory()
    start_proccess(proccess_info)
    # Print final disk state
    start_file_man(files_info)
    file_man.print_disk()


def main():
    if(len(sys.argv) != 3):  # Deve receber dois argumentos
        usage()
    else:
        proccess_file_path = sys.argv[1]
        files_file_path = sys.argv[2]

        with open(proccess_file_path, 'r') as f:
            proccess_info = f.readlines()

        with open(files_file_path, 'r') as f:
            files_info = f.readlines()

        run(proccess_info, files_info)


if __name__ == "__main__":
    main()
