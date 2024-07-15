import streamlit as st
import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io



### Config
st.set_page_config(
    page_title="GetAround",
    page_icon=":blue_car:",
    layout="wide"
)

## IMPORT DATASET
@st.cache_data()
def load_data():
  data = pd.read_excel("get_around_delay_analysis.xlsx")
  return data

data = load_data()


# ----------------------------------


# Findind number of unique cars
number_of_cars = len(data['car_id'].unique())


# Finding number of rentals
number_of_rentals = data.shape[0]

# Add one feututes that shows there is a delay or not 
data['delay']=data['delay_at_checkout_in_minutes'].apply(lambda x : 'Late' if x >0 else 'On-time')

# Define a dataframe that shows for each car , the previous car had delay or not
data['previous_delay']='None'
df =data[data['previous_ended_rental_id'].notnull()]
df= df.dropna(axis = 0).reset_index(drop=True)


data2=data[data['state']=='canceled']
df2 =data2[data2['previous_ended_rental_id'].notnull()]

y=[]
delta=[*range(0,750,30)]
for x in delta:
  y.append(100-100*len(df2[df2['time_delta_with_previous_rental_in_minutes']>x])/len(df2))
  


for i in range(len(df)):
  previous_id_index=data.index[data['rental_id']==df.loc[i,'previous_ended_rental_id']].tolist()
  df['previous_delay'][i]= data.loc[previous_id_index[0],'delay']
  

# Removing NaN values about late checkout from the dataset
data_without_nan = data[data["delay_at_checkout_in_minutes"].isna() == False]
print (f"There are {data_without_nan.shape[0]} rentals in the dataset 'data_delay_without_nan'")





def main():

    pages = {
        'A propos du projet': project,
        'Analyse exploratoire des données': analysis,
        'Résultats': results,
        }

    if "page" not in st.session_state:
        st.session_state.update({
        # Default page
        'page': 'Projet'
        })

    with st.sidebar:
        page = st.selectbox("Menu", tuple(pages.keys()))
    pages[page]()
    
def project():
    
    ### TITLE AND TEXT
    st.title("Tableau GetAround")

    st.write('\n')
    st.write('\n')
    'Fait par Clément Mouton'
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    "GetAround est l'Airbnb des voitures. Vous pouvez louer des voitures auprès de n'importe quelle personne pour quelques heures à quelques jours ! Fondée en 2009, cette entreprise a connu une croissance rapide. En 2019, elle compte plus de 5 millions d'utilisateurs et environ 20 000 voitures disponibles dans le monde entier. En tant que partenaire de Jedha, ils ont proposé ce formidable défi :"
    st.title("Contexte:")
    "Lors de la location d'une voiture, nos utilisateurs doivent compléter un processus de check-in au début de la location et un processus de check-out à la fin de la location afin de :"
    "Évaluer l'état de la voiture et notifier les autres parties des dommages préexistants ou des dommages survenus pendant la location. Comparer les niveaux de carburant. Mesurer le nombre de kilomètres parcourus."
    "Le check-in et le check-out de nos locations peuvent être effectués selon trois flux distincts :"
    "📱 Contrat de location mobile sur les applications natives : le conducteur et le propriétaire se rencontrent et signent tous les deux le contrat de location sur le smartphone du propriétaire. "
    "📲 Connect : le conducteur ne rencontre pas le propriétaire et ouvre la voiture avec son smartphone."
    "📝 Contrat papier (négligeable)"
    st.write('\n')
    st.write('\n')

    st.title("Projet 🚧:")

    "Pour cette étude de cas, nous vous suggérons de vous mettre à notre place et de réaliser une analyse que nous avons effectuée en 2017 🔮"
    "Lors de l'utilisation de Getaround, les conducteurs réservent des voitures pour une période spécifique, allant d'une heure à quelques jours. Ils sont censés ramener la voiture à l'heure, mais il arrive de temps en temps que les conducteurs soient en retard pour le check-out."
    "Les retards lors du check-out peuvent générer une forte friction pour le prochain conducteur si la voiture devait être louée à nouveau le même jour : Le service client rapporte souvent des utilisateurs insatisfaits parce qu'ils ont dû attendre que la voiture revienne de la location précédente ou des utilisateurs qui ont même dû annuler leur location parce que la voiture n'a pas été rendue à temps."
    st.title("Objectifs 🎯:")
    "Pour atténuer ces problèmes, nous avons décidé de mettre en place un délai minimum entre deux locations. Une voiture ne sera pas affichée dans les résultats de recherche si les heures de check-in ou de check-out demandées sont trop proches d'une location déjà réservée."
    "Cette mesure résout le problème des retards au check-out, mais peut également nuire aux revenus de Getaround/propriétaires : nous devons trouver le bon compromis."
    "* Seuil : combien de temps devrait durer le délai minimum ?"
    "* Portée : devons-nous activer cette fonctionnalité pour toutes les voitures ? seulement les voitures Connect ?"
    "Pour les aider à prendre la bonne décision, ils vous demandent des informations basées sur les données. Voici les premières analyses auxquelles ils ont pensé, pour lancer la discussion. N'hésitez pas à effectuer des analyses supplémentaires que vous jugez pertinentes."
    "* Quelle part des revenus de nos propriétaires serait potentiellement affectée par cette fonctionnalité ? Combien de locations seraient affectées par cette fonctionnalité en fonction du seuil et de la portée que nous choisissons ?"
    "* À quelle fréquence les conducteurs sont-ils en retard pour le prochain check-in ? Comment cela impacte-t-il le prochain conducteur ?"
    "* Combien de cas problématiques cela résoudra-t-il en fonction du seuil et de la portée choisis ?"


    st.write('\n')
    st.write('\n')
    st.write('\n')
    # Data exploration with some informations about the dataset
    st.subheader("Dataset")

    # Look the data
    nrows_data = st.slider('Sélectionner le nombre de lignes à afficher', min_value=1, max_value=200) # Getting the input.
    data_rows = data.head(nrows_data) # Filtering the dataframe.

    st.dataframe(data_rows) # Displaying the dataframe.
    
    st.write (f"Il y a {number_of_cars} différentes voitures dans le dataset.")
    
    # infos
    st.subheader("Types de data et valeurs manquantes")
    buffer = io.StringIO()
    data.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)
    st.write('\n')
    st.write('\n')
    
   

