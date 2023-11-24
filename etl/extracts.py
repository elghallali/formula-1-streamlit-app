import pandas as pd

class Extracts:
    def __init__(self,datasource,extension):
        self.datasource = datasource
        self.extension = extension

    def __read_csv_file(self, sep=','):
        df = pd.read_csv(filepath_or_buffer=self.datasource, sep=sep)
        return df
    
    def __read_excel_file(self):
        df = pd.read_excel(io=self.datasource)
        return df
    
    def __read_json_file(self):
        df = pd.read_json(filepath_or_buf=self.datasource)
        return df
    
    def __read_xml_file(self):
        df = pd.read_xml(filepath_or_buffer=self.datasource)
        return df
    
    def __read_html_file(self):
        df = pd.read_html(io=self.datasource)
        return df
    
    def __read_pickle_file(self):
        df = pd.read_pickle(filepath_or_buffer=self.datasource)
        return df
    
    def load_data(self):
        if self.extension in ['xlsx', 'xls']:
            return self.__read_excel_file()
        elif self.extension in ['csv', 'tsv', 'txt']:
            return self.__read_csv_file()
        elif self.extension == 'tsv':
            return self.__read_csv_file(sep=' ')
        elif self.extension == 'json':
            return self.__read_json_file()
        elif self.extension == 'html':
            return self.__read_html_file()
        elif self.extension == 'xml':
            return self.__read_xml_file()
        else:
            return self.__read_html_file()