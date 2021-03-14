# Rackathon_2021

## Objective
The objective of this project is to build a AI augmented decision making system for trading stocks of Nifty 50 banks The Nifty 50 banks comprise of Axis, HDFC, ICICI, Induslnd and SBI. The user inserts the financial news article into our postman request, and the build in machine learning system will recommend its decision on whether to invest or to divest on this stock today!

## Implementation
There are two machine learning models (Naive Bayes and Logistic Regression), which are trained with news articles of Nifty50 banks, sourced from the moneycontrol website for the last 11 years (2010 to 2011)! Based on the date of the news article the yahoo api is called for the stock data of that company on that particular day. Using the stock data a new feature is made that subtracts the opening and closing price of the stock (profit/loss feature). This feature is used to label the news as positive or negative. Hence, the model can predict only in the time frame of the entire day, and not for the fluctuations within the day.

The ETL process accommodates for news articles published after 3:30 pm to be influencing only the next days stock price.  It also allocates the news published on holidays to the next working day of that particular stock (the number of holidays that are accounted for are upto two days). **This is the largest data on this category that is web parsed from the public domain to the best of our knowledge!**  The news articles that are published on the same day are compressed to a single news article, and labelled based on the profit/loss feature built from the Yahoo APi.  


## Application
The user inputs the news article from the postman request, which is read API. This API uses one of our trained model either a Naive Bayes model or Logistic Regression model, and it outputs it recommendation as either a "positive news" or "negative news"!


## Future
**In our future version there will be UI hosted in amazon, and the API is going to be done in serverless Lambda application. Hence, the user will have a smooth experience. Furthermore, we will generate artificial news articles to balance as well as increase the data count. This will enable us to use more sophisticated models such as Convolution Neural Network. **

**To summarize, in future the user will have UI with input box, and a submit button as well as better prediction results. Currently, the prediction accuracy is around 60% for both the models. Hence, by default we use the Naive Bayes model, which in future will left out at the users discretion to choice the model.**
