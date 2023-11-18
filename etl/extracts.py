import pandas as pd

class Extracts:
    def __init__(self,datasource):
        self.datasource = datasource

    def read_csv_file(self):
        df = pd.read_csv(filepath_or_buffer=self.datasource)
        return df
    
    def read_excel_file(self):
        df = pd.read_excel(io=self.datasource)
        return df
    
    def read_json_file(self):
        df = pd.read_json(filepath_or_buf=self.datasource)
        return df
    
    def read_xml_file(self):
        df = pd.read_xml(filepath_or_buffer=self.datasource)
        return df
    
    def read_html_file(self):
        df = pd.read_html(io=self.datasource)
        return df
    
    def read_pickle_file(self):
        df = pd.read_pickle(filepath_or_buffer=self.datasource)
        return df