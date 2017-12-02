class IOMan():
    def __init__(self):
        self.scanner = -1
        self.impressora_1 = -1
        self.impressora_2 = -1
        self.modem = -1
        self.sata_1 = -1
        self.sata_2 = -1

    def proc_alloc(self, process):
        imp_1_temp = self.impressora_1
        imp_2_temp = self.impressora_2
        scanner_temp = self.scanner
        modem_temp = self.modem
        sata_1_temp = self.sata_1
        sata_2_temp = self.sata_2

        if process.cod_impressora == 1:
            imp_1_temp = process.pid
            if self.impressora_1 != -1 and self.impressora_1 != process.pid:
                raise Exception("Processo", process.pid, "bloqueado: Impressora 1 ocupada.")
        if process.cod_impressora == 2:
            imp_2_temp = process.pid
            if self.impressora_2 != -1 and self.impressora_2 != process.pid:
                raise Exception("Processo", process.pid, "bloqueado: Impressora 2 ocupada.")
        if process.req_scanner == 1:
            scanner_temp = process.pid
            if self.scanner != -1 and self.scanner != process.pid:
                raise Exception("Processo", process.pid, "bloqueado: Scanner ocupado.")
        if process.req_modem == 1:
            modem_temp = process.pid
            if self.modem != -1 and self.modem != process.pid:
                raise Exception("Processo", process.pid, "bloqueado: Modem ocupado.")
        if process.num_cod_disco == 1:
            sata_1_temp = process.pid
            if self.sata_1 != -1 and self.sata_1 != process.pid:
                raise Exception("Processo", process.pid, "bloqueado: Sata 1 ocupada.")
        if process.num_cod_disco == 2:
            sata_2_temp = process.pid
            if self.sata_2 != -1 and self.sata_2 != process.pid:
                raise Exception("Processo", process.pid, "bloqueado: Sata 2 ocupada.")

        self.scanner = scanner_temp
        self.impressora_1 = imp_1_temp
        self.impressora_2 = imp_2_temp
        self.modem = modem_temp
        self.sata_1 = sata_1_temp
        self.sata_2 = sata_2_temp

    def proc_dealloc(self, process):
        if process.cod_impressora == 1:
            self.impressora_1 = -1
        if process.cod_impressora == 2:
            self.impressora_2 = -1
        if process.req_scanner == 1:
            self.scanner = -1
        if process.req_modem == 1:
            self.modem = -1
        if process.num_cod_disco == 1:
            self.sata_1 = -1
        if process.num_cod_disco == 2:
            self.sata_2 = -1