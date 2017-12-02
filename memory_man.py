class Memory():
    """
        Classe que representa a memoria. Cada proccessso
        fica no dict proc_offsets que guarda chave valor
        da forma PID -> offset
    """
    def __init__(self):
        self.max_size = 1024
        self.system_size = 64
        self.proc_offsets = {}  # PID -> Offset
        self.pointer_user_new = 64  # Aponta para o inicio da mem de usuario livre
        self.pointer_sys_new = 0  # Aponta para o inicio da memoria livre do sistema

    def allocate(self, block_size, PID, system=False):
        """
            Aloca um bloco de memoria de tamanho block_size para um
            processo, se for um processo do sistema ele tenta usar a area
            de memoria do sistema. Se nao for do sistema ou nao tiver espaco
            ele tenta alocar na memoria de usuario
        """
        if system and self.system_size - (self.pointer_sys_new + block_size) >= 0:
            self.proc_offsets[PID] = self.pointer_sys_new
            self.pointer_sys_new += block_size
        else:
            if self.max_size - (self.pointer_user_new + block_size) < 0:
                raise Exception("Memoria incuficiente para alocar o processo: ", PID)
            else:
                self.proc_offsets[PID] = self.pointer_user_new
                self.pointer_user_new += block_size

    def get_proc_offset(self, PID):
        """
            Retorna o offset de um sistema a partir de seu PID
        """
        return self.proc_offsets.get(PID, -1)
