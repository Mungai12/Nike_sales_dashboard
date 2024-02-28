"""
> Data source: https://www.kaggle.com/datasets/pavankota2020/nike-sales-dataset

> The objective of the program is to create an interactive dashboard web app on streamlit
 to make it easy to understand the sales of the sportswear company Nike for 2020-2021 f/y.
"""

import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import streamlit.components.v1 as components
import plotly.graph_objects as go

# reading the data from the .xlsx file
df = pd.read_excel('Nike.xlsx')
st.set_page_config(layout='wide')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
image = Image.open('nike_logo.jpg')

col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image(image, width=100)

html_title = """
    <style>
    .title-test {
    font-weight:bold;
    padding:5px;
    border-radius:6px;
    }
    </style>
    <center><h1 class="title-test">Nike Interactive Sales Dashboard (2020-2021)</h1></center>"""
with col2:
    st.markdown(html_title, unsafe_allow_html=True)

col3, col4, col5 = st.columns([0.1, 0.45, 0.45])
with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by:Levi Mungai  \n {box_date}")

with col4:
    fig = px.bar(df, x="Retailer", y="Total Sales", labels={"Total Sales": "Total Sales {$}"},
                 title="Total Sales by Retailer", hover_data=["Total Sales"],
                 template="gridon", height=500)
    st.plotly_chart(fig, use_container_width=True)

_, view1, dwn1, view2, dwn2 = st.columns([0.15, 0.20, 0.20, 0.20, 0.20])
with view1:
    expander = st.expander(" Sales per Retailer")
    data = df[["Retailer", "Total Sales"]].groupby(by="Retailer")["Total Sales"].sum()
    expander.write(data)
with dwn1:
    st.download_button("Download Data", data=data.to_csv().encode("utf-8"),
                       file_name="RetailerSales.csv", mime="text/csv")

df["Month_Year"] = df["Invoice Date"].dt.strftime("%b'%y")
result = df.groupby(by=df["Month_Year"])["Total Sales"].sum().reset_index()

with col5:
    fig1 = px.line(result, x="Month_Year", y="Total Sales", title="Total Sales Over Time",
                   template="gridon")
    st.plotly_chart(fig1, use_container_width=True)

with view2:
    expander = st.expander("Monthly Sales")
    data = result
    expander.write(data)
    with dwn2:
        st.download_button("Download Data", data=result.to_csv().encode("utf-8"),
                           file_name="Monthly Sales.csv", mime="text/csv")

st.divider()

result1 = df.groupby(by="State")[["Units Sold", "Total Sales"]].sum().reset_index()

# Add the units sold as a line chart on a secondary y-axis
fig3 = go.Figure()
fig3.add_trace(go.Bar(x=result1['State'], y=result1['Total Sales'], name='Total Sales'))
fig3.add_trace(go.Scatter(x=result1["State"], y=result1["Units Sold"], mode="lines",
                          name="Units Sold", yaxis='y2'))
fig3.update_layout(
    title="Total units and total sales sold by state",
    xaxis=dict(title='state'),
    yaxis=dict(title="Total Sales", showgrid=True),
    yaxis2=dict(title="Units Sold", overlaying="y", side="right"),
    template="gridon",
    legend=dict(x=1, y=1.1)
)
_, col6 = st.columns([0.1, 1])
with col6:
    st.plotly_chart(fig3, use_container_width=True)

_, view3, dwn3 = st.columns([0.5, 0.45, 0.45])
with view3:
    expander = st.expander("view Data for Sales by Units Sold")
    expander.write(result1)
with dwn3:
    st.download_button("Download Data", data=result1.to_csv().encode("utf-8"),
                       file_name="Sales_by_units_Sold.csv", mime="text/csv")

st.divider()

_, col7 = st.columns([0.1, 1])
treemap = df[["Region", "Retailer", "Total Sales"]].groupby(by=["Region", "Retailer"])[
    "Total Sales"].sum().reset_index()


def format_sales(value):
    if value >= 0:
        return '{:.2f} grand'.format(value / 1000)


treemap["Total Sales (Formatted)"] = treemap["Total Sales"].apply(format_sales)

fig4 = px.treemap(treemap, path=["Region", "Retailer"], values="Total Sales",
                  hover_name="Total Sales (Formatted)",
                  hover_data=["Total Sales (Formatted)"],
                  color='Retailer', height=700, width=600)
fig4.update_traces(textinfo="label+value")

with col7:
    st.subheader(":point_right: Total Sales By Region Treemap")
    st.plotly_chart(fig4, use_container_width=True)

_, view4, dwn4 = st.columns([0.5, 0.45, 0.45])
with view4:
    result2 = df[["Region", "Retailer", "Total Sales"]].groupby(by=["Region", "Retailer"])["Total Sales"].sum()
    expander = st.expander("View data for Total Sales by Region and Retailer")
    expander.write(result2)
with dwn4:
    st.download_button("Download Data", data=result2.to_csv().encode("utf-8"),
                       file_name="Sales by Region.csv", mime="text/csv")

_, view5, dwn5 = st.columns([0.5, 0.45, 0.45])
with view5:
    expander = st.expander("view Sales Raw Data")
    expander.write(df)
    with dwn5:
        st.download_button("Download Raw Data", data=df.to_csv().encode("utf-8"),
                           file_name="SalesRawData.csv", mime='text/csv')
st.divider()

footer_temp = """
<!-- CSS  -->
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" 
type="text/css" rel="stylesheet" media="screen,projection"/>
<link href="static/css/style.css" type="text/css" rel="stylesheet" media="screen,projection"/>
<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.5.0/css/all.css" 
integrity="sha384-B4dIYHKNBt8Bc12p+WXckhzcICo0wtJAoU8YZTY5qE0Id1GSseTk6S+L3BlXeVIU" crossorigin="anonymous">
<footer class="page-footer grey darken-4">
<div class="container" id="aboutapp">
<div class="row">
<div class="col l6 s12">
<h5 class="white-text">Nike Dashboard App</h5>
<h6 class="grey-text text-lighten-4">Levi Mungai's ADS Project.</h6>
</div>
<div class="col l3 s12">
<h5 class="white-text">Connect With Me</h5>
<ul>
<a href="https://www.youtube.com/channel/UCUv0uC9nWNoi7zW4ebWw6eg" target="_blank" class="white-text">
<i class="fab fa-youtube-square fa-4x"></i>
</a>
<a href="https://github.com/" target="_blank" class="white-text">
<i class="fab fa-github-square fa-4x"></i>
</a>
</ul>
</div>
</div>
</div>
<div class="footer-copyright">
<div class="container">
<h5 class="white-text text-lighten-3">Created by: Levi Mungai</h5></a><br/>
"""

st.header("About App")
components.html(footer_temp, height=300)
