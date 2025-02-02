    #import Parts
import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image



#Sql Connection
mydb=psycopg2.connect(host="localhost",
                    user="postgres",
                    port="5432",
                    database="Phonepe_data",
                    password="MySQL")
cursor=mydb.cursor()

#aggre_insurance_df
cursor.execute("select*from aggregated_insurance")
mydb.commit()
table1=cursor.fetchall()

Aggre_insurance=pd.DataFrame(table1,columns=("States","Years","Quarter","Transaction_type",
                                             "Transaction_count","Transaction_amount"))


#aggre_transaction_df
cursor.execute("select*from aggregated_transaction")
mydb.commit()
table2=cursor.fetchall()
Aggre_transaction=pd.DataFrame(table2,columns=("States","Years","Quarter","Transaction_type",
                                             "Transaction_count","Transaction_amount"))


#aggre_user_df
cursor.execute("select*from aggregated_user")
mydb.commit()
table3=cursor.fetchall()

Aggre_user=pd.DataFrame(table3,columns=("States","Years","Quarter","Brands",
                                             "Transaction_count","Percentage"))



#map_insurance_df
cursor.execute("select*from map_insurance")
mydb.commit()
table4=cursor.fetchall()

Map_insurance=pd.DataFrame(table4,columns=("States","Years","Quarter","Districts",
                                             "Transaction_count","Transaction_amount"))



#map_transaction_df
cursor.execute("select*from map_transaction")
mydb.commit()
table5=cursor.fetchall()

Map_transaction=pd.DataFrame(table5,columns=("States","Years","Quarter","Districts",
                                             "Transaction_count","Transaction_amount"))



#map_user_df
cursor.execute("select*from map_user")
mydb.commit()
table6=cursor.fetchall()

Map_user=pd.DataFrame(table6,columns=("States","Years","Quarter","Districts",
                                             "RegisteredUsers","AppOpens"))



#top_insurance_df
cursor.execute("select*from top_insurance")
mydb.commit()
table7=cursor.fetchall()

Top_insurance=pd.DataFrame(table7,columns=("States","Years","Quarter","Pincodes",
                                             "Transaction_count","Transaction_amount"))



#top_transaction_df
cursor.execute("select*from top_transaction")
mydb.commit()
table8=cursor.fetchall()

Top_transaction=pd.DataFrame(table8,columns=("States","Years","Quarter","Pincodes",
                                             "Transaction_count","Transaction_amount"))





#top_user_df
cursor.execute("select*from top_user")
mydb.commit()
table9=cursor.fetchall()

Top_user=pd.DataFrame(table9,columns=("States","Years","Quarter","Pincodes",
                                             "RegisteredUsers"))

