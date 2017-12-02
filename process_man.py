class Process():
    """
    Classe que representa o processo, construtor recebe uma lista
    com todas as informacoes.
    Para gerar a lista basta usar .split(',') em cada linha
    do input do process.txt.
    """
    PID = 0

    def __init__(self, lista_info):
        self.pid = Process.PID
        self.tempo_de_init = int(lista_info[0])
        self.prioridade = int(lista_info[1])
        self.tempo_proc = int(lista_info[2])
        self.blocos_mem = int(lista_info[3])
        self.cod_impressora = int(lista_info[4])
        self.req_scanner = int(lista_info[5])
        self.req_modem = int(lista_info[6])
        self.num_cod_disco = int(lista_info[7])
        self.offset = -1
        self.instruction_counter = 0
        self.age = 0
        Process.PID += 1

    def print_info(self):
        print("PID:", self.pid)
        print("offset:", self.offset)
        print("blocks:", self.blocos_mem)
        print("priority:", self.prioridade)
        print("time:", self.tempo_proc)
        print("printers:", self.cod_impressora)
        print("scanners:", self.req_scanner)
        print("modems:", self.req_modem)
        print("drives:", self.num_cod_disco)
