class Disco:
    def __init__(self, id):
        self.id = id
        self.memoria = []
        self.blocos_livres = []

class Arquivo:
    def __init__(self, nome, tamanho):
        self.nome = nome
        self.tamanho = tamanho
        self.blocos = []

class Diretorio:
    def __init__(self, nome, bloco):
        self.nome = nome
        self.arquivos = []
        self.subdiretorios = []
        self.bloco = bloco

class ArquivoSystemSimulator:
    def __init__(self, tamanho_memoria, bloco_tamanho, num_discos):
        self.tamanho_memoria = tamanho_memoria
        self.bloco_tamanho = bloco_tamanho
        self.num_discos = num_discos
        self.discos = [Disco(i) for i in range(num_discos)]
        self.raiz_diretorio = None
        self.init_discos()

def alocar_blocos(self, num_blocos):
    blocos_alocados = []
    for disco in self.discos:
        if len(disco.blocos_livres) >= num_blocos:
            blocos_alocados = disco.blocos_livres[:num_blocos]
            disco.blocos_livres = disco.blocos_livres[num_blocos:]
            break
    
    if not blocos_alocados:
        print("Não há blocos livres o bastante para alocacao")
        return None

    for disco in self.discos:
        for bloco in blocos_alocados:
            disco.memoria[bloco] = True

        # Display Uso de memoria
        print(f"Blocos alocados: {blocos_alocados}")
        print(f"Uso de memoria em cada disco:")
        for disco in self.discos:
            print(f"Disco {disco.id}: {disco.memoria.count(True) * self.bloco_tamanho} bytes / {self.tamanho_memoria} bytes")
        print(f"Uso de memoria total: {sum(disco.memoria.count(True) for disco in self.discos) * self.bloco_tamanho} bytes / {self.num_discos * self.tamanho_memoria} bytes")

        return blocos_alocados

    def init_discos(self):
        for disco in self.discos:
            disco.blocos_livres = list(range(self.tamanho_memoria // self.bloco_tamanho))

    def desalocar_blocos(self, blocos):
        self.blocos_livres.extend(blocos)
        self.blocos_livres.sort()

        # Display Uso de memoria
        print(f"Blocos desalocados: {blocos}")
        print(f"Blocos livres: {self.blocos_livres}")
        print(f"Uso de memoria: {len(self.memoria) * self.bloco_tamanho - len(self.blocos_livres) * self.bloco_tamanho} bytes / {self.tamanho_memoria} bytes")

    def criar_arquivo(self, diretorio, nome, tamanho):
        #Checa se o nome do arquivo já existe nos arquivos pertencentes ao atual diretório
        if diretorio and any(arquivo.nome == nome for arquivo in diretorio.arquivos):
            print(f"Arquivo '{nome}' ja existe no diretorio '{diretorio.nome}'.")
            return
        
        # Checa se o nome do arquivo é o mesmo de algum subdiretório que já existe
        if diretorio and any(subdir.nome == nome for subdir in diretorio.subdiretorios):
            print(f"Arquivo '{nome}' não pode ter o mesmo nome que um subdiretorio no diretorio '{diretorio.nome}'.")
            return
        
        # Checa se o nome do arquivo é o mesmo que o nome de um diretório já alocado
        if diretorio and diretorio.nome == nome:
            print("Não pode alocar um arquivo com o mesmo nome que o diretorio.")
            return

        blocos_necessarios = (tamanho + self.bloco_tamanho - 1) // self.bloco_tamanho
        blocos_alocados = self.alocar_blocos(blocos_necessarios)

        if blocos_alocados is None:
            print("fragmentacao detectada! Não há blocos o bastante para alocação.")
            return

        new_arquivo = Arquivo(nome, tamanho)
        new_arquivo.blocos = blocos_alocados

        if diretorio:
            diretorio.arquivos.append(new_arquivo)
            print(f"Arquivo '{nome}' criado medindo {tamanho} bytes no diretorio '{diretorio.nome}'. Blocos alocados: {blocos_alocados}")
        else:
            self.raiz_diretorio.arquivos.append(new_arquivo)
            print(f"Arquivo '{nome}' criado como um arquivo independente medindo {tamanho} bytes. Blocos alocados: {blocos_alocados}")

    def criar_diretorio(self, parent_diretorio, nome):
        # Checa se o diretório possui um nome já existente no atual diretorio
        if any(subdir.nome == nome for subdir in parent_diretorio.subdiretorios):
            print(f"'{nome}'  já existe como um diretório nessa sessão.")
            return

        # Checa se já existe um arquivo com o mesmo nome que o diretório nessa sessão
        if any(arquivo.nome == nome for arquivo in parent_diretorio.arquivos):
            print(f"Não se pode criar o diretorio '{nome}', já existe um arquivo com o mesmo nome nessa sessão.")
            return

        bloco = self.alocar_blocos(1)[0]
        new_diretorio = Diretorio(nome, bloco)
        parent_diretorio.subdiretorios.append(new_diretorio)
        print(f"Diretorio '{nome}' criado. bloco: {bloco}")

    def listar_conteudo(self, diretorio):
        for arquivo in diretorio.arquivos:
            print(f"- Arquivo: {arquivo.nome} ({arquivo.tamanho} bytes)")
            print(f"  blocos: {arquivo.blocos}")
            
        for subdiretorio in diretorio.subdiretorios:
            print(f"- Diretorio: {subdiretorio.nome} (bloco: {subdiretorio.bloco})")
            if subdiretorio.arquivos:
                print("  Arquivos:")
                for arquivo in subdiretorio.arquivos:
                    print(f"  - Arquivo: {arquivo.nome} ({arquivo.tamanho} bytes)")
                    print(f"    blocos: {arquivo.blocos}")

    def deletar_arquivo(self, diretorio, nome):
        found_arquivo = None
        for arquivo in diretorio.arquivos:
            if arquivo.nome == nome:
                found_arquivo = arquivo
                break

        if found_arquivo is not None:
            self.desalocar_blocos(found_arquivo.blocos)
            diretorio.arquivos.remove(found_arquivo)
            print(f"Arquivo '{nome}' deletado.")
        else:
            print(f"Arquivo '{nome}' não encontrado.")

    def deletar_diretorio(self, parent_diretorio, nome):
        found_diretorio = None
        for subdiretorio in parent_diretorio.subdiretorios:
            if subdiretorio.nome == nome:
                found_diretorio = subdiretorio
                break

        if found_diretorio is not None:
            self.recursively_desalocados_diretorio_blocos(found_diretorio)
            parent_diretorio.subdiretorios.remove(found_diretorio)
            print(f"Diretorio '{nome}' deletado.")
        else:
            print(f"Diretorio '{nome}' não encontrado.")

    def recursively_desalocar_diretorio_blocos(self, diretorio):
        for arquivo in diretorio.arquivos:
            self.desalocar_blocos(arquivo.blocos)
        for subdiretorio in diretorio.subdiretorios:
            self.recursively_desalocar_diretorio_blocos(subdiretorio)

    def get_diretorio_by_nome(self, parent_diretorio, nome):
        for subdiretorio in parent_diretorio.subdiretorios:
            if subdiretorio.nome == nome:
                return subdiretorio
        return None

if __name__ == "__main__":
    tamanho_memoria = 2048  
    bloco_tamanho = 256 
    num_discos = 12

    fs_simulator = ArquivoSystemSimulator(tamanho_memoria, bloco_tamanho, num_discos)
    current_diretorio = fs_simulator.raiz_diretorio

    while True:
        command = command = input(f"Atual diretório: {current_diretorio.nome if current_diretorio else 'raiz'} "
                        f"(bloco: {current_diretorio.bloco if current_diretorio else 'N/A'})\n"
                        "Insira um comando (criar_arquivo, criar_diretorio, listar_conteudo, deletar_arquivo, deletar_diretorio): ")

        if command == "criar_arquivo":
            nome = input("Digite o nome do arquivo: ")
            tamanho = int(input("Digite o tamanho do arquivo: "))
            is_inside_diretorio = input("Esse arquivo pertence a um diretório? (s/n): ").lower()

            if is_inside_diretorio == "s":
                diretorio_nome = input("Digite o nome do diretorio: ")
                diretorio = fs_simulator.get_diretorio_by_nome(current_diretorio, diretorio_nome)
                if diretorio:
                    fs_simulator.criar_arquivo(diretorio, nome, tamanho)
                else:
                    print(f"Diretorio '{diretorio_nome}' não encontrado.")
            else:
                fs_simulator.criar_arquivo(None, nome, tamanho)

        elif command == "criar_diretorio":
           nome = input("Digite o nome do diretorio: ")
           fs_simulator.criar_diretorio(current_diretorio, nome)

        elif command == "listar_conteudo":
           fs_simulator.listar_conteudo(current_diretorio)

        elif command == "deletar_arquivo":
            nome = input("Digite o nome do arquivo: ")
            fs_simulator.deletar_arquivo(current_diretorio, nome)

        elif command == "deletar_diretorio":
            nome = input("Digite o nome do diretorio: ")
            fs_simulator.deletar_diretorio(current_diretorio, nome)

        else:
            print("Comando inválido.")
