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
        self.num_discos = num_discos  #ATUALIZAÇÃO: Número de discos.
        self.memoria = [None] * (tamanho_memoria // bloco_tamanho)
        self.blocos_livres = list(range(len(self.memoria)))
        self.discos = [[] for _ in range(num_discos)]  #ATUALIZAÇÃO: Lista de discos
        self.raiz_diretorio = Diretorio("raiz", self.alocar_blocos(1)[0])
    
    #ATUALIZAÇÃO: Inicializar os discos
        for _ in range(1, num_discos):
            self.discos[_] = self.blocos_livres.copy()

    #ATUALIZAÇÃO: Alocar blocos no disco escolhido
    def alocar_blocos_em_disco(self, num_blocos, disco):
        if len(self.discos[disco]) < num_blocos:
            print("Não há blocos livres o bastante para alocação no disco escolhido.")
            return None

        blocos_alocados = self.discos[disco][:num_blocos]
        self.discos[disco] = self.discos[disco][num_blocos:]

        return blocos_alocados
    
    #ATUALIZAÇÃO: Função para criar o arquivo no disco escolhido.
    def criar_arquivo_em_disco(self, diretorio, nome, tamanho, disco):
        if disco < 0 or disco >= self.num_discos:
            print("Disco inválido.")
            return

        blocos_necessarios = (tamanho + self.bloco_tamanho - 1) // self.bloco_tamanho
        blocos_alocados = self.alocar_blocos_em_disco(blocos_necessarios, disco)

        if blocos_alocados is None:
            print("Fragmentacao detectada! Não há blocos o bastante para alocação.")
            return
        
        new_arquivo = Arquivo(nome, tamanho)
        new_arquivo.blocos = blocos_alocados
    
        if diretorio:
            diretorio.arquivos.append(new_arquivo)
            print(f"Arquivo '{nome}' criado medindo {tamanho} bytes no diretório '{diretorio.nome}' no disco {disco}. Blocos alocados: {blocos_alocados}")
        else:
            self.raiz_diretorio.arquivos.append(new_arquivo)
            print(f"Arquivo '{nome}' criado como um arquivo independente medindo {tamanho} bytes no disco {disco}. Blocos alocados: {blocos_alocados}")

    #ATUALIZAÇÃO: Função para criar o diretório no disco escolhido.       
    def criar_diretorio_em_disco(self, parent_diretorio, nome, disco):
        if disco < 0 or disco >= self.num_discos:
            print("Disco inválido.")
            return

        bloco = self.alocar_blocos_em_disco(1, disco)[0]
        new_diretorio = Diretorio(nome, bloco)
        parent_diretorio.subdiretorios.append(new_diretorio)
        print(f"Diretório '{nome}' criado no bloco {bloco} do disco {disco}.")

    #ATUALIZAÇÃO: implementação do RAID 0
    def nivel_raid(self):
        return "RAID 0"  # Retorna o nível de RAID implementado

    def alocar_blocos(self, num_blocos):
        if len(self.blocos_livres) < num_blocos:
            print("Não há blocos livres o bastante para a alocacao")
            return None

        blocos_alocados = self.blocos_livres[:num_blocos]
        self.blocos_livres = self.blocos_livres[num_blocos:]

        # Distribui os blocos pelos discos (striping RAID 0)
        for i, bloco in enumerate(blocos_alocados):
            self.discos[i % self.num_discos].append(bloco)  # Atualização: Distribuição em discos

        # Display Uso de memoria
        print(f"Blocos alocados: {blocos_alocados}")
        print(f"Blocos livres: {self.blocos_livres}")
        print(f"Uso de memoria: {len(blocos_alocados) * self.bloco_tamanho} bytes / {self.tamanho_memoria} bytes")

        #ATUALIZAÇÃO: Mostra a alocação nos discos
        for i, disco in enumerate(self.discos):
            print(f"Disco {i}: {disco}")

        if len(blocos_alocados) < num_blocos:
            print(f"Fragmentacao Interna: {num_blocos - len(blocos_alocados)} blocos")
        else:
            print("Sem Fragmentacao Interna")

        return blocos_alocados

    def desalocar_blocos(self, blocos):
        self.blocos_livres.extend(blocos)
        self.blocos_livres.sort()

         #ATUALIZAÇÃO: Remove os blocos dos discos
        for bloco in blocos:
            for disco in self.discos:
                if bloco in disco:
                    disco.remove(bloco)
                    break

        # Display Uso de memoria
        print(f"Blocos desalocados: {blocos}")
        print(f"Blocos livres: {self.blocos_livres}")
        print(f"Uso de memoria: {len(self.memoria) * self.bloco_tamanho - len(self.blocos_livres) * self.bloco_tamanho} bytes / {self.tamanho_memoria} bytes")

    def criar_arquivo(self, diretorio, nome, tamanho):
        escolher_disco = input("Deseja escolher o disco para alocar o arquivo? (s/n): ").lower()
        if escolher_disco == "s":
            disco = int(input(f"Escolha o disco (0 a {self.num_discos - 1}): "))
            self.criar_arquivo_em_disco(diretorio, nome, tamanho, disco)
        else:
            blocos_alocados = self.alocar_blocos(blocos_necessarios)

            if blocos_alocados is None:
                print("Fragmentacao detectada! Não há blocos o bastante para alocação.")
                return
            
            new_arquivo = Arquivo(nome, tamanho)
            new_arquivo.blocos = blocos_alocados

            if diretorio:
                diretorio.arquivos.append(new_arquivo)
                print(f"Arquivo '{nome}' criado medindo {tamanho} bytes no diretório '{diretorio.nome}' no Disco {disco}. Blocos alocados: {blocos_alocados}")
            else:
                self.raiz_diretorio.arquivos.append(new_arquivo)
                print(f"Arquivo '{nome}' criado como um arquivo independente medindo {tamanho} bytes no Disco {disco}. Blocos alocados: {blocos_alocados}")

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

        escolher_disco = input("Deseja escolher o disco para alocar o diretório? (s/n): ").lower()
        if escolher_disco == "s":
            disco = int(input(f"Escolha o disco (0 a {self.num_discos - 1}): "))
            self.criar_diretorio_em_disco(parent_diretorio, nome, disco)
        else:
            bloco = self.alocar_blocos(1)[0]
            new_diretorio = Diretorio(nome, bloco)
            parent_diretorio.subdiretorios.append(new_diretorio)
            print(f"Diretório '{nome}' criado no bloco {bloco} do Disco 0.")
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
    tamanho_memoria = 1024  
    bloco_tamanho = 64 
    num_discos = 8  #ATUALIZAÇÃO: Número de discos na configuração RAID 0

    fs_simulator = ArquivoSystemSimulator(tamanho_memoria, bloco_tamanho, num_discos)
    current_diretorio = fs_simulator.raiz_diretorio

    while True:
        command = input(f"Atual diretorio: {current_diretorio.nome} (bloco: {current_diretorio.bloco})\n"
                        f"Nível de RAID: {fs_simulator.nivel_raid()}\n" # Exibe o nível de RAID
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

          