import os
import pprint

class Unzipper:
    def __init__(self, path):

        self.path = path
        self.full_map = self.process()

    
    def process(self, current_path):
        itens = 




if __name__ == "__main__":

    uz = Unzipper(r"C:\Users\horsf\Documents\Projetos\Unzipper\Teste")
    print("Estrutura de arquivos mapeada:")
    pprint.pprint(uz.full_map)

    