class ViginereBreaker:
    def __init__(self):
        self.IOC_INGLES = 0.066
        self.IOC_PORTUGUES = 0.074
        self.IOC_ALEAORIO = 0.0385
        self.TAM_MAX_CHAVE = 20
        self.freq_relativa_ingles = [8.167,1.492,2.782,4.253,12.702,2.228,2.015,6.094,6.966,0.253,1.772,4.025,2.406,6.749,7.507,1.929,0.095,5.987,6.327,9.056,2.758,0.978,2.360,0.250,1.974,0.074]
        self.freq_relativa_portugues = [14.634,1.043,3.882,4.992,12.570,1.023,1.303,1.281,6.186,0.879,0.015,2.779,4.738,4.446,9.735,2.523,1.204,6.530,6.805,4.336,3.639,1.575,0.037,0.453,0.006,0.470]
        self.char_mais_frequente_ingles = chr(ord(chr(max([(j, i) for i, j in enumerate(self.freq_relativa_ingles)])[1] + ord('a'))))
        self.char_mais_frequente_portugues = chr(ord(chr(max([(j, i) for i, j in enumerate(self.freq_relativa_portugues)])[1] + ord('a'))))
        
    def get_ioc(text):
        frequency = {}
        for char in text:
            frequency[char] = frequency.get(char,0) + 1
        # frequency.pop('\n')
        acumulador = 0
        n = len(text)
        for char in frequency.keys():
            acumulador += frequency[char]*(frequency[char]-1)
        return acumulador/(n*(n-1))
    
    def calcula_tamanho_chave_e_lingua(self):
        for i in range(2,self.TAM_MAX_CHAVE):
            curr_ioc = ViginereBreaker.get_ioc(self.full_ciphertext[::i])
            dist_to_aleatorio = abs(curr_ioc-self.IOC_ALEAORIO)
            dist_to_ingles = abs(curr_ioc-self.IOC_INGLES)
            dist_to_portugues = abs(curr_ioc-self.IOC_PORTUGUES)
            menor_dist = min(dist_to_aleatorio,dist_to_ingles,dist_to_portugues)
            if menor_dist != dist_to_aleatorio:
                self.tamanho_chave = i
                self.lingua_detectada = 'pt' if menor_dist == dist_to_portugues else 'en'
                break
        print('\tlingua detectada:', self.lingua_detectada)
        print('\ttamanho de chave encontrado:', self.tamanho_chave)
    
    def calcula_frequencia(texto: str,caracter: str):
        return (texto.count(caracter)/len(texto))*100
    
    def calcula_chave(self):
        letra_mais_frequente_da_lingua = self.char_mais_frequente_portugues if self.lingua_detectada=='pt' else self.char_mais_frequente_ingles
        letras_candidatas = []
        for i in range(self.tamanho_chave):
            letra_to_freq = {}
            texto_com_mesmo_deslocamento = self.full_ciphertext[i::self.tamanho_chave]
            for i in range(26):
                caracter = chr(i+97)
                letra_to_freq[caracter] = ViginereBreaker.calcula_frequencia(texto_com_mesmo_deslocamento,caracter)
            letra_to_freq = list(letra_to_freq.items())
            letra_to_freq.sort(key = lambda x: x[1], reverse=True)
            # print(letra_to_freq)
            letra_mais_frequente_no_texto = letra_to_freq[0][0]
            segunda_letra_mais_frequente = letra_to_freq[1][0]
            letras_candidatas.append((letra_mais_frequente_no_texto, segunda_letra_mais_frequente))
        print('\topcoes de chave:')
        for primeira,segunda in letras_candidatas:
            deslocamento_primeira = abs(ord(primeira) - ord(letra_mais_frequente_da_lingua))
            deslocamento_segunda = abs(ord(segunda) - ord(letra_mais_frequente_da_lingua))
            primeira_opcao_chave = chr(deslocamento_primeira+ord('a'))
            segunda_opcao_chave = chr(deslocamento_segunda+ord('a'))
            
            print('\t\t'+primeira_opcao_chave,segunda_opcao_chave)
        
        chave = input('\tDigite a chave: ')
            
        self.chave = chave
    
    def calcula_texto_decifrado(self):
        texto_decifrado = ''
        for idx,letra in enumerate(self.full_ciphertext):
            char_chave = self.chave[idx%len(self.chave)]
            deslocamento = ord(char_chave) - ord('a')
            idx_letra_alfabeto = ord(letra) - ord('a')
            nova_pos_alfabeto = idx_letra_alfabeto-deslocamento
            letra_original = (26+nova_pos_alfabeto)%26
            letra_original = chr(letra_original+ord('a'))
            texto_decifrado += letra_original
        self.texto_decifrado = texto_decifrado
        
    def decifra(self, full_ciphertext):
        self.full_ciphertext = full_ciphertext
        self.calcula_tamanho_chave_e_lingua()
        self.calcula_chave()
        self.calcula_texto_decifrado()
        return self.texto_decifrado
    
    def save_plaintext_file(self, path, filename):
        with open(path+filename, 'w') as plaintext_file:
            plaintext_file.write(self.texto_decifrado)
        

if __name__=='__main__':
    diretorio_com_cifras = r'./Textos cifrados-20240402' + '//'
    diretorio_plaintext = r'./Textos_decifrados' + '//'
    for counter in range(1,32):
        filename = f'cipher{counter}.txt'
        with open(diretorio_com_cifras+filename) as file:
            print(f"decifrando {filename}")
            texto_cifrado = file.read()
            decifrador = ViginereBreaker()
            decifrador.decifra(texto_cifrado)
            decifrador.save_plaintext_file('', diretorio_plaintext+f'plaintext{counter}.txt')
            
    # testes = [r'20201-teste1.txt', r'20201-teste2.txt']
    # idx = 1
    # with open(testes[idx]) as file:
    #     texto_cifrado = file.read()
    #     decifrador = ViginereBreaker()
    #     decifrador.decifra(texto_cifrado)
    #     print(decifrador.texto_decifrado)
    #     decifrador.save_plaintext_file('', 'plaintext_'+testes[idx])
        