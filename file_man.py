class File():
    def __init__(self, name, starting_block, size, owner=-1):
        self.name = name
        self.starting_block = starting_block
        self.size = size
        self.owner = owner


class FileMan():
    """
        Representa o disco, recebe o tamanho e uma lista com os
        arquivos que ja comecam no hd.
        Todas as operacoes no disco devem passar por essa classe
    """
    def __init__(self, size, starting_files):
        self.size = size
        self.disk = [0 for i in range(self.size)]  # Comeca o disco com 0s
        # Guarda as informacoes do arquivo file_name -> File Object
        self.files_info = {}

        # Coloca os arquivos iniciais no disco
        for file in starting_files:
            # file[0] = nome, file[1] = inicio, file[2] = tamanho
            nome = file[0]
            starting = int(file[1])
            file_size = int(file[2])
            new_file = File(nome, starting, file_size)
            for i in range(starting, starting + file_size):
                self.disk[i] = nome
            self.files_info[nome] = new_file

    def delete_file(self, file_name, PID, force=False):
        """
            Deleta um arquivo do disco checando antes se o arquivo
            tem permissao. force vai ser true se for um processo
            do sistema (prioridade 0).
        """
        if file_name not in self.files_info:
            raise Exception("Arquivo " + file_name + " nao existe.\n")
        if self.files_info[file_name].owner == PID or \
           self.files_info[file_name].owner == -1 or force:
            # Apagando
            self.disk = [f if f != file_name else 0 for f in self.disk]
        else:
            raise Exception("Processo " + str(PID) +
                            " nao tem permissao para apagar " + file_name + "\n")

    def create_file(self, file_name, size, PID):
        """
            Procura espaco para o arquivo usando first fit
        """
        for i in range(self.size):
            if self.disk[i] == 0:  # Checa se tem espaco vazio
                espaco_vazio = 0
                while espaco_vazio + i < self.size - 1 and \
                        self.disk[espaco_vazio + i] == 0 and \
                        espaco_vazio < size:
                    espaco_vazio += 1
                if espaco_vazio == size:  # Se tiver espaco
                    self.files_info[file_name] = File(file_name, i, size, PID)
                    for j in range(i, i+size):
                        self.disk[j] = file_name
                    return range(i, i+size)
                else:
                    i += espaco_vazio  # Se n tiver espaco adianta o i
        else:
            raise Exception("O processo " + str(PID) + " não pode criar o arquivo "
                            + file_name + " (falta de espaço).\n")

    def print_disk(self):
        print("|" + "|".join(str(x) for x in self.disk) + "|")
