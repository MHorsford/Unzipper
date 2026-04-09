import os
import pprint
import zipfile as zf
from pathlib import Path
import shutil

class Unzipper:

    def __init__(self, source_folder: str | Path, destination_folder: str | Path | None=None, MAX_DEPTH: int | None=None):

        os.makedirs(source_folder, exist_ok=True)

        os.makedirs(destination_folder, exist_ok=True)

        self.backup_path = Path('process/backup')
        self.archived_path = Path('process/archived') 

        os.makedirs(self.archived_path, exist_ok=True)
        os.makedirs(self.backup_path, exist_ok=True)

        shutil.copytree(source_folder, self.backup_path, dirs_exist_ok=True)
        
        self.source_path = Path(source_folder).resolve()
        self.destination_path  = Path(destination_folder).resolve() if destination_folder else self.source_path
        self.extraction_plan = {}
        self.count = 0
        print(f'Pasta raiz: {self.source_path} \nPasta Destino: {self.destination_path}\n\n\n')
        

    def scan(self, source_path: str | Path| None=None):
        if source_path is None:
            source_path = self.source_path
        source_path = Path(source_path).resolve()
        for item in source_path.rglob('*.zip'):
            relative = item.relative_to(source_path)
            #print(f'Caminho Relativo do Arquivo: {relative}\n')  # Apagar
            destination = self.destination_path / relative.parent / item.stem
            #print(f'Pasta Destino do Arquivo: {destination}\n')  # Apagar
            if item.is_file():
                if item not in self.extraction_plan:
                    self.extraction_plan[item] = {
                        'Item': item,
                        'Destination': destination,
                        'Status': 'pending',
                        'Error': None
                    }
        
        print(100*'#')
        pprint.pprint(f'Plano de Extração: {self.extraction_plan}')


    def extract(self):
            for item in self.extraction_plan.values():

                if item['Status'] == 'pending':
                    try:
                        item['Destination'].mkdir(parents=True, exist_ok=True)
                        with zf.ZipFile(item['Item']) as zip_ref: 
                            zip_ref.extractall(item['Destination'])
                            
                    except:
                        pass
                    else:
                        item['Status'] = 'extracted'
                        shutil.move(item['Item'], self.archived_path)
                    finally:
                        pass
                        

            self.scan(self.destination_path)
            if any(item['Status'] == 'pending' for item in self.extraction_plan.values()):
                self.extract()

  


if __name__ == "__main__":

    uz = Unzipper("C:/Users/horsf/Documents/Projetos/Unzipper/Teste", "C:/Users/horsf/Documents/Projetos/Unzipper/Destino_Temp")
    print('-----------------------------------------')
    uz.scan()
    print('-----------------------------------------')
    uz.extract()





























































    