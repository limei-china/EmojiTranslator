import streamlit as st
from openai import OpenAI

def main():
      st.set_page_config(page_title="Emoji Translator App")
      st.title("Emoji Expert :sunglasses: ")
      st.subheader("Help to find the emoji suitable for you")
      # Get the API key from the user
      api_key = st.secrets.openai_key
      st.chat_message("assistant").write("Tell me how you're feeling or what's on your mind.")
      if api_key:
        # Create the Anthropi client
        client = OpenAI(api_key=api_key)

        # Define mood categories
        mood_categories = ["Happy", "Sad", "Angry", "Fearful", "Worried", "Excited","Surprised","Confused", "Enthusiastic", "Neutral", "Love", "Tired"]
        emtion_dictionary = {
            "Happy" : "😄",
            "Sad" : "😢",
            "Angry" : "😡",
            "Fearful" : "😨",
            "Worried" : "😟",
            "Excited" : "😆",
            "Surprised" : "😮",
            "Confused" : "😕",
            "Enthusiastic" : "🤩",
            "Neutral" : "😐",
            "Love" : "😍",
            "Tired" : "😴"
        }
        # Get user input
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "Tell me how you're feeling or what's on your mind."}]          
        
        if prompt := st.chat_input():
            message = f"Based on the following text, can you analyze the overall mood or sentiment expressed by the person?\n\n" \
                      f"The user's message is: {prompt}\n\n"
            
            st.session_state.messages.append({"role": "user", "content": message})

            st.chat_message("user").write(prompt)
            response = client.chat.completions.create(model="gpt-3.5-turbo-0125", messages=st.session_state.messages)

            mood_analysis = response.choices[0].message.content
            # Display the mood analysis using Markdown for formatting
            st.markdown("**Mood Analysis:**")
            st.write(mood_analysis)

            # Categorize the mood based on keywords or patterns
            mood_category = "Neutral"
            for category in mood_categories:
                if category.lower() in mood_analysis.lower():
                    mood_category = category
                    break

            # Display the mood category with emphasis
            mood_display = f"**Mood Category:** {mood_category}"
            if mood_category == "Happy" or mood_category == "Excited" or mood_category == "Enthusiastic":
                st.success(mood_display)
            elif mood_category == "Sad" or mood_category == "Angry":
                st.error(mood_display)
            elif mood_category == "Anxious" or mood_category == "Fearful" or mood_category == "Confused":
                st.warning(mood_display)
            else:  # Neutral or any other category
                st.info(mood_display)

            # Provide recommendations
            st.write("**Recommendations:**")
            st.write(f"Based on the result, the recommand emoji for you is {emtion_dictionary[mood_category]}")

      else:
        st.warning("Please enter your Anthropic API Key to use the app.")

if __name__ == "__main__":
    main()