def analysis():


    st.markdown("<h1 style='text-align: center;'>EDA et Data visualisation</h1>", unsafe_allow_html=True)
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    col1, col2 = st.columns(2)

    with col1 : 
        # pie chart 1
        st.write('\n')
        st.subheader('Proportion des types de check-in')
        fig = px.pie(data,names='checkin_type')
        st.plotly_chart(fig  , use_container_width=True)

    with col2 : 
        # pie chart 2
        st.write('\n')
        st.subheader('Proportion de statuts')
        fig = px.pie(data,names='state')
        st.plotly_chart(fig  , use_container_width=True)

    st.write('\n')
    st.write('\n')

   

    # Late checkouts proportions
    st.subheader('Proportion de retard par rapport à ceux dans les temps')
    st.write('\n')

    fig = px.pie(data, names='delay',hole=0.33)
    st.plotly_chart(fig , use_container_width=True)
    

    

    st.write('\n')


    st.subheader('Y a-t-il une relation significative entre la méthode de check-in et le statut ?')

    fig = px.histogram(data, x = "state",
                   color = 'checkin_type',
                   barmode ='group',
                   width= 800,
                   height = 600,
                   histnorm = 'percent',
                   text_auto = True
                  )       
    fig.update_traces(textposition = 'outside', textfont_size = 15)
    fig.update_layout(title_x = 0.5,
                  margin=dict(l=50,r=50,b=50,t=50,pad=4),
                  yaxis = {'visible': False}, 
                  xaxis = {'visible': True}, 
                  xaxis_title = ' ')
    fig.update_xaxes(tickfont_size=15)                     
    st.plotly_chart(fig )

    st.write('\n')
    st.write("Bien que le pourcentage plus élevé de commandes annulées soit lié au type de vérification connecté, cette différence n'est pas significative.\n")


    st.subheader('Y a-t-il une relation significative entre le retard du voyage précédent et le retard de ce voyage ?')
    st.write("Pour comprendre cette question, nous devrions ajouter une autre colonne au dataframe, qui indiquera si la voiture a été en retard précédemment ou non, en fonction de l'ID de la location précédente.")
    df_top= df.head(5) 
    st.dataframe(df_top) # Displaying the dataframe.
    
    st.write('\n')
    fig = px.histogram(df, x = "delay",
                   color = 'previous_delay',
                   barmode ='group',
                   width= 1000,
                   height = 600,
                   histnorm = 'percent',
                   text_auto = True
                  ) 
    st.plotly_chart(fig )  

    st.write("Lorsque la voiture précédente est à l'heure, il peut y avoir une probabilité de 50-50 que la prochaine voiture soit en retard. En revanche, lorsque la voiture précédente est en retard, la probabilité que la voiture suivante soit également en retard augmente, bien que cette augmentation ne soit pas significative.\n")
    st.write('\n')
    st.subheader("Histogramme des retards au check-out en minutes")
    fig = px.histogram(data[data['delay_at_checkout_in_minutes']>0],
                    x ='delay_at_checkout_in_minutes',
                    range_x = [0,1440],
                    nbins=7200
                    )
    st.plotly_chart(fig )
                    
 
    
def results():
    st.markdown("<h1 style='text-align: center;'>Results:</h1>", unsafe_allow_html=True)
    st.write('\n')
    st.write('\n')

    st.subheader("L'effet de la période de location de la voiture sur l'heure de livraison de la voiture précédente")
    st.write(f"Pour cette revue, nous devons examiner uniquement les données d'annulation. Sur l'ensemble des données, {len(data2)} conducteurs ont annulé leur trajet.\n")
    st.write(f"Sur ces {len(data2)}, il y en a {len(df2)} pour lesquels nous avons des informations sur l'ID de la location précédente terminée.\n")


    st.write("Nous voulons vérifier comment la différence de temps entre deux locations de voitures affecte l'annulation de la commande. Par exemple, si l'intervalle de temps entre la restitution de la voiture précédente et la location de la nouvelle voiture est de 60 minutes, le pourcentage d'annulations pourrait être réduit. Il est clair que plus l'intervalle de temps est long, plus le pourcentage d'annulations est faible.\n")
    delta = st.select_slider(
    'Sélectionnez un intervalle de temps',
    options=[*range(0,750,30)])
    x=delta
    z=100-100*len(df2[df2['time_delta_with_previous_rental_in_minutes']>x])/len(df2)

    st.write(f"Si l'intervalle de temps entre la restitution de la voiture précédente et la location de la nouvelle voiture est de {delta} minutes,\n")
    st.write(f"le pourcentage d'annulations pourrait potentiellement diminuer de {z} %." )
    st.write('\n')

    



    


if __name__ == "__main__":
    main()