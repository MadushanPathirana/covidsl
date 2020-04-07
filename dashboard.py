from scipy.integrate import odeint as od
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

def main():
    st.title('Covid-19 SIR Model')
    days=st.slider('Select no. of days :',0,100,1,1)
    Istart=st.slider('Intially infected pop % :',.01,1.0,.01,.01)
    trans_rate=st.slider('Transfer rate :',0,10,1,1)
    reco_rate=st.slider('Recovery rate :',0.0,1.0,0.1,0.01)
    df = corona(Istart,trans_rate,reco_rate,100,days)

    df_melt=pd.melt(df,id_vars='Days',value_vars=['Suspect','Infected','Recovered'],var_name='Legend',value_name='% of Population')
    st.altair_chart(alt.layer(
        Charts(df_melt,'Infected','darkred'),
        Charts(df_melt,'Suspect','darkblue'),
        Charts(df_melt,'Recovered','darkgreen')).encode(
                alt.Stroke(
                'clm:N',scale=alt.Scale(domainMid=1,domain=['Infected','Suspect','Recoverd'],
                                range=['darkred','darkblue','darkgreen'] ))))

def corona(Istart,trans_rate,reco_rate,population,days):
    Sstart=1-Istart
    Rstart=0
    t=np.linspace(1,days,days)
    
    
    def sol(c,t):
        s,i,r=c
        S=-s*i*trans_rate
        I=trans_rate*s*i-reco_rate*i
        R=reco_rate*i
        
        return [S,I,R]
    
   # def new_cases(y,p,d):
   #     y_=np.diff(y,1)*p
   #     y_[y_<0]=0
   #     x_=np.linspace(1,d-1,d-1)
   #     return x_,y_
    
    Sol=od(sol,[Sstart,Istart,Rstart],t)
    
    df=pd.DataFrame({'Days':np.arange(days),'Suspect':Sol[:,0],'Infected':Sol[:,1],'Recovered':Sol[:,2]})
    
    return df
    #Suspect  = Sol[:,0]
    #Infected = Sol[:,1]
    #Recoverd = Sol[:,2]

#pop=st.slider('Select no. of days :',0,1000,1,1)



def Charts(df,clm,C):
    chart=alt.Chart(df[df.Legend==clm]).mark_area(line={'color':C},
        color=alt.Gradient(    gradient='linear',
        stops=[alt.GradientStop(color='white', offset=.01),
               alt.GradientStop(color=C, offset=1)] ,
        x1=1,
        x2=1,
        y1=1,
        y2=0)
        ).encode(
        x='Days',
        y='% of Population:Q',
        
        tooltip='% of Population',
        opacity=alt.value(.5)).properties(
        height=300,
        width=730).interactive()
    return chart 

#chart_dic={'Infected':'red','Suspect':'blue','Recovered':'green'}


if __name__ == "__main__":
    main()



