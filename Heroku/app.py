import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import helper
import preprocessor

st.set_page_config(page_title='Arjunan K - Project',
                   page_icon=None,
                   layout='wide',
                   initial_sidebar_state='auto')
hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; font-size: 100px; padding-bottom: 10px;'>WhatsApp Chat Digger</h1>",
            unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-size: 18px; padding: 10px;'>Export your WhatsApp group or personal chat and drop here for a detailed analysis.</h3>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-size: 18px; padding-top: 0px; padding-bottom: 40px;'>Made by Arjunan K</h3>", unsafe_allow_html=True)
# st.markdown("<h1 style='text-align: center; font-size: 25px; padding-bottom: 20px;'></h1>", unsafe_allow_html=True)


# st.sidebar.markdown(
#     "<img src='https://pnggrid.com/wp-content/uploads/2021/04/whatsapp-logo-1024x1024.png' width=50/>",
#     unsafe_allow_html=True)
# st.sidebar.title("Steps")

st.sidebar.markdown(
    "Steps<ol><li>Click Download Demo Chat</li> "
    "<li>Click Browse files</li> "
    "<li>Upload the downloaded file</li> "
    "<li>Click Show Analysis</li></ol>",
    unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader("Upload WhatsApp Chat")

with open('WhatsApp Chat.txt', encoding="utf-8") as f:
    st.sidebar.download_button('Download Demo Chat', f, file_name='Demo Whatsapp Chat.txt')

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetch unique user
    user_list = df["user"].unique().tolist()
    user_list.remove('Group Notification')
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show Analysis for users", user_list)

    if st.sidebar.button("Show Analysis"):

        # 4 KPI Metrics
        num_messages, num_words, num_media, num_links = helper.fetch_stats(selected_user, df)
        r1c1, r1c2, r1c3, r1c4 = st.columns(4)

        r1c1fig = go.Figure(go.Indicator(mode="number", value=num_messages, delta={"reference": 512, "valueformat": ".0f"}, title={"text": "TOTAL MESSAGES"}, domain={'y': [0, 1], 'x': [0.25, 0.75]}))
        r1c1fig.update_layout(margin=dict(l=0, r=0, b=0, t=0, pad=4))
        r1c1.plotly_chart(r1c1fig, use_container_width=True)

        r1c2fig = go.Figure(go.Indicator(mode="number", value=num_words, delta={"reference": 512, "valueformat": ".0f"}, title={"text": "TOTAL WORDS"}, domain={'y': [0, 1], 'x': [0.25, 0.75]}))
        r1c2fig.update_layout(margin=dict(l=0, r=0, b=0, t=0, pad=4))
        r1c2.plotly_chart(r1c2fig, use_container_width=True)

        r1c3fig = go.Figure(go.Indicator(mode="number", value=num_media, delta={"reference": 512, "valueformat": ".0f"}, title={"text": "TOTAL MEDIA"}, domain={'y': [0, 1], 'x': [0.25, 0.75]}))
        r1c3fig.update_layout(margin=dict(l=0, r=0, b=0, t=0, pad=4))
        r1c3.plotly_chart(r1c3fig, use_container_width=True)

        r1c4fig = go.Figure(go.Indicator(mode="number", value=num_links, delta={"reference": 512, "valueformat": ".0f"}, title={"text": "TOTAL LINKS"}, domain={'y': [0, 1], 'x': [0.25, 0.75]}))
        r1c4fig.update_layout(margin=dict(l=0, r=0, b=0, t=0, pad=4))
        r1c4.plotly_chart(r1c4fig, use_container_width=True)

        # Timeline Daily
        daily_timeline = helper.day_timeline(selected_user, df)
        r2c2fig = px.line(daily_timeline, x="date_only", y="message", title='Daily Activity Timeline',
                          labels={"date_only": "Date", "message": "Number of Messages"})
        r2c2fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
        r2c2fig.update_layout(height=600, margin=dict(l=100, r=100, b=100, t=100, pad=4), title_x=0.5)
        st.plotly_chart(r2c2fig, use_container_width=True)


        # finding the active users in the group (Group Level)
        if selected_user == "Overall":
            col1, col2 = st.columns(2)
            # Most Active Users
            x, percent_df = helper.most_active_users(df)
            fig1 = px.bar(data_frame=x[:5], title="Most Active Users", height=600,
                          labels={"index": "User", "value": "Number of Messages"})
            fig1.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
            fig1.update_layout(width=800, margin=dict(l=100, r=100, b=100, t=100, pad=4), showlegend=False, title_x=0.5)
            col1.plotly_chart(fig1, use_container_width=True)

            # Percentage of Active Users
            fig2 = go.Figure(data=[go.Table(header=dict(values=list(percent_df.columns), fill_color='black', align='center', height=31),
                                            cells=dict(values=[percent_df.Name, percent_df["Percentage of Activity"]], fill_color='black', align='center', height=31))])
            fig2.update_layout(title="Percentage of Active Users", autosize=True, width=400, height=605,
                               margin=dict(l=100, r=100, b=100, t=100, pad=4), paper_bgcolor="black", title_x=0.5)
            fig2.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
            col2.plotly_chart(fig2, use_container_width=True)


        # Word Cloud
        df_wc = helper.create_wordcloud(selected_user, df)
        fig3 = px.imshow(df_wc, color_continuous_scale='black', title="Mostly Used Word-Cloud")
        fig3.update_layout(width=1200, height=600, margin=dict(l=0, r=0, b=100, t=100), title_x=0.5)
        fig3.update_layout(coloraxis_showscale=False)
        fig3.update_xaxes(showticklabels=False, visible=False)
        fig3.update_yaxes(showticklabels=False, visible=False)
        st.plotly_chart(fig3, use_container_width=True)


        r2c1, r2c2 = st.columns(2)
        # Most Common Words
        most_common_df = helper.most_common_word(selected_user, df)
        fig4 = px.bar(data_frame=most_common_df, x="Count", y="Word", title="Most Common Words")
        fig4.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
        fig4.update_layout(margin=dict(l=100, r=100, b=100, t=100, pad=4), title_x=0.5)
        r2c1.plotly_chart(fig4, use_container_width=True)

        # Most Common Emoji
        emoji_df = helper.emoji_helper(selected_user, df)
        fig5 = px.pie(emoji_df[:10], values='Count', names='Emoji', color_discrete_sequence=px.colors.sequential.Blues, title="Emoji Analysis")
        fig5.update_layout(margin=dict(l=100, r=100, b=100, t=100, pad=4), title_x=0.5)
        r2c2.plotly_chart(fig5, use_container_width=True)



        # Timeline Monthly
        month_timeline = helper.monthly_timeline(selected_user, df)
        r2c1fig = px.line(month_timeline.tail(12), x="time", y="message", title='Monthly Activity Timeline',
                          labels={"time": "Month", "message": "Number of Messages"})
        r2c1fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
        r2c1fig.update_layout(height=600, margin=dict(l=100, r=100, b=100, t=100, pad=4), title_x=0.5)
        st.plotly_chart(r2c1fig, use_container_width=True)


        r3c1, r3c2 = st.columns(2)

        # Week Activity
        week_activity = helper.week_activity(selected_user, df)
        r3c1fig = px.bar(data_frame=week_activity[:5], title="Most Active Day", height=600,
                         labels={"index": "Day", "value": "Number of Messages"})
        r3c1fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
        r3c1fig.update_layout(width=800, margin=dict(l=100, r=100, b=100, t=100, pad=4), showlegend=False, title_x=0.5)
        r3c1.plotly_chart(r3c1fig, use_container_width=True)

        # Month Activity
        month_activity = helper.month_activity(selected_user, df)
        r3c2fig = px.bar(data_frame=month_activity[:5], title="Most Active Month", height=600,
                         labels={"index": "Month", "value": "Number of Messages"})
        r3c2fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
        r3c2fig.update_layout(width=800, margin=dict(l=100, r=100, b=100, t=100, pad=4), showlegend=False, title_x=0.5)
        r3c2.plotly_chart(r3c2fig, use_container_width=True)