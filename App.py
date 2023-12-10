import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import os
import io
import warnings

warnings.filterwarnings('ignore')

path_file = os.getcwd() + '/images/f1_logo.png'
logo = Image.open(path_file)

path_car = os.getcwd() + '/images/image.webp'
car = Image.open(path_car)

path_dashboard_driver_file = os.getcwd() + '/images/Formula-1-Dashboard.png'
dashboard_driver = Image.open(path_dashboard_driver_file)

path_dashboard_team_file = os.getcwd() + '/images/Formula-1-Dashboard-team.png'
dashboard_team = Image.open(path_dashboard_team_file)

st.set_page_config(
    page_title='Formula 1 | Home',
    page_icon=logo,
    layout='wide'
)
st.markdown("""
<div>
  <img src="https://raw.githubusercontent.com/elghallali/my-images/master/Faculty%20Official/fsjest.jpg" title="fsjest" alt="fsjest" width="150" height="150" align="left"/>
  <img src="https://raw.githubusercontent.com/elghallali/my-images/master/Faculty%20Official/uae.png" title="UAE" **alt="UAE" width="150" height="150" align="right"/>
</div>
<br><br>
<br><br>
<br><br>
<div align="center">
  <img src="https://raw.githubusercontent.com/elghallali/my-images/master/Faculty%20Official/logo.png" title="DSDS" alt="DSDS" width="400" height="150"/>
</div>
""",unsafe_allow_html=True)
st.markdown('# <img src="https://raw.githubusercontent.com/elghallali/formula-1-streamlit-app/master/images/f1_logo.png" alt="Formula 1 Logo" width=100/> Formula 1 Application',unsafe_allow_html=True)
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
    st.subheader('Tools')
    tool1,tool2,tool3,tool4,tool5,tool6,tool7,tool8,tool9,tool10,tool11= st.columns(11)
    st.markdown("""
        <style>
            button {
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
            button img {
                position:relative
                padding:5px;
            }
            button:hover {
                background-color: #999999;
            }
            .description {
                display: none;
                text-align: center;
                color: white;
            }
        </style>
        <script>
            function toggleDescription() {
                var description = document.getElementById("python_description");
                description.style.display = description.style.display === "none" ? "block" : "none";
            }
        </script>
    """, unsafe_allow_html=True)
    with tool1:
        st.markdown("""
                    <button id="python" onclick="toggleDescription('python')">
                    <img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/python/python-original-wordmark.svg" alt="" with=80 height=80>
                    </button>
                    
                    """, unsafe_allow_html=True)
    with tool2:
        st.markdown("""
                 <button>
                 <img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/vscode/vscode-original-wordmark.svg" alt="" with=80 height=80>
                 </button>
                 """, unsafe_allow_html=True)
    with tool3:
        st.markdown("""
                 <button>
                 <img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/git/git-original-wordmark.svg" alt="" with=80 height=80>
                 </button>
                 """, unsafe_allow_html=True)
    with tool4:
        st.markdown("""
                 <button>
                 <img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/docker/docker-plain-wordmark.svg" alt="" with=80 height=80>
                 </button>
                 """, unsafe_allow_html=True)
    with tool5:
        st.markdown("""
                 <button>
                 <img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/numpy/numpy-original-wordmark.svg" alt="" with=80 height=80>
                 </button>
                 """, unsafe_allow_html=True)
    with tool6:
        st.markdown("""
                 <button>
                 <img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/pandas/pandas-original-wordmark.svg" alt="" with=80 height=80>
                 </button>
                 """, unsafe_allow_html=True)
    with tool7:
        st.markdown("""
                 <button>
                 <img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/github/github-original-wordmark.svg" alt="" with=80 height=80>
                 </button>
                 """, unsafe_allow_html=True)
    with tool8:
        st.markdown("""
                 <button>
                 <img src="https://raw.githubusercontent.com/elghallali/my-images/aff6e3ea2f3f31483187856b7c9d412852c9205c/streamlit-logo-primary-colormark-darktext.svg" alt="" with=80 height=60>
                 </button>
                 """, unsafe_allow_html=True)
    with tool9:
        st.markdown("""
                 <button>
                 <img src="https://camo.githubusercontent.com/20db5efd6873b071b1c72818028df47ce86c511d7560e789c34ba1811593c3eb/68747470733a2f2f73746f72652d696d616765732e732d6d6963726f736f66742e636f6d2f696d6167652f617070732e33363836382e62666230653265652d626539652d346337332d383037662d6530613762383035623162652e37313261666635642d353830302d343765302d393762652d3538643137616461336662382e61343638343565362d636539342d343463662d383932622d353436333763366663663036" alt="" with=80 height=80>
                 </button>
                 """, unsafe_allow_html=True)
    with tool10:
        st.markdown("""
                 <button>
                 <img src="https://raw.githubusercontent.com/elghallali/my-images/aff6e3ea2f3f31483187856b7c9d412852c9205c/GitHub%20Actions.svg" alt="" with=80 height=80>
                 </button>
                 """, unsafe_allow_html=True)
    with tool11:
        st.markdown("""
                 <button>
                 <img src="https://camo.githubusercontent.com/9f56ecb12a5b746c29c31e08e91a1f3cf483f8a3657118be1530cf8c3ae674a2/68747470733a2f2f6475636b64622e6f72672f696d616765732f6c6f676f2d646c2f4475636b44425f4c6f676f2d737461636b65642e737667" alt="" with=80 height=60>
                 </button>
                 """, unsafe_allow_html=True)

    st.subheader('Dataset')

    st.subheader('Dashboard')

    dashboard1,dashboard2 = st.columns(2)
    with dashboard1:
        st.image(dashboard_driver)
    with dashboard2:
        st.image(dashboard_team)