def Transaction_amount_count_Y(df,year):
    tacy=df[df["Years"]==year]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(tacyg,x="States",y="Transaction_amount",title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=650,width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_amount=px.bar(tacyg,x="States",y="Transaction_count",title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(fig_amount)

    col1,col2=st.columns(2)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()

        fig_india_1=px.choropleth(tacyg,geojson=data1,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name="States",title=f"{year} TRANSACTION AMOUNT",fitbounds="locations",
                                height=600,width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2=px.choropleth(tacyg,geojson=data1,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name="States",title=f"{year} TRANSACTION COUNT",fitbounds="locations",
                                height=600,width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy 

def Transaction_amount_count_Y_Q(df,quarter):
    tacy=df[df["Quarter"]==quarter]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(tacyg,x="States",y="Transaction_amount",title=f"{tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered,height=650,width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count=px.bar(tacyg,x="States",y="Transaction_count",title=f"{tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(fig_count)


    col1,col2=st.columns(2)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()

        fig_india_1=px.choropleth(tacyg,geojson=data1,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name="States",title=f"{tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",fitbounds="locations",
                                height=600,width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2=px.choropleth(tacyg,geojson=data1,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name="States",title=f"{tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",fitbounds="locations",
                                height=600,width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy



def Aggre_Tran_Transaction_type(df,state):

    tacy=df[df["States"]==state]
    tacy.reset_index(drop=True,inplace=True)


    tacyg=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_pie_1=px.pie(data_frame=tacyg,names="Transaction_type",values="Transaction_amount",
                        width=600,title=f"{state.upper()} TRANSACTION AMOUNT",hole=0.5)
        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2=px.pie(data_frame=tacyg,names="Transaction_type",values="Transaction_count",
                        width=600,title=f"{state.upper()} TRANSACTION COUNT",hole=0.5)
        st.plotly_chart(fig_pie_2)



#Aggre_User_Analysis_1
def Aggre_user_plot_1(df,year):
    aguy=df[df["Years"]==year]
    aguy.reset_index(drop=True,inplace=True)

    aguyg=pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyg,x="Brands",y="Transaction_count",title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000,color_discrete_sequence=px.colors.sequential.Cividis_r,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguy


#Aggre_User_Analysis_2
def Aggre_user_plot_2(df,quarter):
    aguyq=df[df["Quarter"]==quarter]
    aguyq.reset_index(drop=True,inplace=True)

    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyqg,x="Brands",y="Transaction_count",title=f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                        width=1000,color_discrete_sequence=px.colors.sequential.Oranges_r,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq



#Aggre_User_Analysis_3
def Aggre_user_plot_3(df,state):
    auyqs=df[df["States"]==state]
    auyqs.reset_index(drop=True,inplace=True)

    fig_line_1=px.line(auyqs,x="Brands",y="Transaction_count",hover_data="Percentage",
                    title="BRANDS, TRANSACTION COUNT, PERCENTAGE",width=1000,markers=True,)
    st.plotly_chart(fig_line_1)




#Map_insurance_districts
def Map_insur_District(df,state):

    tacy=df[df["States"]==state]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_bar_1=px.bar(data_frame=tacyg,x="Transaction_amount",y="Districts",orientation="h",height=600,
                        title=f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2=px.bar(data_frame=tacyg,x="Transaction_count",y="Districts",orientation="h",height=600,
                        title=f"{state.upper()} DISTRICT AND TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_2)


#Map_user_plot_1
def map_user_plot_1(df,year):

    muy=Map_user[Map_user["Years"]==year]
    muy.reset_index(drop=True,inplace=True)

    muyg=muy.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    muyg.reset_index(inplace=True)

    fig_line_1=px.line(muyg,x="States",y=["RegisteredUsers","AppOpens"],
                        title=f"{year} REGISTEREDUSER, APPOPENS", width=1000,height=800,markers=True)
    st.plotly_chart(fig_line_1)

    return muy



#Map_user_plot_2
def map_user_plot_2(df,quarter):

    muyq=df[df["Quarter"]==quarter]
    muyq.reset_index(drop=True,inplace=True)

    muyqg=muyq.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    muyqg.reset_index(inplace=True)

    fig_line_1=px.line(muyqg,x="States",y=["RegisteredUsers","AppOpens"],
                        title=f"{df['Years'].min()} YEAR {quarter} QUARTER REGISTEREDUSER, APPOPENS", width=1000,height=800,markers=True,
                        color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return muyq


#Map_User_Plot_3
def map_user_plot_3(df,states):
    muyqs=df[df["States"]==states]
    muyqs.reset_index(drop=True,inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_map_user_bar_1=px.bar(muyqs,x="RegisteredUsers",y="Districts",orientation="h",
                                title=f"{states.upper()} REGISTERED USER",height=800,color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:
        fig_map_user_bar_2=px.bar(muyqs,x="AppOpens",y="Districts",orientation="h",
                                title=f"{states.upper()} APPOPENS",height=800,color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_2)


#Top_insurance_Plot_1
def Top_insurance_plot_1(df,state):
    tiy=df[df["States"]==state]
    tiy.reset_index(drop=True,inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_top_insur_bar_1=px.bar(tiy,x="Quarter",y="Transaction_amount",hover_data="Pincodes",
                                    title="TRANSACTION AMOUNT",height=650,width=500,color_discrete_sequence=px.colors.sequential.Sunsetdark_r)
        st.plotly_chart(fig_top_insur_bar_1)

    with col2:
        fig_top_insur_bar_2=px.bar(tiy,x="Quarter",y="Transaction_count",hover_data="Pincodes",
                                    title="TRANSACTION COUNT",height=650,width=500,color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_top_insur_bar_2)


#Top_user_Analysis
def top_user_plot_1(df,year):
    tuy=df[df["Years"]==year]
    tuy.reset_index(drop=True,inplace=True)

    tuyg=pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)

    fig_top_plot_1=px.bar(tuyg,x="States",y="RegisteredUsers", color="Quarter",width=1000,height=800,
                        color_discrete_sequence=px.colors.sequential.Darkmint_r,hover_name="States",
                        title=f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy


#Top_user_plot_2
def top_user_plot_2(df,state):
    tuys=df[df["States"]==state]
    tuys.reset_index(drop=True,inplace=True)

    fig_top_plot_2=px.bar(tuys,x="Quarter",y="RegisteredUsers",title="REGISTEREDUSERS, PINCODES, QUARTER",
                        width=1000,height=800,color="RegisteredUsers",hover_data="Pincodes",
                        color_continuous_scale=px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)


#answer for query(transaction_amount)
def top_chart_transaction_amount(table_name):
        #Sql Connection
        mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="Phonepe_data",
                        password="MySQL")
        cursor=mydb.cursor()


        #Plot_1
        query1=f'''SELECT states, sum(transaction_amount) as transaction_amount
                from {table_name}
                group by states
                order by transaction_amount desc
                limit 10;'''

        cursor.execute(query1)
        table_1=cursor.fetchall()

        col1,col2=st.columns(2)
        with col1:
            df_1=pd.DataFrame(table_1,columns=("states","transaction_amount"))
            fig_amount=px.bar(df_1,x="states",y="transaction_amount",title="TOP 10 OF TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered,height=650,width=550,hover_name="states")
            st.plotly_chart(fig_amount)


        #Plot_2
        query2=f'''SELECT states, sum(transaction_amount) as transaction_amount
                from {table_name}
                group by states
                order by transaction_amount 
                limit 10;'''

        cursor.execute(query2)
        table_2=cursor.fetchall()

        with col2:
            df_2=pd.DataFrame(table_2,columns=("states","transaction_amount"))
            fig_amount_2=px.bar(df_2,x="states",y="transaction_amount",title="LAST 10 OF TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=550,hover_name="states")
            st.plotly_chart(fig_amount_2)


        #Plot_3
        query3=f'''select states, avg(transaction_amount) as transaction_amount
                from {table_name}
                group by states
                order by transaction_amount;'''

        cursor.execute(query3)
        table_3=cursor.fetchall()

        df_3=pd.DataFrame(table_3,columns=("states","transaction_amount"))

        fig_amount_3=px.bar(df_3,x="states",y="transaction_amount",title="AVERAGE OF TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Blackbody,height=700,width=600,hover_name="states")
        st.plotly_chart(fig_amount_3)



#answer for query(transaction_count)
def top_chart_transaction_count(table_name):
        #Sql Connection
        mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="Phonepe_data",
                        password="MySQL")
        cursor=mydb.cursor()


        #Plot_1
        query1=f'''SELECT states, sum(transaction_count) as transaction_count
                from {table_name}
                group by states
                order by transaction_count desc
                limit 10;'''

        cursor.execute(query1)
        table_1=cursor.fetchall()

        col1,col2=st.columns(2)
        with col1:
            df_1=pd.DataFrame(table_1,columns=("states","transaction_count"))
            fig_amount=px.bar(df_1,x="states",y="transaction_count",title="TOP 10 OF TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered,height=650,width=600,hover_name="states")
            st.plotly_chart(fig_amount)


        #Plot_2
        query2=f'''SELECT states, sum(transaction_count) as transaction_count
                from {table_name}
                group by states
                order by transaction_count 
                limit 10;'''

        cursor.execute(query2)
        table_2=cursor.fetchall()

        with col2:
            df_2=pd.DataFrame(table_2,columns=("states","transaction_count"))
            fig_amount_2=px.bar(df_2,x="states",y="transaction_count",title="LAST 10 OF TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600,hover_name="states")
            st.plotly_chart(fig_amount_2)


        #Plot_3
        query3=f'''select states, avg(transaction_count) as transaction_count
                from {table_name}
                group by states
                order by transaction_count;'''

        cursor.execute(query3)
        table_3=cursor.fetchall()

        
        df_3=pd.DataFrame(table_3,columns=("states","transaction_count"))

        fig_amount_3=px.bar(df_3,x="states",y="transaction_count",title="AVERAGE OF TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Blackbody,height=650,width=600,hover_name="states")
        st.plotly_chart(fig_amount_3)


#answer for query(registered_user)
def top_chart_registered_user(table_name,state):
        #Sql Connection
        mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="Phonepe_data",
                        password="MySQL")
        cursor=mydb.cursor()


        #Plot_1
        query1=f'''select districts, sum(registeredusers) as registeredusers
                    from {table_name}
                    where states='{state}'
                    group by districts
                    order by registeredusers desc
                    limit 10;'''

        cursor.execute(query1)
        table_1=cursor.fetchall()

        col1,col2=st.columns(2)
        with col1:
            df_1=pd.DataFrame(table_1,columns=("districts","registeredusers"))
            fig_amount=px.bar(df_1,x="districts",y="registeredusers",title="TOP 10 OF REGISTERED USER",
                            color_discrete_sequence=px.colors.sequential.Bluered,height=650,width=600,hover_name="districts")
            st.plotly_chart(fig_amount)


        #Plot_2
        query2=f'''select districts, sum(registeredusers) as registeredusers
                    from {table_name}
                    where states='{state}'
                    group by districts
                    order by registeredusers 
                    limit 10;'''

        cursor.execute(query2)
        table_2=cursor.fetchall()

        with col2:
            df_2=pd.DataFrame(table_2,columns=("districts","registeredusers"))
            fig_amount_2=px.bar(df_2,x="districts",y="registeredusers",title="LAST 10 OF REGISTERED USER",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600,hover_name="districts")
            st.plotly_chart(fig_amount_2)


        #Plot_3
        query3=f'''select districts, avg(registeredusers) as registeredusers
                    from {table_name}
                    where states='{state}'
                    group by districts
                    order by registeredusers;'''

        cursor.execute(query3)
        table_3=cursor.fetchall()

        df_3=pd.DataFrame(table_3,columns=("districts","registeredusers"))

        fig_amount_3=px.bar(df_3,x="districts",y="registeredusers",title="AVERAGE OF REGISTERED USER",
                        color_discrete_sequence=px.colors.sequential.Blackbody,height=650,width=600,hover_name="districts")
        st.plotly_chart(fig_amount_3)


#answer for query(appopens)
def top_chart_appopens(table_name,state):
        #Sql Connection
        mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="Phonepe_data",
                        password="MySQL")
        cursor=mydb.cursor()


        #Plot_1
        query1=f'''select districts, sum(appopens) as appopens
                    from {table_name}
                    where states='{state}'
                    group by districts
                    order by appopens desc
                    limit 10;'''

        cursor.execute(query1)
        table_1=cursor.fetchall()

        col1,col2=st.columns(2)
        with col1:
            df_1=pd.DataFrame(table_1,columns=("districts","appopens"))
            fig_amount=px.bar(df_1,x="districts",y="appopens",title="TOP 10 OF APPOPENS",
                            color_discrete_sequence=px.colors.sequential.Bluered,height=650,width=600,hover_name="districts")
            st.plotly_chart(fig_amount)


        #Plot_2
        query2=f'''select districts, sum(appopens) as appopens
                    from {table_name}
                    where states='{state}'
                    group by districts
                    order by appopens 
                    limit 10;'''

        cursor.execute(query2)
        table_2=cursor.fetchall()

        with col2:
            df_2=pd.DataFrame(table_2,columns=("districts","appopens"))
            fig_amount_2=px.bar(df_2,x="districts",y="appopens",title="LAST 10 OF APPOPENS",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600,hover_name="districts")
            st.plotly_chart(fig_amount_2)


        #Plot_3
        query3=f'''select districts, avg(appopens) as appopens
                    from {table_name}
                    where states='{state}'
                    group by districts
                    order by appopens;'''

        cursor.execute(query3)
        table_3=cursor.fetchall()

        df_3=pd.DataFrame(table_3,columns=("districts","appopens"))

        fig_amount_3=px.bar(df_3,x="districts",y="appopens",title="AVERAGE OF APPOPENS",
                        color_discrete_sequence=px.colors.sequential.Blackbody,height=650,width=600,hover_name="districts")
        st.plotly_chart(fig_amount_3)


#answer for query(registered_users)#2
def top_chart_registered_users(table_name):
        #Sql Connection
        mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="Phonepe_data",
                        password="MySQL")
        cursor=mydb.cursor()


        #Plot_1
        query1=f'''select states, sum(registeredusers)as registeredusers
                    from {table_name}
                    group by states
                    order by registeredusers desc
                    limit 10;'''

        cursor.execute(query1)
        table_1=cursor.fetchall()

        col1,col2=st.columns(2)
        with col1:
            df_1=pd.DataFrame(table_1,columns=("states","registeredusers"))
            fig_amount=px.bar(df_1,x="states",y="registeredusers",title="TOP 10 OF REGISTERED USERS",
                            color_discrete_sequence=px.colors.sequential.Bluered,height=650,width=600,hover_name="states")
            st.plotly_chart(fig_amount)


        #Plot_2
        query2=f'''select states, sum(registeredusers)as registeredusers
                    from {table_name}
                    group by states
                    order by registeredusers 
                    limit 10;'''

        cursor.execute(query2)
        table_2=cursor.fetchall()

        with col2:
            df_2=pd.DataFrame(table_2,columns=("states","registeredusers"))
            fig_amount_2=px.bar(df_2,x="states",y="registeredusers",title="LAST 10 OF REGISTERED USERS",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600,hover_name="states")
            st.plotly_chart(fig_amount_2)



        #Plot_3
        query3=f'''select states, avg(registeredusers)as registeredusers
                    from {table_name}
                    group by states
                    order by registeredusers;'''

        cursor.execute(query3)
        table_3=cursor.fetchall()

        df_3=pd.DataFrame(table_3,columns=("states","registeredusers"))

        fig_amount_3=px.bar(df_3,x="states",y="registeredusers",title="AVERAGE OF REGISTERED USERS",
                        color_discrete_sequence=px.colors.sequential.Blackbody,height=650,width=600,hover_name="states")
        st.plotly_chart(fig_amount_3)




#######   Streamlit Part   ########


st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    select =option_menu("Main Menu", ["HOME", "DATA EXPLORATION", "TOP CHARTS"])

if select == "HOME":
    col1,col2=st.columns(2)
    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("Phonepe is an Indian digital payments and financial technology company")
        st.write("FEATURES")
        st.write("- Credit & Debit card linking")
        st.write("- Bank Balance Check")
        st.write("- Money Storage")
        st.write("- PIN Authorization")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.video(r"C:\Users\heera\OneDrive\Desktop\New project\PhonePe Motion Graphics.mp4")

    col3,col4=st.columns(2)
    with col3:
        st.image(r"C:\Users\heera\OneDrive\Desktop\New project\PhonePe-Logo.wine.png",width=500)

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Pyment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")
    
    col5,col6=st.columns(2)
    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly  From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.image(Image.open(r"C:\Users\heera\OneDrive\Desktop\New project\phonepe pay anytime.jpg"),width=400)




elif select=="DATA EXPLORATION":
    tab1,tab2,tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])

    with tab1:
        method=st.radio("Select The Method",["Insurance Analysis","Transaction Analysis","User Analysis"])

        if method=="Insurance Analysis":
            
            col1,col2=st.columns(2)
            with col1:
                min_year = Aggre_insurance["Years"].min()
                max_year = Aggre_insurance["Years"].max()
                if min_year == max_year:
                    max_year += 1
                years = st.slider("Select The Year", min_value=min_year, max_value=max_year, value=min_year)
                #years=st.slider("Select The Year",Aggre_insurance["Years"].min(),Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())
            tac_Y=Transaction_amount_count_Y(Aggre_insurance,years)

            col1,col2=st.columns(2)
            with col1:
                min_quarter = tac_Y["Quarter"].min()
                max_quarter = tac_Y["Quarter"].max()
                if min_quarter == max_quarter:
                    max_quarter += 1
                quarters = st.slider("Select The Quarter", min_value=min_quarter, max_value=max_quarter, value=min_quarter)
                 #quarters=st.slider("Select The Quarter",tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y,quarters)

            
        elif method=="Transaction Analysis":
             
            col1,col2=st.columns(2)
            with col1:
                min_year = Aggre_transaction["Years"].min()
                max_year = Aggre_transaction["Years"].max()
                if min_year == max_year:
                    max_year += 1
                years = st.slider("Select The Year", min_value=min_year, max_value=max_year, value=min_year)
                #years=st.slider("Select The Year",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
            Aggre_tran_tac_Y=Transaction_amount_count_Y(Aggre_transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The States", Aggre_tran_tac_Y["States"].unique())
            
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                min_quarter = Aggre_tran_tac_Y["Quarter"].min()
                max_quarter = Aggre_tran_tac_Y["Quarter"].max()
                if min_quarter == max_quarter:
                    max_quarter += 1
                quarters = st.slider("Select The Quarter", min_value=min_quarter, max_value=max_quarter, value=min_quarter)
                 #quarters=st.slider("Select The Quarter",tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Aggre_tran_tac_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The States_Ty", Aggre_tran_tac_Y_Q["States"].unique())
            
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q,states)

        elif method=="User Analysis":
            col1,col2=st.columns(2)
            with col1:
                min_year = Aggre_user["Years"].min()
                max_year = Aggre_user["Years"].max()
                if min_year == max_year:
                    max_year += 1
                years = st.slider("Select The Year", min_value=min_year, max_value=max_year, value=min_year)
                #years=st.slider("Select The Year",Aggre_user["Years"].min(),Aggre_user["Years"].max(),Aggre_user["Years"].min())
            Aggre_user_Y=Aggre_user_plot_1(Aggre_user,years)

            col1,col2=st.columns(2)
            with col1:
                min_quarter = Aggre_user_Y["Quarter"].min()
                max_quarter = Aggre_user_Y["Quarter"].max()
                if min_quarter == max_quarter:
                    max_quarter += 1
                quarters = st.slider("Select The Quarter", min_value=min_quarter, max_value=max_quarter, value=min_quarter)
                 #quarters=st.slider("Select The Quarter",Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q=Aggre_user_plot_2(Aggre_user_Y,quarters)


            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The States", Aggre_user_Y_Q["States"].unique())
            
            Aggre_user_plot_3(Aggre_user_Y_Q,states)

    with tab2:
        method_2=st.radio("Select The Method",["Map Insurance","Map Transaction","Map User"])

        if method_2=="Map Insurance":
    
            col1,col2=st.columns(2)
            with col1:
                min_year = Map_insurance["Years"].min()
                max_year = Map_insurance["Years"].max()
                if min_year == max_year:
                    max_year += 1
                years = st.slider("Select The Year_MI", min_value=min_year, max_value=max_year, value=min_year)
                #years=st.slider("Select The Year",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
            map_insur_tac_Y=Transaction_amount_count_Y(Map_insurance,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_mi", map_insur_tac_Y["States"].unique())
            
            Map_insur_District(map_insur_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                min_quarter = map_insur_tac_Y["Quarter"].min()
                max_quarter = map_insur_tac_Y["Quarter"].max()
                if min_quarter == max_quarter:
                    max_quarter += 1
                quarters = st.slider("Select The Quarters", min_value=min_quarter, max_value=max_quarter, value=min_quarter)
                 #quarters=st.slider("Select The Quarter",tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            map_insur_tac_Y_Q=Transaction_amount_count_Y_Q(map_insur_tac_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The States_MP", map_insur_tac_Y_Q["States"].unique())
            Map_insur_District(map_insur_tac_Y_Q,states)

        elif method_2=="Map Transaction":
            col1,col2=st.columns(2)
            with col1:
                min_year = Map_transaction["Years"].min()
                max_year = Map_transaction["Years"].max()
                if min_year == max_year:
                    max_year += 1
                years = st.slider("Select The Year_MT", min_value=min_year, max_value=max_year, value=min_year)
                #years=st.slider("Select The Year",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
            Map_tran_tac_Y=Transaction_amount_count_Y(Map_transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_mi", Map_tran_tac_Y["States"].unique())
            
            Map_insur_District(Map_tran_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                min_quarter = Map_tran_tac_Y["Quarter"].min()
                max_quarter = Map_tran_tac_Y["Quarter"].max()
                if min_quarter == max_quarter:
                    max_quarter += 1
                quarters = st.slider("Select The Quarters", min_value=min_quarter, max_value=max_quarter, value=min_quarter)
                 #quarters=st.slider("Select The Quarter",tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            Map_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Map_tran_tac_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The States_MI", Map_tran_tac_Y_Q["States"].unique())
            Map_insur_District(Map_tran_tac_Y_Q,states)

        elif method_2=="Map User":
            col1,col2=st.columns(2)
            with col1:
                min_year = Map_user["Years"].min()
                max_year = Map_user["Years"].max()
                if min_year == max_year:
                    max_year += 1
                years = st.slider("Select The Year_mu", min_value=min_year, max_value=max_year, value=min_year)
                #years=st.slider("Select The Year",Map_user["Years"].min(),Map_user["Years"].max(),Map_user["Years"].min())
            map_user_tac_Y=map_user_plot_1(Map_user,years)

            col1,col2=st.columns(2)
            with col1:
                min_quarter = map_user_tac_Y["Quarter"].min()
                max_quarter = map_user_tac_Y["Quarter"].max()
                if min_quarter == max_quarter:
                    max_quarter += 1
                quarters = st.slider("Select The Quarters_mu", min_value=min_quarter, max_value=max_quarter, value=min_quarter)
                 #quarters=st.slider("Select The Quarter",tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            Map_user_Y_Q=map_user_plot_2(map_user_tac_Y,quarters)


            col1,col2=st.columns(2)
            with col1:
                    states=st.selectbox("Select The States_MU", Map_user_Y_Q["States"].unique())
            map_user_plot_3(Map_user_Y_Q,states)

    with tab3:
        method_3=st.radio("Select The Method",["Top Insurance","Top Transaction","Top User"])

        if method_3=="Top Insurance":
            col1,col2=st.columns(2)
            with col1:
                min_year = Top_insurance["Years"].min()
                max_year = Top_insurance["Years"].max()
                if min_year == max_year:
                    max_year += 1
                years = st.slider("Select The Year_TI", min_value=min_year, max_value=max_year, value=min_year)
                #years=st.slider("Select The Year",Top_insurance["Years"].min(),Top_insurance["Years"].max(),Top_insurance["Years"].min())
            Top_insur_tac_Y=Transaction_amount_count_Y(Top_insurance,years)

            col1,col2=st.columns(2)
            with col1:
                    states=st.selectbox("Select The States_TI", Top_insur_tac_Y["States"].unique())
            Top_insurance_plot_1(Top_insur_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                min_quarter = Top_insur_tac_Y["Quarter"].min()
                max_quarter = Top_insur_tac_Y["Quarter"].max()
                if min_quarter == max_quarter:
                    max_quarter += 1
                quarters = st.slider("Select The Quarters_TI", min_value=min_quarter, max_value=max_quarter, value=min_quarter)
                 #quarters=st.slider("Select The Quarter",Top_insur_tac_Y["Quarter"].min(),Top_insur_tac_Y["Quarter"].max(),Top_insur_tac_Y["Quarter"].min())
            Top_insur_tac_Y_Q=Transaction_amount_count_Y_Q(Top_insur_tac_Y,quarters)

        elif method_3=="Top Transaction":
            col1,col2=st.columns(2)
            with col1:
                min_year = Top_transaction["Years"].min()
                max_year = Top_transaction["Years"].max()
                if min_year == max_year:
                    max_year += 1
                years = st.slider("Select The Year_TT", min_value=min_year, max_value=max_year, value=min_year)
                #years=st.slider("Select The Year",Top_transaction["Years"].min(),Top_transaction["Years"].max(),Top_transaction["Years"].min())
            Top_tran_tac_Y=Transaction_amount_count_Y(Top_transaction,years)

            col1,col2=st.columns(2)
            with col1:
                    states=st.selectbox("Select The States_TT", Top_tran_tac_Y["States"].unique())
            Top_insurance_plot_1(Top_tran_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                min_quarter = Top_tran_tac_Y["Quarter"].min()
                max_quarter = Top_tran_tac_Y["Quarter"].max()
                if min_quarter == max_quarter:
                    max_quarter += 1
                quarters = st.slider("Select The Quarters_TT", min_value=min_quarter, max_value=max_quarter, value=min_quarter)
                 #quarters=st.slider("Select The Quarter",Top_transaction["Quarter"].min(),Top_transaction["Quarter"].max(),Top_transaction["Quarter"].min())
            Top_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Top_tran_tac_Y,quarters)

        elif method_3=="Top User":
            col1,col2=st.columns(2)
            with col1:
                min_year = Top_user["Years"].min()
                max_year = Top_user["Years"].max()
                if min_year == max_year:
                    max_year += 1
                years = st.slider("Select The Year_TU", min_value=min_year, max_value=max_year, value=min_year)
                #years=st.slider("Select The Year",Top_user["Years"].min(),Top_user["Years"].max(),Top_user["Years"].min())
            Top_user_Y=top_user_plot_1(Top_user,years)

            col1,col2=st.columns(2)
            with col1:
                    states=st.selectbox("Select The States_TT", Top_user_Y["States"].unique())
            top_user_plot_2(Top_user_Y,states)

elif select=="TOP CHARTS":
    
    question=st.selectbox("Select the Question",["1. Transaction Amount and Count of Aggregated Insurance",
                                                 "2. Transaction Amount and Count of Map Insurance",
                                                 "3. Transaction Amount and Count of Top Insurance",
                                                 "4. Transaction Amount and Count of Aggregated Transaction",
                                                 "5. Transaction Amount and Count of Map Transaction",
                                                 "6. Transaction Amount and Count of Top Transaction",
                                                 "7. Transaction Count of Aggregated User",
                                                 "8. Registered users of Map User",
                                                 "9. App opens of Map User",
                                                 "10. Registered users of Top User"])
    
    if question=="1. Transaction Amount and Count of Aggregated Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")

    elif question=="2. Transaction Amount and Count of Map Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")

    elif question=="3. Transaction Amount and Count of Top Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")

    elif question=="4. Transaction Amount and Count of Aggregated Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")

    elif question=="5. Transaction Amount and Count of Map Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")

    elif question=="6. Transaction Amount and Count of Top Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")

    elif question=="7. Transaction Count of Aggregated User":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")

    elif question=="8. Registered users of Map User":

        states=st.selectbox("Select the state",Map_user["States"].unique())
        st.subheader("REGISTERED USERS")
        top_chart_registered_user("Map_user", states)


    elif question=="9. App opens of Map User":

        states=st.selectbox("Select the state",Map_user["States"].unique())
        st.subheader("APPOPENS")
        top_chart_appopens("Map_user", states)

    elif question=="10. Registered users of Top User":

        st.subheader("REGISTERED USERS")
        top_chart_registered_users("Top_user")


