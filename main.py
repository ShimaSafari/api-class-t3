import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Connection to Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="Sheet2", usecols=list(range(3)), ttl=5)
df = df.dropna(how="all")


st.title('_Shima_: Welcome :yellow_heart: :wave:')
st.header('', divider='rainbow')

action = st.selectbox(
    "Choose an Action",
    [
        "Write New Comment",
        "View All Result",
    ],
)

if action == "Write New Comment":
    st.header('Comment Form')
    with st.form("comment_form"):

        star_rating = st.select_slider(
            label="How do you rate our product?:star::star::star::star::star:",
            options=[1, 2, 3, 4, 5])

        feedback_title = st.text_input("Write your product code:")
        feedback_comments = st.text_area("Write your comment about the product")
        st.markdown("**required*")
        submit_button = st.form_submit_button("Submit Feedback")

        if submit_button:
            if not feedback_title or not feedback_comments:
                st.warning("Ensure all fields are filled. :eyes:")
            else:
                # Collect feedback data
                feedback_data = pd.DataFrame([
                    {
                        "Star Rating": star_rating,
                        "Feedback Title": feedback_title,
                        "Feedback Comments": feedback_comments
                    }
                ])

                # Add new data to Google Sheet
                add_df = pd.concat([df, feedback_data], ignore_index=True)
                conn.update(worksheet="Sheet2", data=add_df)

                st.success("Thank you for your feedback! :full_moon_with_face::+1: ")


elif action == "View All Result":
    st.title("Product Feedback Result")
    # Display bar chart
    rating_counts = df['Star Rating'].value_counts().reset_index(name='Counts')
    rating_counts.columns = ['Star Rating', 'Counts']

    st.bar_chart(rating_counts, x='Star Rating', y='Counts', color="#fd0")

    average_rating = df['Star Rating'].mean()
    st.subheader(f"Average Rating: {average_rating:.1f} / 5 :star: ")
    st.dataframe(df, selection_mode="multi-row", use_container_width=True, hide_index=True)
