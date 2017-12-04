import sys
import process_man as pm
import memory_man as mm
import file_man as fm
import queue_man as qm
import io_man as im

memory = None
file_man = None
queue_man = None
# Dicionario para guardar PID -> Process (facilita busca)
proc_dict = {}
# Lista para guardar processos pela ordem de chegada
proc_list = []
io_man = im.IOMan()


def usage():
    print("Usage: python dispatcher.py " +
          "<arquivo de processos> <arquivo de arquivos>")


def start_queue_man():
    global queue_man

    queue_man = qm.QueueMan()


def start_memory():
    global memory

    memory = mm.Memory()


def start_process(process_info):
    """
    Cria os processos a partir das info no arquivo process.txt
    """
    global memory
    global proc_dict
    global proc_list

    print("Process:")
    # Lista com informacoes de cada processo
    process_info_order = [proc.split(',') for proc in process_info]
    process_info_order.sort(key=lambda p: int(p[0]))
    proc_list_info = [pm.Process(proc) for proc in process_info_order]
    for proc in proc_list_info:
        try:
            #is_system_proc = proc.prioridade == 0  # se eh processo do sistema
            #memory.allocate(proc.blocos_mem, proc.pid, system=is_system_proc)
            #proc.offset = memory.get_proc_offset(proc.pid)
            #current_proc.print_info()
            #print()
            proc_dict[proc.pid] = proc
            proc_list.append(proc)
        except Exception as e:
            print(e)
    proc_list.sort(key=lambda p: p.tempo_de_init, reverse=True)


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
        process = int(op_info[0])
        operation = int(op_info[1])
        file_name = op_info[2]
        try:
            print("Operação " + str(i + 1) + " => ", end='')
            if process not in proc_dict:
                raise Exception("Não existe o processo.\n")
            if operation == 0:  # Criar novo
                block_size = int(op_info[3])
                blocks = file_man.create_file(file_name, block_size, process)
                print("Sucesso")
                print("O processo " + str(process) + " criou o arquivo " + file_name, end='')
                print(" (blocos " + ', '.join([str(num) for num in blocks]) + ").\n")
            elif operation == 1:
                proc_priority = proc_dict[process].prioridade
                file_man.delete_file(file_name, process, force=(proc_priority == 0))
                print("Sucesso")
                print("O processo " + str(process) + " deletou o arquivo " + file_name + ".\n")
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
    global queue_man

    start_memory()
    start_process(proccess_info)
    start_queue_man()

    # Rodar processos
    time = 0
    proc_tempo_real = False
    current_proc = None
    while len(proc_list) > 0 or queue_man.size_of_all_queues() != 0 or current_proc is not None:
        #queue_man.age()
        # Coloca os processos que chegaram agora na fila
        while len(proc_list) > 0 and proc_list[-1].tempo_de_init == time:
            queue_man.put_in_queue(proc_list.pop())
        # Pegar um processo da fila
        if current_proc is None and queue_man.size_of_all_queues() != 0:
            current_proc = queue_man.get_from_queue(io_man)
            if current_proc.instruction_counter == 0:
                #  T
                is_system_proc = current_proc.prioridade == 0  # se eh processo do sistema
                memory.allocate(current_proc.blocos_mem, current_proc.pid, system=is_system_proc)
                current_proc.offset = memory.get_proc_offset(current_proc.pid)
                current_proc.print_info()
                print()
                #  T
                print("\nprocess", current_proc.pid, "=>")
                print("P" + str(current_proc.pid) + " STARTED")
        # Roda uma instrucao do processo
        if current_proc is not None:
            print("P" + str(current_proc.pid) + " instruction",
                  current_proc.instruction_counter + 1, "at time", time+1)
            current_proc.instruction_counter += 1
            # Se o processo acabou
            if current_proc.instruction_counter == current_proc.tempo_proc:
                print("P" + str(current_proc.pid), " return SIGINT\n")
                io_man.proc_dealloc(current_proc)
                current_proc = None
            # Troca de contexto
            elif current_proc.prioridade != 0:
                queue_man.put_in_queue(current_proc)
                current_proc = None
        time += 1
        #queue_man.print_ages()

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
