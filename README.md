# EconoFactCheck
## University of London Final Project

EconoFactCheck is to create an easy-to-use, reliable, and accurate Financial Technology (FinTech) web application tool to help investors discern between fake and real news that can potentially affect their investment decisions. Because news can also contain sentiment that may sway the reader’s opinion, the tool contains a sentiment analysis feature that allows the user to determine whether the news is biased, rather than presenting facts to allow the reader to come to their conclusions about the information. Additionally, the tool contains a visual feature that allows the user to view the text classifier and sentiment analysis results as a word cloud or graph to better understand the contents of the article or document. 

To run this web application:
1. Fine-tune and save the text classifier model
   Because my fine-tuned model was too large to save to this repository, you'll have to fine-tune and save your own model. The first thing you're going to want to do is go into the backend.py file and scroll down to the "if __name__ == '__main__':" section. Uncomment the first three lines of code and comment out the rest of the section's code as follows:
   ![image](https://github.com/AnikaGoel02/EconoFactCheck/assets/87030632/fb677645-dc85-4bf8-b182-3bc88a9f796c)
   Run the script by typing 'python backend.py' in your local terminal. This is what the output should look like at the end of training:
   ![image](https://github.com/AnikaGoel02/EconoFactCheck/assets/87030632/b36906dc-a135-4cd1-acc3-87f89283344c)
After it completes training the model (~5 mins), it will save the fine-tuned model to your current directory. Look for a folder called 'model'. 

2. Fine-tune and save the sentiment analysis model
   A similar process will done for the sentiment analysis model. This time, comment all lines except the line that calls the function 'supportSentimentAnalysis()':
   ![image](https://github.com/AnikaGoel02/EconoFactCheck/assets/87030632/beab5c60-8101-4ef6-b7b9-6e46f5257496)
   Run the script by typing 'python backend.py' in your local terminal. It will save the fine-tuned model called 'sentAnalysisModel' to your current directory after it completes the training.

3. Test the models.
   To test the text classifier, comment all lines in the backend.py main function except for the line that loads the text classifier model and the three lines at the bottom.
   ![image](https://github.com/AnikaGoel02/EconoFactCheck/assets/87030632/8b77b611-6f91-4c66-b680-77da0ba2cd80)
   You should get an output that looks something like this:
   ![image](https://github.com/AnikaGoel02/EconoFactCheck/assets/87030632/0c59cf45-7e2b-4ef8-8db4-06fd36c29c46)

   Similarly, to test the sentiment analysis model, comment all lines in the backend.py main function except for the line that loads the sentiment analysis model and the three lines at the bottom.
   ![image](https://github.com/AnikaGoel02/EconoFactCheck/assets/87030632/912713c9-42ae-42ab-9bda-c858a8f6c72e)
   You should get an output that looks something like this:
   ![image](https://github.com/AnikaGoel02/EconoFactCheck/assets/87030632/2ee02ceb-aea2-43f7-8777-4348ab836969)

4. Run the web application.
   After fine-tuning the models, you can run the web application. Type 'streamlit run frontend.py' in the terminal. This will open a browser with the web application.

   This is what the you should see in the browser:
   
   The default selected radio button is URL. The user can enter in a URL for detection. Upon pressing the "Fetch Article" button, the app will display the article's contents directly on the web page. To classify the article, the user should press the 'Classify Article" button.
   ![image](https://github.com/AnikaGoel02/EconoFactCheck/assets/87030632/840cf796-feb3-4fdb-a22d-ac104cf67e99)

   When you click on the text radio button, the app should display a text field for the user to enter in the article's contents.
   ![image](https://github.com/AnikaGoel02/EconoFactCheck/assets/87030632/f9d3cf52-ce37-4271-8491-51fc1be6e438)

   When you click on the local directory radio button, the app should display an area where the user can drag and drop or browse for a file. 
   ![image](https://github.com/AnikaGoel02/EconoFactCheck/assets/87030632/849327dd-7d30-410f-b64f-ea235db6496a)

   A word cloud and sentiment analysis pie chart should be displayed when the user presses the 'Show Visualizations" button.
   ![image](https://github.com/AnikaGoel02/EconoFactCheck/assets/87030632/3ad0dc22-aa5a-4876-b503-283069fbaacf)


   Here is a link to a video presenting how to use the tool: https://youtu.be/qTf80wms9aw
