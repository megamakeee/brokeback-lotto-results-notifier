# Brokeback Lotto Results Notifier
A simple python script that will get the latest lottery results, check them against Brokeback crews own lottery lines and notify the results.
### Installation
* Get the code and install place it to a server of your choice.
* Install python and pip
```bash
sudo apt-get install python3 pip
python3 -m pip install -r <script-location>/brokeback-lotto-results-notifier/requirements.txt
```
* Set environment variables for twilio API secrets
```bash
vi ~/.bash_profile
export twilio_account_sid=<insert twilio account sid>
export twilio_auth_token=<insert twilio auth token>
export twilio_from_number=<insert twilio registered phonenumber>
source ~/.bash_profile
```
* Schedule the script to run every saturday ten minutes after lotto has been drawn (21:10)
```bash
10 21 * * 6 python3 <script-location>/brokeback-lotto-results-notifier/lotto.py >/dev/null 2>&1
```
### Development
Want to contribute? Contact through Brokeback Whatsapp group and we shall discuss!
### Todos
* Support for lotto doubling and plus numbers

![](https://decider.com/wp-content/uploads/2014/10/brokeback-mountain2.png?w=500&crop=1) 
