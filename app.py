from dotenv import load_dotenv
import os
import streamlit as st


from components.eln_data import ELN
from components.eln_push import LumiEln
from components.lumi_create import LumiCreateExp
from components.lumi_pull import LumiData

from config.lumi_jwt import get_valid_jwt


# hide streamlit style
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)
# background-color: #ed9439;
st.markdown("""
<style>
.navbar {
  height: 80px;
  background-color: #ed9439;
  color: #ed9439;
}
.navbar-brand{
    font-size: 40px;
    margin-left:40px;
}
</style>""", unsafe_allow_html= True)


st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark">
  <a class="navbar-brand" href="#" target="_blank">CatSci</a>
  

</nav>
""", unsafe_allow_html=True)



st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #ed9439;
    color:#0f1b2a;
    border:None;
}
div.stButton > button:first-child:focus {
    background-color: #ed9439;
    color:#0f1b2a;
    border:None;
}
</style>""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .button-primary {
        background-color: #FF5733; /* Change this to your desired color */
        color: white;
    }
    .button-secondary {
        background-color: #FDE74C; /* Change this to your desired color */
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)



import os
from utils.common import read_yaml_file
current_dir = os.path.dirname(__file__)
st.write(f"curr dir {current_dir}")
schema_pth = "Lumi/config/schema.yaml"
SCHEMA_FILE_PATH = os.path.join(current_dir, schema_pth)
st.write(f" schema path {SCHEMA_FILE_PATH}")
a = read_yaml_file(SCHEMA_FILE_PATH)
st.write(a)

# eid = "experiment:b572a4ea-67e4-4333-b34e-bd78a8d3ee3d"
eid = "experiment:7427ab3b-295b-4480-9e66-2797306234bb"


jwt_token = get_valid_jwt(email= st.secrets["email"], password= st.secrets["password"])

# email = os.environ.get("email")
# password = os.environ.get("password")

# jwt_token = get_valid_jwt(email= email, password= password)


def create_pipeline(api, jwt_token):

    e = ELN(eid = eid, api_key= api)
    eln_data = e.initiate_data_extraction()

    lumi = LumiCreateExp(data= eln_data, jwt_token= jwt_token)
    output = lumi.create_experiment()
    return output

def push_pipeline(api, jwt_token):
    lumi_data = LumiData(eid = eid, jwt_token= jwt_token)
    img = lumi_data.get_data()
    st.image(img, caption='Your Image', use_column_width=True)

    le = LumiEln(eid = eid, file= img, api_key= api)
    output = le.send_data_to_eln()
    return output

st.title("ELN-Lumi Connector")
# st.info('Please make sure to upload **all files** !!')


if st.button("Create Experiment in Lumi", key="create_lumi", type="primary"):
    # load_dotenv('.env')
    # api = os.environ.get("SANDBOX_API_KEY")
    api = st.secrets["SANDBOX_API_KEY"]
    # st.write(eid)
    with st.spinner("Creating experiment"):
        output = create_pipeline(api = api, jwt_token= jwt_token)
        if output == "success":
            st.success("Experiment created in Lumi")


if st.button("Send Data from Lumi to ELN", key="pull_lumi", type="secondary"):
    # load_dotenv('.env')
    # api = os.environ.get("SANDBOX_API_KEY")
    api = st.secrets["SANDBOX_API_KEY"]
    # st.write(eid)
    with st.spinner("Uploading data to ELN"):
        output = push_pipeline(api = api, jwt_token= jwt_token)
        st.write(output)
        if output == "success":
            st.success("Data uploaded to ELN")

