import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from streamlit_lottie import st_lottie
import requests

# MongoDB Connection
uri = "mongodb+srv://sylvester:Hostwire123$@restaurantsdb.ptj9p.mongodb.net/?retryWrites=true&w=majority&appName=restaurantsdb"
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    st.success("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    st.error(e)

# Access Database and Collection
test_db = client['test']
swigge = test_db['swiggyrestaurants']

# Define Fields to Retrieve
fields_to_print = {
    "aggregatedDiscountInfoV3": 1,
    "avgRating": 1,
    "cuisines": 1,
    "location": 1,
    "name": 1,
    "areaName": 1,
    "locality": 1,
    "_id": 0
}

# Fetch Data
data = list(swigge.find({}, fields_to_print))
df = pd.DataFrame(data)

# Flatten Nested Fields
if 'location' in df.columns:
    location_df = pd.json_normalize(df['location'])
    df = pd.concat([df.drop(columns=['location']), location_df], axis=1)

if 'aggregatedDiscountInfoV3' in df.columns:
    discount_df = pd.json_normalize(df['aggregatedDiscountInfoV3'])
    df = pd.concat([df.drop(columns=['aggregatedDiscountInfoV3']), discount_df], axis=1)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Restaurant Filter", "Restaurant Comparison"])

# Home Page
if page == "Home":
    st.title("Welcome to Restaurant Finder 🍽️")
    from streamlit_lottie import st_lottie
    import requests


    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()


    # Example Lottie Animation URL (Replace with your choice)
    lottie_animation = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_1a8dx7zj.json")

    # Display Lottie Animation
    if lottie_animation:
        st_lottie(lottie_animation, height=300, key="restaurant_animation")

    st.write("Use this app to filter and compare restaurants based on cuisine, location, and ratings.")

    # Updated Image from Freepik
    image_url = "data:image/jpeg;base64,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"

    st.image(image_url, caption="Find the Best Restaurants 🍕")

# Restaurant Filter Page
elif page == "Restaurant Filter":
    st.title("Restaurant Filter 🍛")
    st.markdown(
        """
        <style>
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            .animated-text {
                animation: fadeIn 2s ease-in-out;
            }
        </style>
        <div class="animated-text">
            <h3>Use this app to filter and compare restaurants based on cuisine, location, and ratings.</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(df)

    # Filter Based on User Input
    cuisine_input = st.text_input("Enter the cuisine:").strip()
    if cuisine_input:
        filtered_df = df[df['cuisines'].apply(lambda x: cuisine_input in x if isinstance(x, list) else False)]

        if not filtered_df.empty:
            area_input = st.text_input("Enter the area name:").strip()
            if area_input:
                filtered_df = filtered_df[filtered_df['areaName'].str.contains(area_input, case=False, na=False)]

            if not filtered_df.empty:
                locality_input = st.text_input("Enter the locality (or leave blank to skip):").strip()
                if locality_input:
                    filtered_df = filtered_df[
                        filtered_df['locality'].str.contains(locality_input, case=False, na=False)]

                if not filtered_df.empty:
                    filtered_df = filtered_df.sort_values(by='avgRating', ascending=False)
                    st.dataframe(filtered_df[['name', 'avgRating', 'areaName', 'locality']])
                else:
                    st.warning("No results found for the specified locality.")
            else:
                st.warning("No results found for the specified area name.")
        else:
            st.warning("No results found for the specified cuisine.")

# Restaurant Comparison Page
elif page == "Restaurant Comparison":
    # Get user input for restaurant names
    rest1 = st.text_input("Enter the first restaurant name:").strip()
    rest2 = st.text_input("Enter the second restaurant name:").strip()

    if rest1 and rest2:
        rest1_data = df[df['name'].str.contains(rest1, case=False, na=False)]
        rest2_data = df[df['name'].str.contains(rest2, case=False, na=False)]
        if not rest1_data.empty:
            rating1 = rest1_data.iloc[0]['avgRating']
            area1 = rest1_data.iloc[0]['areaName']
            city1 = rest1_data.iloc[0]['locality']
            swiggy_link1 = f"[Find on Swiggy](https://www.swiggy.com/search?query={rest1.replace(' ', '%20')})"
        else:
            rating1 = None

        if not rest2_data.empty:
            rating2 = rest2_data.iloc[0]['avgRating']
            area2 = rest2_data.iloc[0]['areaName']
            city2 = rest2_data.iloc[0]['locality']
            swiggy_link2 = f"[Find on Swiggy](https://www.swiggy.com/search?query={rest2.replace(' ', '%20')})"
        else:
            rating2 = None


        if not rest1_data.empty and not rest2_data.empty:
            st.subheader("Comparison Table")
            comparison_df = pd.concat([rest1_data, rest2_data])
            st.dataframe(comparison_df[['name', 'avgRating', 'areaName', 'locality']])


            # Visual Comparison
            st.subheader("Visual Comparison")

            # Bar Chart - Rating Comparison
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.barplot(
                x=comparison_df['name'],
                y=comparison_df['avgRating'],
                palette="viridis",
                ax=ax
            )
            ax.set_ylabel("Average Rating")
            ax.set_xlabel("Restaurant")
            ax.set_title("Restaurant Rating Comparison")
            st.pyplot(fig)


            st.subheader("Summary")
            if rating1 is not None and rating2 is not None:
                if rating1 > rating2:
                    best_restaurant = rest1
                    comparison_summary = (
                        f"Based on customer ratings, **{rest1}** emerges as the better choice with an impressive rating of {rating1}. "
                        f"It surpasses **{rest2}**, which has a lower rating of {rating2}. Customers seem to appreciate the overall experience "
                        f"at **{rest1}**, indicating better food quality, service, and ambiance."
                    )
                elif rating2 > rating1:
                    best_restaurant = rest2
                    comparison_summary = (
                        f"According to customer reviews, **{rest2}** stands out as the preferred option with a rating of {rating2}. "
                        f"In contrast, **{rest1}** received a slightly lower rating of {rating1}. The higher rating suggests that **{rest2}** "
                        f"offers a more satisfying dining experience, possibly due to better service, food quality, or overall ambiance."
                    )
                else:
                    best_restaurant = "Both restaurants are equally rated."
                    comparison_summary = (
                        f"Both **{rest1}** and **{rest2}** have received the same customer rating of {rating1}, indicating that they are equally popular. "
                        f"This suggests that both restaurants provide a comparable level of service, food quality, and overall experience. "
                        f"Choosing between them may come down to personal preferences such as menu selection, location, or ambiance."
                    )

                st.subheader("Comparison Summary")
                st.write(comparison_summary)
                website1 = f"[{rest1}.com](https://{rest1.replace(' ', '').lower()}.com)" if not rest1_data.empty else "Website not available"
                website2 = f"[{rest2}.com](https://{rest2.replace(' ', '').lower()}.com)" if not rest2_data.empty else "Website not available"

                st.subheader("Restaurant Ratings & Links")
                st.write(f"**{rest1}:** {rating1 if rating1 is not None else 'Rating not available'} ⭐")
                st.write(f"🔗 {swiggy_link1}")

                st.write(f"Rating for {rest2}: {rating2}")
                st.write(f"**{rest1}:** {rating1 if rating1 is not None else 'Rating not available'} ⭐")
                st.write(f"🔗 {swiggy_link2}")
        else:
            st.warning("One or both restaurant names not found in the database.")

