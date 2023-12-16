import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import os
import io
import qrcode
from io import BytesIO
import warnings

warnings.filterwarnings('ignore')

path_file = os.getcwd() + '/images/f1_logo.png'
logo = Image.open(path_file)

path_car = os.getcwd() + '/images/image.webp'
car = Image.open(path_car)

# Create QR for Data Source Link 
qr_datasource = qrcode.make("https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020")

# Create QR for Our Application Link 
qr_applink = qrcode.make("https://formula-1-app.streamlit.app/")

path_dashboard_driver_file = os.getcwd() + '/images/Formula-1-Dashboard.png'
dashboard_driver = Image.open(path_dashboard_driver_file)

path_dashboard_team_file = os.getcwd() + '/images/Formula-1-Dashboard-team.png'
dashboard_team = Image.open(path_dashboard_team_file)

st.set_page_config(
    page_title='Formula 1 | Home',
    page_icon=logo,
    layout='wide'
)
col_logos_1,col_logos_2,col_logos_3 = st.columns([1,8,1])
with col_logos_2:
    st.markdown("""
            <style>
                .logos {
                    background-color: white;
                    height: 170px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    border-radius: 0 0 5px 5px;
                }
                
            </style>
            <div class="logos">
              <img src="https://raw.githubusercontent.com/elghallali/my-images/master/Faculty%20Official/fsjest.jpg" title="fsjest" alt="fsjest" width="150" height="150" />
              <img src="https://raw.githubusercontent.com/elghallali/my-images/master/Faculty%20Official/logo.png" title="DSDS" alt="DSDS" width="400" height="150"/>
              <img src="https://raw.githubusercontent.com/elghallali/my-images/master/Faculty%20Official/uae.png" title="UAE" **alt="UAE" width="150" height="150" /> 
            </div>
    """,unsafe_allow_html=True)
st.markdown("""
            
            <div align="center" >

            # <img src="https://raw.githubusercontent.com/elghallali/formula-1-streamlit-app/master/images/f1_logo.png" alt="Formula 1 Logo" width=100/> Formula 1 Application

            </div>
            """,unsafe_allow_html=True)
st.markdown('<style> div.block-container {padding-top: 0.1rem;}</style>',unsafe_allow_html=True)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

with st.container():
    col_img0, col_img1, col_img2 = st.columns([1,8,1])
    with col_img1:
        st.image('https://www.cnet.com/a/img/resize/46b2fd5f0a17ea81e247b83132fff08df9cda0cb/hub/2021/07/15/56433bea-88e8-42bc-b9a7-4c158b3225b5/image.jpg?auto=webp&fit=crop&height=675&width=1200')

with st.container():
    
    col_team0, col_team1, col_team2, col_team3 = st.columns([1,4,4,1])
    with col_team1:
        st.markdown("""
                <style>
                    .centered-header {
                        text-align: center;
                    }
                </style>
            """, unsafe_allow_html=True)
        st.markdown('<h2 class="centered-header">Team</h2>', unsafe_allow_html=True)
        team = pd.DataFrame({'Name':['Yassine EL GHALLALI', 'Rabia SLAOUI', 'Issam EL MEHDI', 'Said SEHLALI']})
        fig = ff.create_table(team, height_constant=30, colorscale=[[0, '#4d004c'],[.5, '#f2e5ff'],[1, '#ffffff']])
        fig.update_layout(font=dict(size=20))
        st.plotly_chart(fig, use_container_width=True)
        
    with col_team2:
        st.markdown("""
                <style>
                    .centered-header {
                        text-align: center;
                    }
                </style>
            """, unsafe_allow_html=True)
        st.markdown('<h2 class="centered-header">Proposed by</h2>', unsafe_allow_html=True)
        team = pd.DataFrame({'Prof':['Anass BENNANI']})
        fig = ff.create_table(team, height_constant=30, colorscale=[[0, '#4d004c'],[.5, '#f2e5ff'],[1, '#ffffff']])
        fig.update_layout(font=dict(size=30))
        st.plotly_chart(fig, use_container_width=True)

with st.container():
    st.header('Description')
    st.subheader('Data Source & the link of our Application')
    # Convert PilImage to bytes
    img_bytes_1 = BytesIO()
    qr_datasource.save(img_bytes_1, format='PNG')  # Assuming PNG format, change accordingly

    img_bytes_2 = BytesIO()
    qr_applink.save(img_bytes_2, format='PNG')
    datasource_col0,datasource_col1,datasource_col2,datasource_col3,datasource_col4 = st.columns(5)
    with datasource_col1:
        # Display the QR code in Streamlit
        st.image(img_bytes_1, caption='Data Source QR Code')
    with datasource_col3:
        # Display the QR code in Streamlit
        st.image(img_bytes_2, caption='Our Application QR Code')
    st.subheader('Tools')
    tool1,tool2,tool3,tool4,tool5,tool6,tool7,tool8,tool9,tool10,tool11= st.columns(11)
    st.markdown("""
        <style>
            .image {
                background-color: transparent;
                border: none;  /* Remove the button border */
                background-color: white;
                width: 100px;
                height: 100px;
                border-radius: 5px;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .image img {
                position:relative
                padding:5px;
            }
            .image:hover {
                background-color: #999999;
            }
            .github_actions {
                padding: 15px 5px 0px 5px;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
            }
            
            .github_actions p {
                color: black;
                font-size: 14px;
            }
            
        </style>
    """, unsafe_allow_html=True)
    with tool1:
        st.markdown("""
                    <div class="image">
                    <img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/python/python-original-wordmark.svg" alt="" with=80 height=80>
                    </div>
                    
                    """, unsafe_allow_html=True)
    with tool2:
        st.markdown("""
                 <div class="image">
                 <img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/vscode/vscode-original-wordmark.svg" alt="" with=80 height=80>
                 </div>
                 """, unsafe_allow_html=True)
    with tool3:
        st.markdown("""
                 <div class="image">
                 <img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/git/git-original-wordmark.svg" alt="" with=80 height=80>
                 </div>
                 """, unsafe_allow_html=True)
    with tool4:
        st.markdown("""
                 <div class="image">
                 <img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/docker/docker-plain-wordmark.svg" alt="" with=80 height=80>
                 </div>
                 """, unsafe_allow_html=True)
    with tool5:
        st.markdown("""
                 <div class="image">
                 <img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/numpy/numpy-original-wordmark.svg" alt="" with=80 height=80>
                 </div>
                 """, unsafe_allow_html=True)
    with tool6:
        st.markdown("""
                 <div class="image">
                 <img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/pandas/pandas-original-wordmark.svg" alt="" with=80 height=80>
                 </div>
                 """, unsafe_allow_html=True)
    with tool7:
        st.markdown("""
                 <div class="image">
                 <img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/github/github-original-wordmark.svg" alt="" with=80 height=80>
                 </div>
                 """, unsafe_allow_html=True)
    with tool8:
        st.markdown("""
                 <div class="image">
                 <img src="https://raw.githubusercontent.com/elghallali/my-images/aff6e3ea2f3f31483187856b7c9d412852c9205c/streamlit-logo-primary-colormark-darktext.svg" alt="" with=80 height=60>
                 </div>
                 """, unsafe_allow_html=True)
    with tool9:
        st.markdown("""
                 <div class="image">
                 <img src="https://camo.githubusercontent.com/20db5efd6873b071b1c72818028df47ce86c511d7560e789c34ba1811593c3eb/68747470733a2f2f73746f72652d696d616765732e732d6d6963726f736f66742e636f6d2f696d6167652f617070732e33363836382e62666230653265652d626539652d346337332d383037662d6530613762383035623162652e37313261666635642d353830302d343765302d393762652d3538643137616461336662382e61343638343565362d636539342d343463662d383932622d353436333763366663663036" alt="" with=80 height=80>
                 </div>
                 """, unsafe_allow_html=True)
    with tool10:
        st.markdown("""
                 <div class="image">
                    <div class="github_actions">
                      <img src="https://raw.githubusercontent.com/elghallali/my-images/aff6e3ea2f3f31483187856b7c9d412852c9205c/GitHub%20Actions.svg" alt="" with=50 height=50>
                      <p>GitHub Actions</p>
                    </div>
                 </div>
                 """, unsafe_allow_html=True)
    with tool11:
        st.markdown("""
                 <div class="image">
                 <img src="https://camo.githubusercontent.com/9f56ecb12a5b746c29c31e08e91a1f3cf483f8a3657118be1530cf8c3ae674a2/68747470733a2f2f6475636b64622e6f72672f696d616765732f6c6f676f2d646c2f4475636b44425f4c6f676f2d737461636b65642e737667" alt="" with=80 height=60>
                 </div>
                 """, unsafe_allow_html=True)

    st.subheader('ETL')
    col_etl = st.columns(4)
    with col_etl[0]:
      button1 = st.button('**Extracts**',use_container_width=True)
    with col_etl[1]:
      button2 =st.button('**Transforms**',use_container_width=True)
    with col_etl[2]:
      button3 = st.button('**Loads**',use_container_width=True)
    with col_etl[3]:
      button4 = st.button('**Data**',use_container_width=True)
    if button1:
        st.code("""
import pandas as pd

class Extracts:
    def __init__(self,datasource):
        self.datasource = datasource
        self.extension = self.datasource.split('/')[-1].split('.')[-1]
        self.name = self.datasource.split('/')[-1].split('.')[0].replace('_',' ').capitalize()

    def __read_csv_file(self, sep=','):
        df = pd.read_csv(filepath_or_buffer=self.datasource, sep=sep)
        return df,self.name
    
    def __read_excel_file(self):
        df = pd.read_excel(io=self.datasource)
        return df,self.name
    
    def __read_json_file(self):
        df = pd.read_json(filepath_or_buf=self.datasource)
        return df,self.name
    
    def __read_xml_file(self):
        df = pd.read_xml(filepath_or_buffer=self.datasource)
        return df,self.name
    
    def __read_html_file(self):
        df = pd.read_html(io=self.datasource)
        return df,self.name
    
    def __read_pickle_file(self):
        df = pd.read_pickle(filepath_or_buffer=self.datasource)
        return df,self.name
    
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
""")
    if button2:
        st.code("""
import pandas as pd

class Transforms:
    def __init__(self,dataset,param0='',param1='',how='inner'):
        self.dataset = dataset
        self.param0 = param0
        self.param1 = param1
        self.how = how

    def split_columns(self):
        df = self.dataset[self.param0].str.split(self.param1, expand=True)
        return df
    
    def transform_state(self):
        df = pd.merge(self.dataset, self.param0, on=self.param1, how=self.how)
        return df
    
""")
    if button3:
        st.code("""
import pandas as pd

class Loads:
    def __init__(self,dataset, outputdir,filename):
        self.dataset = dataset
        self.outputdir = outputdir
        self.filename = filename

    def send_to_csv(self):
        self.dataset.to_csv(path_or_buf=self.outputdir + self.filename, index=False)
    
    def send_to_excel(self):
        self.dataset.to_excel(excel_writer=self.outputdir + self.filename, index=False)

    def send_to_parquet(self):
        self.dataset.to_parquet(path=self.outputdir + self.filename, index=False)

    def send_to_feather(self):
        self.dataset.to_feather(path=self.outputdir + self.filename)

    def send_to_pickle(self):
        self.dataset.to_pickle(path=self.outputdir + self.filename, compression='gzip')
""")
    if button4:
        st.code("""
import pandas as pd
import numpy as np
import os

from etl.extracts import Extracts
from etl.transforms import Transforms

#############################################################################
###                                                                       ###
###                             Extracts data                             ###
###                                                                       ###
#############################################################################

circuits = Extracts(os.getcwd() +'/data/circuits.csv').load_data()
laptimes = Extracts(os.getcwd() +'/data/lap_times.csv').load_data()
pitstops = Extracts(os.getcwd() +'/data/pit_stops.csv').load_data()
seasons = Extracts(os.getcwd() +'/data/seasons.csv').load_data()
status = Extracts(os.getcwd() +'/data/status.csv').load_data()
constructor_standings = Extracts(os.getcwd() +'/data/constructor_standings.csv').load_data()
constructors = Extracts(os.getcwd() +'/data/constructors.csv').load_data()
driver_standings = Extracts(os.getcwd() +'/data/driver_standings.csv').load_data()
drivers = Extracts(os.getcwd() +'/data/drivers.csv').load_data()
races = Extracts(os.getcwd() +'/data/races.csv').load_data()
constructor_results = Extracts(os.getcwd() +'/data/constructor_results.csv').load_data()
results = Extracts(os.getcwd() +'/data/results.csv').load_data()
qualifying = Extracts(os.getcwd() +'/data/qualifying.csv').load_data()

#############################################################################
###                                                                       ###
###                            Transform Data                             ###
###                                                                       ###
#############################################################################
def factTable():

    races[0]['GPName'] = races[0]['name']

    constructors[0]['brandNationality']= constructors[0]['nationality']
    constructors[0]['brand']= constructors[0]['name']

    drivers[0]['driverName']= drivers[0]['forename']+ ' ' + drivers[0]['surname']
    drivers[0]['driverNationality']= drivers[0]['nationality']
    qualifying[0]['startingPosition'] = qualifying[0]['position']
    df_pitstop = pitstops[0].groupby(['raceId', 'driverId']).agg(duration=('milliseconds', 'sum')).reset_index()
    
    df = Transforms(results[0], param0=races[0][['raceId','year','GPName','round']],param1='raceId',how='left').transform_state()
    df = Transforms(df, param0=drivers[0][['driverId', 'driverName','driverNationality']], param1='driverId', how='left').transform_state()
    df = Transforms(df, param0=constructors[0][['constructorId', 'brand', 'brandNationality']], param1='constructorId', how='left').transform_state()
    df = Transforms(df, param0=status[0], param1='statusId', how='left').transform_state()
    df = Transforms(df, param0=qualifying[0][['raceId', 'driverId','startingPosition']], param1=['raceId', 'driverId'], how='left').transform_state()
    df = Transforms(df, param0=df_pitstop[['raceId', 'driverId','duration']], param1=['raceId', 'driverId'], how='left').transform_state()
    df = df.drop(['number', 'position', 'positionText', 'laps', 'fastestLap','grid'], axis=1)
    df = df.sort_values(by=['year', 'round', 'positionOrder'], ascending=[False, True, True])
    df['driverName'] = df['driverName'].str.replace("'", "", regex=True)
    df.time.replace('\\N',np.nan, inplace=True)
    df.milliseconds.replace('\\N',np.nan, inplace=True)
    df.fastestLapTime.replace('\\N',np.nan, inplace=True)
    df.fastestLapSpeed.replace('\\N',np.nan, inplace=True)
    df.fastestLapSpeed = df.fastestLapSpeed.astype(float)
    df.milliseconds =df.milliseconds.astype(float)
    return df
""")
        


    