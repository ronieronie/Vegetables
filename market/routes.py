from market import app, db
from market.models.User import User
from market.models.Commodities import Commodities
from flask import render_template, redirect, session, request, jsonify
import calendar
from flask_wtf.csrf import CSRFProtect
import statistics
# from market.models import Item, User
# from market.forms import RegisterForm, LoginForm

# from flask_login import login_user, logout_user, login_required
import pickle
import numpy as np  
from werkzeug.security import generate_password_hash, check_password_hash


csrf = CSRFProtect(app)
model = pickle.load(open('C:\\Users\\cardo\\FlaskMarket\\market\\model.pkl','rb'))
kgmodel = pickle.load(open('C:\\Users\\cardo\\\FlaskMarket\\market\\kgmodel.pkl','rb'))

logged_user = ''

@app.route('/')
@app.route('/home')
def home_page():    
    return render_template('index.html')

@app.route('/home_page')
def get_home_page():
    if 'user' in session:
        user = session['user']
        return render_template('/home.html', user=user)
    return render_template('login_page.html')

@app.route('/get_login_page')
def get_login_page():
    if 'user' in session:
        return redirect('/home_page')
    return render_template('login_page.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password') 

    user = User.query.filter_by(email=email).first()
    
    if user and check_password_hash(user.password, password):
        session['user'] = user.name
        return redirect('/home_page')
    
    else:
        session.pop('user', None)
        return "Invalid credentials", 401
    
@app.route('/market')
def market_page():
    if 'user' not in session:
        return redirect('/get_login_page') 
    
    user = session['user']
    return render_template('market.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/get_login_page')

@app.route('/get_market_prices')
def get_market_prices():
    commodities = Commodities.query.all()
    return jsonify([
        {"id": c.id, "commodity_type": c.commodity_type, "price": c.price}
        for c in commodities
    ])

@app.route('/forecast/<commodity>')
def forecast(commodity):
    if 'user' not in session:
        return redirect('/get_login_page') 
    user = session['user']

    user = session['user']
    selected_commodity = Commodities.query.filter_by(commodity_type=commodity).first()
    price = selected_commodity.price
    return render_template('forecast.html', commodity=commodity, price=price, user=user)
    
@app.route('/predict_price', methods=['POST'])
def predict_price():
    #month
    January = 0                   
    February = 0          
    March = 0                    
    April = 0                    
    May = 0                        
    June = 0                    
    July = 0                      
    August = 0                 
    September = 0              
    October = 0                    
    November = 0                   
    December = 0
    getmonth = request.form.get('month')
    if getmonth == 'January':
        January = 1
    elif getmonth == 'February':
        February = 1
    elif getmonth == 'March':
        March = 1
    elif getmonth == 'April':
        April = 1
    elif getmonth == 'May':
        May = 1
    elif getmonth == 'June':
        June = 1
    elif getmonth == 'July':
        July = 1
    elif getmonth == 'August':
        August = 1
    elif getmonth == 'September':
        September = 1
    elif getmonth == 'October':
        October = 1
    elif getmonth == 'November':
        November = 1
    elif getmonth == 'December':
        December = 1
    
    #market
    Metro_Manila = 0
    Santa_Cruz = 0
    Bulacan = 0
    Pampanga = 0
    Cavite = 0
    Laguna  = 0
    Rizal = 0  

    #grid values
    latitude = 0
    longtitude = 0

    #provinces
    metro_manila = 0
    bulacan = 0
    laguna = 0 
    rizal = 0
    cavite = 0
    
    #region
    ncr = 0
    region_iii = 0
    region_iv = 0

    getyear = request.form.get("year")
    getlocation = request.form.get("market_location")

    if getlocation == 'Metropolitan Manila, Metro Manila Market':
        ncr = 1
        metro_manila = 1
        Metro_Manila = 1
        latitude = 14.604167
        longtitude = 120.982222

    elif getlocation == 'Rizal, Santa Cruz Market':
        region_iv = 1
        rizal = 1
        Santa_Cruz = 1
        latitude = 14.6089
        longtitude = 121.1712

    elif getlocation == 'Bulacan, Bulacan Market':
        region_iii = 1
        bulacan = 1
        Bulacan = 1
        latitude = 14.843102
        longtitude = 120.814215

    elif getlocation == 'Rizal, Rizal Market':
        region_iv = 1
        rizal = 1
        Rizal = 1
        latitude = 14.594806
        longtitude = 121.171055

    elif getlocation == 'Bulacan, Pampanga Market':
        region_iii = 1
        bulacan = 1
        Pampanga = 1
        latitude = 15.02486
        longtitude = 121.086142

    elif getlocation == 'Laguna, Laguna Market':
        region_iv = 1
        laguna = 1
        Laguna = 1
        latitude = 14.286267
        longtitude = 121.41211

    elif getlocation == 'Cavite, Cavite Market':
        region_iv = 1
        cavite = 1
        Cavite = 1
        latitude = 14.422901
        longtitude = 120.94107

    veg = request.form.get('commodity')
    price = request.form.get('price')

    Cabbage = 0             
    Carrots = 0              
    Garlic = 0             
    OnionsR = 0         
    Tomatoes = 0            
    OnionsW = 0          
    Lantundan = 0      
    Saba = 0           
    GBeans = 0    
    SBeans = 0          
    Bittermelon = 0            
    Bottlegourd = 0            
    CabbageC = 0        
    Calamansi = 0            
    Choko = 0           
    Coconut = 0               
    Eggplants = 0             
    Ginger = 0          
    Papaya = 0               
    Squashes = 0              
    SweetPotatoLeaves = 0      
    Waterspinach = 0            
    Lakatan = 0       
    MangoesC = 0       
    MangoesP = 0           
    Pineapples = 0             
    Mandarins = 0           

    if veg == 'Garlic':
        Garlic = 1
    elif veg == 'Carrot':
        Carrots = 1
    elif veg == 'Cabbage':
        Cabbage = 1
    elif veg == 'Onion':
        OnionsR = 1
    elif veg == 'Tomatoes':
        Tomatoes = 1
    elif veg == 'Onions (white)':
        OnionsW = 1
    elif veg == 'Banana (Latundan)':
        Lantundan = 1
    elif veg == 'Bananas (saba)':
        Saba = 1
    elif veg == 'Beans (green, fresh)':
        GBeans = 1
    elif veg == 'Beans (string)':
        SBeans = 1
    elif veg == 'Bitter melon':
        Bittermelon = 1
    elif veg == 'Bottle gourd':
        Bottlegourd = 1
    elif veg == 'Cabbage (chinese)':
        CabbageC = 1
    elif veg == 'Calamansi':
        Calamansi = 1
    elif veg == 'Choko':
        Choko = 1
    elif veg == 'Eggplants':
        Eggplants = 1
    elif veg == 'Ginger ':
        Ginger = 1
    elif veg == 'Papaya':
        Papaya = 1
    elif veg == 'Squashes':
        Squashes = 1
    elif veg == 'Sweet Potato leaves':
        SweetPotatoLeaves = 1
    elif veg == 'Water spinach':
        Waterspinach = 1
    elif veg == 'Bananas (lakatan)':
        Lakatan = 1
    elif veg == 'Mangoes (carabao)':
        MangoesC = 1
    elif veg == 'Mangoes (piko)':
        MangoesP = 1
    elif veg == 'Pineapples':
        Pineapples = 1
    elif veg == 'Mandarins':
        Mandarins = 1
    elif veg == 'Coconut':
        Coconut = 1

    #int(month),int(getyear),int(latitude),int(longtitude)
    int_features = [float(latitude),float(longtitude),int(getyear),int(Lakatan),int(Lantundan),int(Saba),
                    int(GBeans),int(SBeans),int(Bittermelon),int(Bottlegourd),int(Cabbage),int(CabbageC),int(Calamansi),
                    int(Carrots),int(Choko),int(Coconut),int(Eggplants),int(Garlic),int(Ginger),int(Mandarins),int(MangoesC),
                    int(MangoesP),int(OnionsR),int(OnionsW),int(Papaya),int(Pineapples),int(Squashes),int(SweetPotatoLeaves),
                    int(Tomatoes),int(Waterspinach),int(bulacan),int(cavite),int(laguna),int(metro_manila),int(rizal),int(Bulacan),
                    int(Cavite),int(Laguna),int(Metro_Manila),int(Pampanga),int(Rizal),int(Santa_Cruz),int(January),int(February),
                    int(March),int(April),int(May),int(June),int(July),int(August),int(September),int(October),int(November),
                    int(December),int(ncr),int(region_iii),int(region_iv)]

    #priceforecasting
    final_features = [np.array(int_features)]
    pred_price = model.predict(final_features)
    output = round(pred_price[0],2)
    dif =  float(output) - float(price) 
    ave = (float(price)+float(output))/2
    quo = float(dif)/float(ave)
    percc = float(quo)*100
    perc = round(percc,2)

    if dif < 0:
        inc = "Decrease"
        trend = '<i class="bi bi-graph-down-arrow fs-3 text-primary"></i>'
        color = 'text-primary'
        
    elif dif >= 0:
        inc = "Increase"
        trend = '<i class="bi bi-graph-up-arrow fs-3 text-danger"></i>'
        color = 'text-danger'
        

    #kilogramforecasting
    kg_int_features = [float(output),int(getyear),int(Lakatan),int(GBeans),int(SBeans),int(Bittermelon),
                    int(Bottlegourd),int(Cabbage),int(Calamansi),int(Carrots),int(Choko),int(Eggplants),int(Garlic),int(Ginger),
                    int(MangoesC),int(OnionsR),int(OnionsW),int(Papaya),int(Pineapples),int(Squashes),int(Tomatoes),int(Waterspinach),int(January),
                    int(February),int(March),int(April),int(May),int(June),int(July),int(August),int(September),int(October),int(November),
                    int(December)]
    
    kg_final_features = [np.array(kg_int_features)]
    pred_kg = kgmodel.predict(kg_final_features)
    kg_output = round(pred_kg[0],2)
    kgtext = ""

    if kg_output != 0:
        kgtext = "Around "+ str(kg_output) +" kilograms are likely to sell for this price in " + str(getmonth) + "."

    if Lantundan == 1 or Saba == 1 or CabbageC == 1 or Mandarins == 1 or MangoesP == 1 or SweetPotatoLeaves == 1 or Coconut == 1:
        kg_output = 0
        kgtext = " Data is not available"
    
    if Pineapples == 1:
        kgtext = "Around "+ str(kg_output) +" pieces are likely to sell for this price in " + str(getmonth) + "."
        
    print("pakyu")
    print(int_features)
    print(output)
   
    return jsonify({
        'success': True,
        'output': output,
        'price': price,
        'inc': inc,
        'percent': perc,
        'trend': trend,
        'color': color,
        'kg_text': kgtext,
    })

@app.route('/price_info_chart/<id>')
def price_info(id):
    if 'user' not in session:
        return redirect('/get_login_page') 
    
    user = session['user']
    month = 12
    yr = '2021'
    if id == '1':
        desc = "The graph shows the movement of prices in the markets of Metro Manila and nearby provinces. As you can see the Metro Manila Market and Rizal Market have the highest prices above all the six markets while Bulacan and Pampanga have the lowest prices. The prices doesnt go up and down that much. It's stable throughout the year of 2021 and the differences between the prices of garlic is in its market location."
        veg = 'Garlic'
        mtr = [301.67, 297.5, 290.83, 287.08, 287.08, 285.75, 294.48, 295.42, 277.23, 305.64, 343.51, 345.97]
        bul = [136.5, 139, 112.13, 113.75, 115, 113.75, 113.75, 125.46, 121.28, 118.77, 110.41, 112.92]
        pam = [109.38, 101.88, 101.88, 110.63, 103.75, 103.13, 103.13, 118.94, 126.53, 131.59, 127.79, 129.69]
        riz = [281.67, 290, 296.67, 288.33, 296.67, 296.67, 291.67, 300, 285, 301.67, 301.67, 301.67]
        cav = []
        lag = []

    elif id == '2':
        desc = "All places such as Bulacan, Pampanga, Cavite, Laguna and Rizal have increased the price of onions but Metro Manila is the only one that has a sudden price increase when it comes to onions. This shows that the onion price jumped too much within Metro Manila than in the said areas. Here it can be seen that there is already an increase in the price of onion in the year 2021 and it will increase even more in the year 2022 and 2023."
        veg = 'Onion'
        mtr = [0,0, 102.87, 100.4, 99.33, 106.62, 109.28, 110.27, 114.25, 125.82, 147.22, 163.02]
        bul = [151.25, 115, 115, 105, 105, 101.25, 98.75, 106.02, 107.5, 110.79, 128.53, 153.55]
        pam = [100, 80.63, 78.13, 80.38, 85, 76.88, 93.13, 116.42, 112.01, 129.01, 132.15, 159.21]
        cav = [116.88, 119.38, 125, 103.13, 109.38, 106.25, 105, 115, 124.7, 143.43, 148.99, 186.98]
        riz = []
        lag = []

    elif id == '3':
        desc = "According to what the graph says, there was an increase and decrease in the price of cabbage in 2021. But it is still obvious that Metro Manila still has the price increase again when it comes to Cabbage. It can be seen here that the increase or decrease in price means that there is a balance and no vegetables are wasted due to what the graph shows."
        veg = 'Cabbage'

        mtr = [0,0,70.02, 60.89, 55.92, 65.07,85.08, 117.47,95.83,77.36,76.7,56.86]
        bul = [160, 114.63, 55.63, 43.75, 43.25,35.25,50.25, 90.59,110.4,111.43,96.99,45.4]
        pam = [133.75, 112.5, 68.75, 49.38, 33.75,33.13,38.75, 60.63,136.88,88.75,82.5,56.88]
        cav = [195, 149.38, 90, 60, 71.25, 62, 75.63, 128.75,179.65,127.25,163.93,102.25]
        lag = [186.25, 131.25, 81.25, 60, 53.13, 55, 81.25, 132.5,103.13,111.25,116.25,76.25]
        riz = [183.13, 141.25, 69.38, 52.5, 50.63, 60, 82.5, 134.38,126.13,98.88,116,69.88]

    elif id == '4':
        desc = "The only movement in the price of bananas (latundan) is only in the areas of Cavite, Laguna and Rizal. The movement of the prices in Laguna Market go up a little bit in March and it go down all the way to December while in the Cavite Market and Rizal Market have almost the same movement but the prices in Rizal Market are a way more higher than Cavite Market"
        veg = 'Bananas (Latundan)'
        cav = [50.63,51.25,50.63,51.25,50.63,48.13,43.25,52.5,50,54.38,52.5,49.38]
        lag = [62.5, 62.5, 63.75, 62.5, 62.5, 62.5, 61.88, 59.18, 57.83, 55.98, 55.13, 54.27]
        riz = [55,52.5,52.5,58.13,55,53.13,52.5,63.88,63.5,63.13,64.4,63.76]
        mtr = []
        pam = []
        bul = []

    elif id == '5':
        desc = "The areas of Bulacan, Pampanga, Laguna and Rizal continue to decrease in the graph. There is a steady increase again after a decrease but it immediately decreases after a few months. Metro Manila again has the price increase when it comes to the price of tomatoes. Cavite is the standout area with no price increase when it comes to tomatoes."
        veg = 'Tomatoes'
        mtr = [0,0, 38.64, 36.46, 37.01, 60.68, 93.19, 92.6, 78.79, 59.92, 58.12, 57.38]
        bul = [136.25, 52.5, 23.13, 19.75, 23.88, 24.63, 69, 73.05, 57.8, 37.86, 37.86, 31.14]
        pam = [158.13, 41.25, 21.38, 18.25, 22.63, 33.75, 56.75, 82.83, 69.85, 61.2, 48.21, 41.42]
        lag = [146.25, 75, 37.5, 25.63, 29.38, 39.38, 90, 97.4, 90.93, 62.24, 50.21, 46.97]
        riz = []
        cav = []
    
    elif id == '6':
        yr = '2020'
        desc = "The graph shows the movement of the prices of Onion (white) from April to December. The prices are stable with a little bit up and down from April to August and then it drastically increased starting from August to October. The prices decreased when November comes until December."
        month = 8
        veg = "Onion(white)"
        mtr = [79.02, 76.68, 70.81, 75.49, 90.5, 95.61, 92.66, 91.33]
        bul = [68.77, 72, 67.43, 68, 78.31, 104.92, 107.85, 95.54]
        pam = [55.69, 67.68, 62.11, 76.03, 116.38, 137.97, 86.9, 71.08]
        cav = [67.92, 69.27, 66.95, 65.18, 89.1, 74.78, 78.38, 76.73]
        lag = [72.47, 84, 81.56, 77.25, 89, 96.78, 101.38, 103.67]
        riz = []

    elif id == '7':
        yr = '2020'
        desc = " On this graph, we can see that every market starts in April, has small but steady prices, and has price fluctuations throughout the year. Due to its location in the city, the Rizal and Metro Manila Markets have the highest pricing, while the Laguna Market has the lowest."
        veg = 'Banana (saba)'
        month = 8
        mtr = [52.27, 53.21, 49.05, 51.74, 51.11, 50.73, 50.74, 50.59]
        lag = [23.81, 25.89, 25, 25, 26.53, 28.17, 29.5, 30.39]
        riz = [47.67, 52.5, 51.11, 48.75, 49.58, 51, 50.42, 49.58]
        cav = [40.47, 37.23, 35.92, 36.33, 40.08, 40.83, 40, 40]
        pam = [42.31, 39.49,37.14, 35.3, 36.17, 36.12, 39.03, 39.03, 39.91]
        bul = [36, 36, 36, 36, 36, 36, 36, 39.08]

    elif id == '8':
        desc = "The areas of Bulacan, Pampanga, Cavite, Laguna and Rizal saw almost simultaneous price increases and decreases when it comes to beans. As shown in the next graph, Metro Manila once again had the fastest price increase from February to June. Bulacan, on the other hand, is the only one among the aforementioned areas that has no movement or price change when it comes to beans from January to December."
        veg = 'Beans (green, fresh)'
        mtr = [0,0,74.49, 74.33, 76.64, 124.24, 93.19, 93.98, 82.51, 100.06, 105.36, 81.28]
        bul = []
        pam = [117.5, 85, 71.88, 76, 66.25, 117.5, 111.25, 108.3, 96.53, 108.3, 123.6, 77.69]
        cav = [150, 103.75, 96.25, 85, 85, 123.75, 96.88, 106.63, 95.63, 87.5, 95.63, 95]
        lag = [118.75, 80, 76.25, 67.5, 63.75, 115, 100, 87.5, 78.75, 77.5, 116.25, 87.5]
        riz = [123.75, 88.13, 73.13, 73.75, 76.25, 131.25, 110.63, 97.88, 88.75, 88.75, 146.25, 84.88]
    
    elif id =='9':
        yr = '2020'
        month = 8
        desc = "The graph shows the movement of the prices of Beans (string) from April to December. The movement of the prices in all six markets are almost the same. The prices in all markets are falling staring from May to August and when the ber months start the prices increased until November. Bulacan and Pampanga market prices increased while the rest are falling."
        veg = 'Beans (string)'
        bul = [82.31, 82.31, 73.57, 62.11, 60.46, 60.23, 58.92, 86.08]
        pam = [94.62, 62.52, 54.03, 40.85, 41.42, 54.03, 79.83,117.52]
        cav = [95.29, 74.23,43.2, 59.25, 54.53, 74.82, 113.08, 85.36]
        lag = [85.18, 69.33, 48.11, 43, 50.89, 64.67, 112.5,  88.11]
        riz = [112.07, 71.67, 86.67, 91.67, 100.71, 121.89, 183.33, 128.65]
        mtr = []
    
    elif id == '10':
        desc = "The prices of Bittermellon have the highest in January, and then it starts to go down until mid June and it goes up in august and it goes back down again and is stable in September to December. Rizal market has the highest starting price compared to the other markets while the Pampanga market has the lowest."
        veg = 'Bittermellon'
        mtr = [0,0,72.93,67.28,61.42,75.4,82.06,99.16,85.94,84.47,64.96,78.93]
        bul = [128,92.5,71,60,50.75,56.25,63.5,123.75,66.25,68.75,69.5,67.5]
        pam = [105,86.25,63.13,68.38,48.13,52.5,60,81.51,61.7,66.23,62.26,75.62]
        cav = [156.25, 125, 92.5, 80.63, 83.75, 73.13, 77.5, 106.25, 103.66, 119.65, 88.07, 100.87]
        lag = [135,96.25,77.5,62.5,52.5,63.75,70,104.77,86.92,87.62,73.25,63.51]
        riz = [168.75, 101.88, 75, 70.63, 59.38, 74.38, 78.75, 121.88, 86.25,105.38,73.88,79.63]
    
    elif id == '11':
        desc = "The prices of bottle gourds have the highest starting from January, and then it starts to go down until May and it will go up from June to August and it will go down until December. Pampanga Market has the highest prices of all the markets while Cavite has the lowest. The movement of the lines is almost the same to all of the markets in the Metro Manila and nearby provinces"
        veg = 'Bottegourd'
        mtr = [49.69, 39.56, 34.36, 31.64, 32.25, 36.47, 40.11, 45.73, 42.34, 35, 29.55, 29.03]
        bul = [45.63, 29.38, 22.25, 21.25, 20.5, 21.88, 23.75, 31.75, 32, 28.75, 28.13, 25]
        pam = [51.25, 38.63, 29.38, 26.25, 25.63, 21.25, 22.5, 27.25, 30.63, 31.63, 25, 26.88]
        cav = [33.13, 29.13, 26.25, 24.38, 27.5, 28.13, 27.5, 33.75, 32.59, 26.77, 26.89, 27.36]
        lag = [34.38, 27.5, 21.88, 20.63, 20.63, 20, 23.13, 25.79, 26.94, 25.61, 26.14, 25.69]
        riz = [45.49, 38.93, 29.37, 26.4, 24.58, 29.83, 34.23, 38.43, 40.47, 37.38, 31.56, 28.59]

    elif id == '12':
        yr = '2020'
        desc = "There were no sales from January to March. On the other side, we still have April through December. Looking at this graph, we can see that the five markets becomes more stable from the beginning of May and continues to be so through September, increasing through October, and then declining once more towards the conclusion of the year."
        veg = 'Cabbage (Chinese)'
        month = 8
        mtr = []
        bul = [58.46, 61.08, 55.57, 55.15, 56.46, 56, 94.15, 70.08]
        pam = [45.69, 45.72, 52.31, 45.28, 42.3, 59.23 ,96.53, 47.51]
        cav = [63.02, 66.77, 50.92, 62.2, 44.36, 75, 123.78, 55.3]
        lag = [48.12, 59.44, 49.89, 57.75, 57.33, 60.56, 117.38, 86.22]
        riz = [71.67, 83.33, 71.11, 89.17, 77.5, 151.33, 162.5, 88.08]
    
    elif id == '13':
        desc = "The Graph shows that Calamansi prices in Bulacan, Metro Manila, and Pampanga Market range between 50/kilo the lowest, and 100/kilo the highest throughout the year 2021.The differences between Pammpanga Market and Bulacan Market is the prices in Bulacan rise in February while the prices in the Pampanga falls. The movement is almost the same in March up to December. "
        veg = 'Calamansi'
        mtr = [0,0, 89.04, 90.69, 101.17, 76.16, 66.36, 66.87, 63.3, 61.6, 90.23, 85.14]
        bul = [63.75, 91.75, 77.5, 70, 87.5, 70, 53.75, 54.46, 48.97, 47.99, 68.67, 65.01]
        pam = [52.5, 44.43, 101.88, 75.63, 98.75, 66.88, 61.88, 55.93, 58.57, 31.56, 48.9, 66.06]
        cav = []
        riz = []
        lag = []
    
    elif id == '14':
        desc = "The Graph shows that Choco prices lowest range price was 20/kilo which can be bought in Bulacan, while the highest was 85/kilo which is in Cavite Market. It also shows in the graph that the prices of Choco in Markets drastically increased in September and then it went down up to December."
        veg = 'Choko'
        mtr = [36.94, 35.06, 30.07, 30.72, 32.71, 39.51, 44.97, 50.58, 45.88, 31.84, 29.48, 30.81]
        bul = [27.38, 27.25, 20, 19.75, 22.63, 24.38, 32.5, 46.63, 73.25, 35.75, 35.63, 25]
        pam = [32.5, 47.13, 29.13, 26.75, 25.38, 29.25, 41.88, 51.73, 76.97, 52.64, 37.98, 37.92]
        cav = [42.14, 41.43, 31.25, 32.63, 37.13, 40.25, 48.13, 61.75, 88.43, 59.28, 45.08, 42.61]
        lag = [35, 33.75, 30, 25, 27.5, 36.25, 41.25, 48.29, 72.62, 68.91, 48.16, 36.43]
        riz = [40.63, 38.13, 32.5, 30.63, 31.25, 36.25, 48.75, 55.25, 78.38, 40.5, 36.25, 39]

    
    elif id == '15':
        desc = "The Graph Shows the movement of prices of Coconuts in the markets of Metro Manila and nearby provinces, Based on the graphs the normal range price of Coconuts is 25 to 30/per Coconut and the highest price was 36/per coconut that is located in Pampanga Market."
        veg = 'Coconut'
        mtr = [28.4, 28.35, 28.37, 28.37, 28.69, 28.48, 28.43, 28.37, 28.82, 29.07, 29.05, 29.57]
        bul = [31.88, 32.5, 32.5, 32.5, 32.53, 32.5, 32.5, 32.5, 32.5, 32.5, 31.88, 31.88]
        pam = [36.25, 34.38, 31.88, 32.5, 33.75, 34.38, 34.38, 34.38, 34.38, 33.13, 33.13, 33.13]
        cav = [26.25, 26.25, 28.13, 27.5, 27.5, 28.13, 26.88, 25.63, 24.81, 24.81, 24.19, 24.81]
        lag = [25, 25, 25, 25.25, 25.5, 25.5, 25.5, 25.5, 25.5, 25.5, 25.5, 26.14]
        riz = [25, 24.38, 24.37, 25.5, 25.88, 26.88, 26.88, 26.88, 26.88, 26.88, 26.88, 26.88]

    elif id == '16':
        desc = "The Graph shows that Eggplants in different Markets have different starting prices. The highest was the Rizal market with almost 160/kilo while the other market is between 120-150/kilo. It also shows that prices of eggplants have been stable for 60-100/kilo."
        veg = 'Eggplants'
        mtr = [0,0,71.22, 66.92, 57.97, 54.84, 62.44, 85.89, 60.67, 72.88, 75.9, 81.11]
        bul = [140.63, 97, 67.5, 60.13, 43.13, 42.75, 45, 108.65, 63.65, 85.16, 90, 75.86]
        pam = [128.13, 86.88, 63.13, 55.63, 40.63, 40.63, 43.75, 65.05, 44.9, 30.51, 56.99, 71.96]
        cav = [141.88, 110.63, 90, 79.38, 76.88, 56.88, 51.88, 101.88, 74.82, 98.7, 126.57, 109.06]
        lag = [147.5, 103.75, 80, 66.25, 51.25, 50, 43.75, 85.59, 57.13, 67.54, 72.85, 53.85]
        riz = [173.75, 108.75, 80.63, 71.25, 63.75, 65.63, 56.25, 105.38, 65.5, 90.75, 95, 82]

    elif id == '17':
        desc = "The Metro Manila Market is practically straight from the beginning of February to the end of September, and we can observe that it gradually declines through December, according to the Ginger Graph. Pampanga Market and Bulacan Market continue to rise and fall throughout the year."
        veg = 'Ginger'
        mtr = [151.35, 157.85, 156.57, 154.42, 156.57, 154.42, 156.4, 156, 155.24, 148.63, 146.87, 137.18]
        bul = [153.75, 138.13, 128.75, 128.75, 128.75, 138.75, 118.75, 133.44, 116.3, 115.08, 117.53, 109.58]
        pam = [114.37, 110, 111.88, 121.25, 128.13, 123.75, 125.63, 132.68, 128.54, 106.15, 93.31, 88.94]
        cav = []
        riz = []
        lag = []

    elif id == '18':
        yr = '2020'
        month = 8
        desc = "The graph shows the movement of the prices of Beans (string) from April to December. The movement of the prices in all six markets are almost the same. The differences is the prices Pampanga are much higher among the six and followed by Cavite. Laguna is the 3rd highest prices and then Rizal and Bulacan markets have the lowest of among them."
        veg = 'Papaya'
        cav = [59.17, 60, 58.25, 59.57,60.75, 60.59, 59.53, 61.33]
        lag = [52.21, 55.63, 55.63, 55.63, 55.63, 55.63, 55.63]
        riz = [45, 44.58, 46.11, 47.5, 45, 45, 45, 45]
        mtr = []
        pam = [65.85, 67.12, 65.52, 61.77, 61.73, 73.71, 60.88, 64.54]
        bul = [45.69, 44.31, 45.5, 44.6, 43.23, 43.38, 43.85, 44.62]

    elif id == '19':
        desc = "Squashes Graph reveals that from January to April, the Metro Manila Market, Cavite Market, and Laguna Market are experiencing some hard patches. The three are having success from July through October again, but things start to falter at the end of the year."
        veg = 'Squashes'
        mtr = [101.81, 81.69, 52.53, 39.5, 35.19, 35.93, 38.72, 47.36, 49.83, 50.94, 48.51, 44.64]
        cav = [86.25, 93.13, 66.25, 41.88, 45.63, 37.5, 34.75, 46.25, 51.67, 57.08, 53.75, 49.76]
        lag = [83.75, 78.75, 52.5, 33.75, 31.25, 25, 31.88, 42.5, 41.25, 44.38, 35.63, 34.38]
        pam = []
        riz = []
        bul = []
    
    elif id == '20':
        yr = '2020'
        month = 8
        desc = "The graph indicates that April is the official beginning of the market. As we can see, the Bulacan Market has the most affordable costs compared to other markets. Cavite Market has high sales until the end of the year, although it begins off low and increases as the year comes to a close. The other market, however, has stable pricing."
        veg = "Sweet Potato Leaves"
        mtr = [56.98, 55.71, 51.96, 52.89, 52.95, 55.27, 72.25, 78.29]
        bul = [20, 20, 20, 20, 20, 20.15, 20.6, 21.78]
        pam = [36.31, 34.38, 32.82, 33.98, 37.97, 38.66, 37.88, 36.12]
        cav = [70.21, 65.85, 62.02, 60.6, 60.55, 62.22, 74.65, 81.59]
        lag = [47.1, 50, 50, 50, 50, 50, 74.65, 50, 50]
        riz = [37.2, 31.25, 32.87, 34.73, 33.6, 35.81, 50.96, 75.31]

    elif id == '21':
        yr = '2020'
        desc = "The graph shows the movement of prices in May. Prices are stable from May to December at Bulacan Market, Pampanga is stable as well, but it goes down a little bit in November, and it goes back up in December. Rizal Market prices go up and down in May until August and then it goes up until December. Laguna Market goes up and down until December, while in Metro Manila the prices are stable starting May up to October and then it goes up a bit higher from November up to December. Cavite Market prices are stable; it go up and down as well, but it's a little bit only."
        veg = 'Water Spinach'
        month = 8
        cav = [90, 84.46, 80.85, 73.8, 73, 71.25, 83.11, 88.4]
        lag = [44, 50.49, 48.52, 51.11, 46.79, 54.44, 59.72, 48.52]
        riz = [35.13, 35.79, 42.46, 36.4, 34.68, 35.06, 42.56, 59.8]
        mtr = [63.85, 64.27, 57.48, 56.36, 58.9, 63.85, 97.4, 103.07]
        pam = [37.92, 38.32, 37.42, 34.6, 35.75, 37.42, 31.15, 42.12]
        bul = [30, 30, 30, 28.06, 27.6, 27.23, 30.6, 27.6]

    elif id == '22':
        desc = "The Metro Manila Market was initially bad at the beginning of January, but it started to improve in February and started to become steadier in March until December. The start of the year is favourable for Rizal Market, Laguna Market, Pampanga Market, and Bulacan Market, while the latter part of the year sees a modest decline."
        veg = 'Bananas (Lakatan)'
        cav = []
        lag = [90,88.75,88.13,88.75,88.75,78.75,80,77.35,73.57,69.42,68.16,67.53]
        riz = [83.13,77.5,78.75,78.13,76.25,71.88,71.88,74.38,75,75,73.75,72.5]
        mtr = [0,0,73.22,73.48,73.11,70.21,66.86,65.73,67.53,65.78,64.13,62.27]
        pam = [93.13,89.38,88.13,88.13,86.25,83.13,76.25,76.88,67.5,66.88,66.88,68.75]
        bul = [68.75,68.75,67.5,67.5,66.25,67.5,67.5,62.97,65.69,65.69,64.33,62.97]
    
    elif id == '23':
        desc = " Beginning in February, Metro Manila Market starts to climb and fall in sales after having none in January. At the beginning of the year, the markets in Rizal, Pampanga, Cavite, and Laguna are strong; however, they decline from May to June before rising again throughout the year. On the other side, the Pampanga Market is somewhat off the beaten path and has poor sales."
        veg = 'Mangoes (Carabao)'
        mtr = [0, 0, 168, 159.51, 147.44, 139.27, 146.22, 148.68, 156.59, 153.99, 157.2, 158.87]
        bul = [140, 148.75, 135, 127.5, 97.5, 81.88, 87.5, 91.48, 96.45, 108.88, 115.84, 127.27]
        pam = [200, 148.75, 180, 165.63, 150, 128.13, 123.75, 164.38, 159.38, 169.38, 170, 175.63]
        cav = [192.5, 176.25, 160, 170, 148.75, 133.75, 141.25, 156.25, 169.49, 161.55, 161.55, 160.23]
        lag = [173.75, 190, 185, 158.75, 150, 108.75, 125, 154.1, 166.79, 160.44, 172.13, 167.65]
        riz = [224.38, 190, 166.25, 167.5, 146.25, 125, 150, 159.84, 166.97, 166.72, 167.83, 172.87]

    elif id == '24':
        desc = "As we can see from the graph, Rizal Market started to rise in the beginning of the month of April. It may have had some declines, but it continued to rise until the year's conclusion. The graph, however, ends at June and August for the markets in Cavite and Laguna. The Bulacan Market, on the other hand, maintained a consistent pattern to the end of December."
        yr = "2020"
        month = 8
        veg = "Mangoes (piko)"
        bul = [107.69, 88, 95.71, 126.49, 122.5, 140, 132.82, 126.41]
        cav = [95.81, 91.81, 115.26]
        lag = [90.91, 70.89, 74.44, 80]
        riz = [138.67, 139.17, 153.33, 160, 183.33, 178.67, 170, 194.17]
        mtr = []
        pam = []

    elif id == '25':
        yr = '2020'
        desc = "The price from the month of April had a sudden increase in its price and it remained high until the end of the year. The areas that increased the price are Metro Manila, Bulacan, Pampanga, Cavite, Laguna and Rizal. There was no change in its price until the end of the year and it still remained high."
        veg = 'Pineapple'
        month = 8
        cav = [55.32, 55.54, 55.2, 54.59, 55.71, 58.75, 73.57, 64.47]
        lag = [84.71, 72, 66.67, 66.47, 67.5, 67.5, 70, 81.9]
        riz = [63, 72.5, 67.78, 65.83, 65.83, 66, 69.17, 68.33]
        mtr = [70.94, 72.74, 65.11, 69.86, 68.85, 65.42, 66.83, 68.34]
        pam = [77.46, 73.45, 67.75, 66.75, 68.45, 80.2, 81.73, 91.31]
        bul = [67.46, 54.69, 54.07, 54.75, 55.31, 56.67, 55.85, 57.08]
    
    elif id == '26':
        desc = "When it comes to the price of Mandarin, Pampanga has the net price play from the month of May to November. The same is true in the area of ​​Metro Manila, Bulacan and Rizal where there is an increase and decrease in the price but it returns at the end of the year."
        veg = 'Mandarins'
        mtr = [50.99, 51.55, 51.54, 50.36, 49.86, 51.15, 49.02, 54.88, 60.93, 59.76, 55.08, 53.65]
        bul = [46.25, 43.75, 47.5, 48.75, 47.5, 48.75, 47.5, 47.5, 48.75, 52.5, 52.5, 52.5]
        pam = [68.75, 61.88, 58.75, 59.38, 60, 69.38, 68.75, 78.13, 69.38, 78.13, 66.25, 66.25]
        riz = [47.5, 46.88, 50.63, 51.25, 51.88, 51.88, 51.88, 55, 55, 51.88, 48.75, 51.25]
        cav = []
        lag = []

    elif id == '27':
        desc = "The beginning of January to July and the beginning of August to the end of the year December begins to grow and decline of the sales at the Bulacan Market, Pampanga Market, Cavite Market, Laguna Market, and Rizal Market. The Metro Manila Market has a rocky start to the year, improves through February, and then starts to become more stable toward the conclusion of the year."
        veg = 'Carrot'
        mtr = [0,0,78.44, 65.47, 63, 62.87, 69.03, 93.73, 75.63, 71.81, 98.58, 75.7]
        bul = [131.88, 88.38, 64.13, 53.75, 47, 43.13, 36.75, 64.02, 88.22, 56.57, 98.58, 74.11]
        pam = [137.5, 98.13, 71.25, 67.13, 63.38, 53.75, 61.88, 108.75, 137.5, 106.88, 109.38, 103.13]
        cav = [134.38, 124.38, 105, 86.25, 92.5, 72.88, 75.63, 106.88, 145.98, 91.24, 129.04, 125.13]
        lag = [141.25, 113.75, 82.5, 63.75, 55, 62.5, 62.5, 93.34, 150.06, 108.35, 132.5, 122.91]
        riz = [154.38, 118.75, 99.38, 76.25, 68.75, 66.25, 71.25, 102.88, 141, 103.75, 143.75, 111.88]
        

    return render_template('price_info_chart.html', veg=veg, mtr=mtr, bul=bul, pam=pam,cav=cav,lag=lag,riz=riz, desc=desc, yr=yr, month=month, user=user)
    
@app.route('/market_info')
def market_info_page():
    if 'user' in session:
        user = session['user']
        return render_template('market_info_chart.html', user=user)
    else:
        return render_template('login_page.html')
    
    
@app.route('/marketchart', methods=['POST'])
def market_chart():
    data = [0,0,0,0,0,0,0,0,0,0,0,0]
    mrkt = ""
    text = ""
    text1 = ""
    text2 = ""
    month = 12
    year = 2021
    loc = request.form.get("location")
    com = request.form.get("commodities")

    #COCONUTS
    if loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Coconuts':
        text2 = "The graph shows the prices of Coconuts last 2021. The price of coconut start at 28.4 in January, 28.35 in February and 28.37 in March. During summer season the price of Coconut in April is 28.37 and 28.69 in May. When the rainy season comes, the prices of Coconuts in June is 28.48, 28.43 in July, 28.37 in August. During the Christmas season the price of Coconuts in September is 28.82, 29.07 in October, 29.95 in November and 29.57 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [28.4, 28.35, 28.37, 28.37, 28.69, 28.48, 28.43, 28.37, 28.82, 29.07, 29.05, 29.57]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Coconuts':
        text2 = "The graph shows the prices of Coconuts last 2021. The price of coconut start at 31.88 in January, 32.5 in February and 32.5 in March. During summer season the price of Coconut in April is 32.5 and 32.53 in May. When the rainy season comes, the prices of Coconuts in June is 32.5, 32.5 in July, 32.5 in August. During the Christmas season the price of Coconuts in September is 32.5, 32.5 in October, 31.88 in November and 31.88 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [31.88, 32.5, 32.5, 32.5, 32.53, 32.5, 32.5, 32.5, 32.5, 32.5, 31.88, 31.88]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Coconuts':
        text2 = "The graph shows the prices of Coconuts last 2021. The price of coconut start at 36.25 in January, 34.38 in February and 31.88 in March. During summer season the price of Coconut in April is 32.5 and 33.75 in May. When the rainy season begin, the prices of Coconuts in June is 34.38, 34.38 in July and 34.38 in August. During the Christmas season the price of Coconuts in September is 34.38, 33.13 in October, 33.13 in November and 33.13 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [36.25, 34.38, 31.88, 32.5, 33.75, 34.38, 34.38, 34.38, 34.38, 33.13, 33.13, 33.13]

    elif loc == 'Laguna, Laguna Market' and com == 'Coconuts':
        text2 = "The graph shows the prices of Coconuts last 2021. The price of coconut start at 25 in January, 25 in February and 25 in March. During summer season the price of Coconut in April is 25.25 and 25.5 in May. When the rainy season begin, the prices of Coconuts in June is 25.5, 25.5 in July and  25.5 in August. During the Christmas season the price of Coconuts in September is 25.5, 25.5 in October, 25.5 in November and 26.14 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data = [25, 25, 25, 25.25, 25.5, 25.5, 25.5, 25.5, 25.5, 25.5, 25.5, 26.14]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Coconuts':
        text2 = "The graph shows the prices of Coconuts last 2021. The price of coconut start at 25 in January, 24.38 in February and 24.37 in March. During summer season the price of Coconut in April is 25.5 and 25.88 in May. When the rainy season begin, the prices of Coconuts in June is 26.88, 26.88 in July and 26.88 in August. During the Christmas season the price of Coconuts in September is 26.88, 26.88 in October, 26.88 in November and 26.88 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [25, 24.38, 24.37, 25.5, 25.88, 26.88, 26.88, 26.88, 26.88, 26.88, 26.88, 26.88]
    
    
    elif loc == 'Cavite, Cavite Market' and com == 'Coconuts':
        text2 = "The graph shows the prices of Coconuts last 2021. The price of coconut start at 26.25 in January, 26.25 in February and 28.13 in March. During summer season the price of Coconut in April is 27.5 and 27.5 in May. When the rainy season begin, the prices of Coconuts in June is 28.13, 26.88 in July and  25.63 in August. During the Christmas season the price of Coconuts in September is 24.81, 24.81 in October, 24.19 in November and 24.81 in December."
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [26.25, 26.25, 28.13, 27.5, 27.5, 28.13, 26.88, 25.63, 24.81, 24.81, 24.19, 24.81]
    #CABBAGE 
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Cabbage':
        text2 = "The graph shows the prices of cabbages last 2021. The price of Cabbage start at 70.02 in March. During summer season the price of Cabbage in April is 60.89, and 55.92 in May. When the rainy season begin, the prices of Onion in June is 65.07, 85.08 in July and 117.47 in August. During the Christmas season the price of Onions in September is 95.83, 77.36 in October, 76.7 in November and 56.86 in December."
        month = 10
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [70.02, 60.89, 55.92, 65.07,85.08, 117.47,95.83,77.36,76.7,56.86]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Cabbage':
        text2 = "The graph shows the prices of cabbages last 2021. The price of Cabbage start at 160 in January, 114.63 in February and 55.63 in March. During summer season the price of Cabbage in April is 43.75, and 43.25 in May. When the rainy season begin, the prices of Cabbage in June is 35.25, 50.25 in July and 90.59 in August. During the Christmas season the price of Cabbage in September is 110.4, 111.43 in October, 96.99 in November and 45.4 in December"
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [160, 114.63, 55.63, 43.75, 43.25,35.25,50.25, 90.59,110.4,111.43,96.99,45.4]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Cabbage':
        text2 = "The graph shows the prices of cabbages last 2021. The price of Cabbage start at 133.75 in January, 112.5 in February and 68.75 in March. During summer season the price of Cabbage in April is 49.38, and 33.75 in May. When the rainy season begin, the prices of Cabbage in June is 33.13, 38.75 in July and 60.13 in August. During the Christmas season the price of Cabbage in September is 136.88, 88.75 in October, 82.5 in November and 56.88 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [133.75, 112.5, 68.75, 49.38, 33.75,33.13,38.75, 60.63,136.88,88.75,82.5,56.88]

    elif loc == 'Laguna, Laguna Market' and com == 'Cabbage':
        text2 = "The graph shows the prices of cabbages last 2021. The price of Cabbage start at 186.25  in January, 131.25 in February and 81.25 in March. During summer season the price of Cabbage in April is 60, and 53.13 in May. When the rainy season begin, the prices of Cabbage in June is 55, 81.25 in July and 132.5 in August. During the Christmas season the price of Cabbage in September is 103.13, 111.25 in October, 116.25 in November and 76.25 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data = [186.25, 131.25, 81.25, 60, 53.13, 55, 81.25, 132.5,103.13,111.25,116.25,76.25]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Cabbage':
        text2 = "The graph shows the prices of cabagges last 2021. The price of Cabbage start at 183.13  in January, 141.25 in February and 69.38 in March. During summer season the price of Cabbage in April is 52.5, and 50.63 in May. When the rainy season begin, the prices of Cabbage in June is 60, 82.5 in July and 134.38 in August. During the Christmas season the price of Cabbage in September is 126.13, 98.88 in October, 116 in November and 69.88 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [183.13, 141.25, 69.38, 52.5, 50.63, 60, 82.5, 134.38,126.13,98.88,116,69.88]
    
    
    elif loc == 'Cavite, Cavite Market' and com == 'Cabbage':
        text2 = "The graph shows the prices of cabbages last 2021. The price of Cabbage start at 195 in January, 149.38 in February and 90 in March. During summer season the price of Cabbage in April is 60, and 71.25 in May. When the rainy season begin, the prices of Cabbage in June is 62, 75.63 in July and 128.75 in August. During the Christmas season the price of Cabbage in September is 179.65, 127.25 in October, 163.93 in November and 102.25 in December."
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [195, 149.38, 90, 60, 71.25, 62, 75.63, 128.75,179.65,127.25,163.93,102.25]

    #LATUNDAN
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Bananas (Lantundan)':
        text2 = "Data is not available in Metro Manila Market"
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [0,0,0,0,0,0,0,0,0,0,0]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Bananas (Lantundan)':
        text2 = "Data is not available in Bulacan Market"
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [0,0,0,0,0,0,0,0,0,0,0]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Bananas (Lantundan)':
        text2 = "Data is not available in Pampanga Market"
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [0,0,0,0,0,0,0,0,0,0,0]


    elif loc == 'Laguna, Laguna Market' and com == 'Bananas (Lantundan)':
        text2 = "The graph shows the prices of banana(Latundan) last 2021. The price of Banana(Latundan) start at 62.5 in January, 62.5 in February and 63.75 in March. During summer season the price of Banana(Latundan) in April is 62.5, and 62.5 in May. When the rainy season begin, the prices of Banana(Latundan) in June is 62.5, 61.88 in July and 59.18 in August. During the Christmas season the price of Banana(Latundan) in September is 57.83, 55.98 in October, 55.13 in November and 54.27 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data =  [62.5, 62.5, 63.75, 62.5, 62.5, 62.5, 61.88, 59.18, 57.83, 55.98, 55.13, 54.27]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Bananas (Lantundan)':
        text2 = "The graph shows the prices of banana(Latundan) last 2021. The price of Banana(Latundan) start at 55 in January, 52.5 in February and 52.5 in March. During summer season the price of Banana(Latundan) in April is 58.13, and 55 in May. When the rainy season begin, the prices of Banana(Latundan) in June is 53.13, 52.5 in July and 63.88 in August. During the Christmas season the price of Banana(Latundan) in September is 63.5, 63.13 in October, 64.4 in November and 63.76 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [55,52.5,52.5,58.13,55,53.13,52.5,63.88,63.5,63.13,64.4,63.76]
    
    elif loc == 'Cavite, Cavite Market' and com == 'Bananas (Lantundan)':
        text2 = "The graph shows the prices of Banana (Latundan) last 2021. The price of Banana(Latundan) start at 50.63  in January, 51.25 in February and 50.63 in March. During summer season the price of Banana(Latundan) in April is 51.25, and 50.63 in May. When the rainy season begin, the prices of Banana(Latundan) in June is 48.13, 43.25 in July and 52.5 in August. During the Christmas season the price of Banana(Latundan) in September is 50, 54.34 in October, 52.5 in November and 49.38 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [50.63,51.25,50.63,51.25,50.63,48.13,43.25,52.5,50,54.38,52.5,49.38]

    #TOMATO
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Tomatoes':
        text2 = "The graph shows the prices of tomatoes last 2021. The price of Tomatoes start at 38.64 in March. During summer season the price of Tomatoes in April is 36.46, and 37.01 in May. When the rainy season begin, the prices of Onion in June is 60.68, 93.19 in July and 92.6 in August. During the Christmas season the price of Tomatoes in September is 78.79, 59.92 in October, 58.12 in November and 57.38 in December."
        month = 10
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [38.64, 36.46, 37.01, 60.68, 93.19, 92.6, 78.79, 59.92, 58.12, 57.38]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Tomatoes':
        text2 = "The graph shows the prices of tomatoes last 2021. The price of Tomatoes start at 136.25 in January, 52.5 in February and 23.13 in March. During summer season the price of Tomatoes in April is 19.75, and 23.88 in May. When the rainy season begin, the prices of Tomatoes in June is 24.63, 69 in July and 73.05 in August. During the Christmas season the price of Tomatoes in September is 57.8, 37.86 in October, 37.86 in November and 31.14 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [136.25, 52.5, 23.13, 19.75, 23.88, 24.63, 69, 73.05, 57.8, 37.86, 37.86, 31.14]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Tomatoes':
        text2 = "The graph shows the prices of tomatoes last 2021. The price of Tomatoes start at 158.13 in January, 41.25 in February and 21.38 in March. During summer season the price of Tomatoes in April is 18.25, and 22.63 in May. When the rainy season begin, the prices of Tomatoes in June is 33.75, 56.75 in July and 82.83 in August. During the Christmas season the price of Tomatoes in September is 69.85, 61.2 in October, 48.21 in November and 41.42 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [158.13, 41.25, 21.38, 18.25, 22.63, 33.75, 56.75, 82.83, 69.85, 61.2, 48.21, 41.42]

    elif loc == 'Laguna, Laguna Market' and com == 'Tomatoes':
        text2 = "The graph shows the prices of tomatoes last 2021. The price of Tomatoes start at 146.25 in January, 75 in February and 37.5 in March. During summer season the price of Tomatoes in April is 25.63, and 29.38 in May. When the rainy season begin, the prices of Tomatoes in June is 39.38, 90 in July and 97.4 in August. During the Christmas season the price of Tomatoes in September is 90.93, 62.24 in October, 50.21 in November and 46.97 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data = [146.25, 75, 37.5, 25.63, 29.38, 39.38, 90, 97.4, 90.93, 62.24, 50.21, 46.97]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Tomatoes':
        text2 = "Data is not available in Rizal Market"
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [0,0,0,0,0,0,0,0,0,0,0,0]
    
    
    elif loc == 'Cavite, Cavite Market' and com == 'Tomatoes':
        text2 = "Data is not available in Cavite Market"
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [0,0,0,0,0,0,0,0,0,0,0,0]

    #ONIONS WHITE
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Onions (White)':
        text2 = "The graph shows the prices of Onion(White) last 2020. The price of Onion (White) starts at 79.02 in May. When the rainy season comes, the prices of Onion (White) in June is 76.68, 70.81 in July, 75.49 in August. During the Christmas season the price Onion(White) in September is 90.5, 95.61 in October, 92.66 in November and 91.33 in December."
        month = 8
        year = 2020
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [79.02, 76.68, 70.81, 75.49, 90.5, 95.61, 92.66, 91.33]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Onions (White)':
        text2 = "The graph shows the prices of Onion(White) last 2020. The price of Onion(White) starts at 68.77 in May. When the rainy season comes, the prices of Onion(White) in June is 72, 67.43 in July, 68 in August. During the Christmas season the price of Onion(White) in September is 78.31, 104.92 in October, 107.85 in November and 95.54 in December."
        month = 8
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [68.77, 72, 67.43, 68, 78.31, 104.92, 107.85, 95.54]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Onions (White)':
        text2 = "The graph shows the prices of Onion(White) last 2020. The price of Onion(White) starts at 55.69 in May. When the rainy season comes, the prices of Onion(White) in June is 67.68, 62.11 in July, 76.06 in August. During the Christmas season the price of Onion(White) in September is 116.38, 137.97 in October, 86.9 in November and 71.08 in December."
        month = 8
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [55.69, 67.68, 62.11, 76.03, 116.38, 137.97, 86.9, 71.08]

    elif loc == 'Laguna, Laguna Market' and com == 'Onions (White)':
        text2 = "The graph shows the prices of Onion(White) last 2020. The price of Onion(White) starts at 72.47 in May. When the rainy season comes, the prices of Onion(White) in June is 84, 81.56 in July, 77.25 in August. During the Christmas season the price of Onion(White) in September is 89, 96.78 in October, 101.38 in November and 103.67 in December."
        month = 8
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data = [72.47, 84, 81.56, 77.25, 89, 96.78, 101.38, 103.67]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Onions (White)':
        month = 8
        text2 = "Data is not available in Rizal Market"
        text = " Price in "
        year = 2020
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [0,0,0,0,0,0,0,0,0,0,0,0]
    
    elif loc == 'Cavite, Cavite Market' and com == 'Onions (White)':
        text2 = "The graph shows the prices of Onion(White) last 2020. The price of Onion(White) starts at 67.92 in May. When the rainy season comes, the prices of Onion(White) in June is 69.27, 66.95 in July, 65.18 in August. During the Christmas season the price of Onion(White) in September is 89.1, 74.78 in October, 78.38 in November and 76.73 in December."
        month = 8
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [67.92, 69.27, 66.95, 65.18, 89.1, 74.78, 78.38, 76.73]

    #BANANA SABA   
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Bananas (Saba)':
        text2 = "The graph shows the prices of Banana (saba) last 2020. The price of Banana (saba) starts at 52.27 in May. When the rainy season comes, the prices of Banana (saba) in June is 53.21, 49.05 in July, and 51.74 in August. During the Christmas season the price of Banana (saba) in September is 51.11, 50.73 in October, 50.74 in November and 50.59 in December."
        month = 8
        year = 2020
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [52.27, 53.21, 49.05, 51.74, 51.11, 50.73, 50.74, 50.59]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Bananas (Saba)':
        text2 = "The graph shows the prices of Banana (saba) last 2020. The price of Banana (saba) starts at 36 in May. When the rainy season comes, the prices of Banana (saba) in June is 36, 36 in July, and 36 in August. During the Christmas season the price of Banana (saba) in September is 36, 36 in October, 36 in November and 39.08 in December."
        year = 2020
        month = 8
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [36, 36, 36, 36, 36, 36, 36, 39.08]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Bananas (Saba)':
        text2 = "The graph shows the prices of Banana (saba) last 2020. The price of Banana (saba) starts at 42.31 in May. When the rainy season comes, the prices of Banana (saba) in June is 39.49, 37.14 in July, and 35.3 in August. During the Christmas season the price of Banana (saba) in September is 36.17, 36.12 in October, 39.03 in November and 39.91 in December."
        year = 2020
        month = 8
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [42.31, 39.49,37.14, 35.3, 36.17, 36.12, 39.03, 39.03, 39.91]

    elif loc == 'Laguna, Laguna Market' and com == 'Bananas (Saba)':
        text2 = "The graph shows the prices of Banana (saba) last 2020. The price of Banana (saba) starts at 23.81 in May. When the rainy season comes, the prices of Banana (saba) in June is 25.89, 25 in July, and 25 in August. During the Christmas season the price of Banana (saba) in September is 26.53, 28.17 in October, 29.5 in November and 30.39 in December."
        year = 2020
        month = 8
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data =  [23.81, 25.89, 25, 25, 26.53, 28.17, 29.5, 30.39]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Bananas (Saba)':
        text2 = "The graph shows the prices of Banana (saba) last 2020. The price of Banana (saba) starts at 47.67 in May. When the rainy season comes, the prices of Banana (saba) in June is 52.5, 51.11 in July, and 48.75 in August. During the Christmas season the price of Banana (saba) in September is 49.58, 28. 51 in October, 50.42in November and 49.58 in December."
        year = 2020
        month = 8
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [47.67, 52.5, 51.11, 48.75, 49.58, 51, 50.42, 49.58]
    
    elif loc == 'Cavite, Cavite Market' and com == 'Bananas (Saba)':
        text2 = "The graph shows the prices of Banana (saba) last 2020. The price of Banana (saba) starts at 40.47 in May. When the rainy season comes, the prices of Banana (saba) in June is 37.23, 35.92 in July, and 36.33 in August. During the Christmas season the price of Banana (saba) in September is 40.08, 40.83 in October, 40 in November and 40 in December."
        year = 2020
        month = 8
        text = " Price in "
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [40.47, 37.23, 35.92, 36.33, 40.08, 40.83, 40, 40]

    #BEANS GREEN FRESH
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Beans (Green, Fresh)':
        text2 = "The graph shows the prices of Beans (green, fresh) last 2021. The price of Beans (green, fresh) start at 74.49 in March. During summer season the price of Beans (green, fresh) in April is 74.33, and 76.64 in May. When the rainy season begins, the price of Beans (green, fresh) in June is 124.24, 93.19 in July and 93.98 in August. During the Christmas season the price of Beans (green, fresh) in September is 82.51, 100.06 in October, 105.36 in November and 81.28 in December."
        month = 10
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [74.49, 74.33, 76.64, 124.24, 93.19, 93.98, 82.51, 100.06, 105.36, 81.28]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Beans (Green, Fresh)':
        text2 = "Data is not available in Bulacan Market"
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [0,0,0,0,0,0,0,0,0,0,0,0]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Beans (Green, Fresh)':
        text2 = "The graph shows the prices of Beans (green, fresh) last 2021. The price of Beans (green, fresh) start at 117.5 in January, 85 in February and 71.88 in March. During summer season the price of Beans (green, fresh) in April is 76 and 66.25 in May. When the rainy season begins, the price of Beans (green, fresh) in June is 117.5, 111.25 in July and 108.3 in August. During the Christmas season the price of Beans (green, fresh) in September is 96.53, 108.3 in October, 123.6 in November and 77.69 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [117.5, 85, 71.88, 76, 66.25, 117.5, 111.25, 108.3, 96.53, 108.3, 123.6, 77.69]

    elif loc == 'Laguna, Laguna Market' and com == 'Beans (Green, Fresh)':
        text2 = "The graph shows the prices of Beans (green, fresh) last 2021. The price of Beans (green, fresh) start at 118.75 in January, 80 in February and 76.25 in March. During summer season the price of Beans (green, fresh) in April is 67.5 and 63.75 in May. When the rainy season begins, the price of Beans (green, fresh) in June is 115, 100 in July and 87.5 in August. During the Christmas season the price of Beans (green, fresh) in September is 78.75, 77.5 in October, 116.25 in November and 87.5 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data = [118.75, 80, 76.25, 67.5, 63.75, 115, 100, 87.5, 78.75, 77.5, 116.25, 87.5]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Beans (Green, Fresh)':
        text2 = "The graph shows the prices of Beans (green, fresh) last 2021. The price of Beans (green, fresh) start at 123.75 in January, 88.13 in February and 73.13 in March. During summer season the price of Beans (green, fresh) in April is 73.75 and 76.25 in May. When the rainy season begins, the price of Beans (green, fresh) in June is 131.25, 110.63 in July and 97.88 in August. During the Christmas season the price of Beans (green, fresh) in September is 88.75, 88.75 in October, 146.25 in November and 84.88 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [123.75, 88.13, 73.13, 73.75, 76.25, 131.25, 110.63, 97.88, 88.75, 88.75, 146.25, 84.88]
    
    elif loc == 'Cavite, Cavite Market' and com == 'Beans (Green, Fresh)':
        text2 = "The graph shows the prices of Beans (green, fresh) last 2021. The price of Beans (green, fresh) start at 150 in January, 103.75 in February and 96.25 in March. During summer season the price of Beans (green, fresh) in April is 85 and 85 in May. When the rainy season begins, the price of Beans (green, fresh) in June is 123.75, 96.88 in July and 106.63 in August. During the Christmas season the price of Beans (green, fresh) in September is 95.63, 87.5 in October, 95.63 in November and 95 in December."
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [150, 103.75, 96.25, 85, 85, 123.75, 96.88, 106.63, 95.63, 87.5, 95.63, 95]

    #STRING BEANS
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Beans (String)':
        year = 2020
        text2 = "Data is not available in Metro Manila Market"
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [0,0,0,0,0,0,0,0,0,0,0,0]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Beans (String)':
        text2 = "The graph shows the prices of Beans (string) last 2020. The price of Beans (string) starts at 82.31 in May. When the rainy season comes, the price of Beans (string) in June is 82.31, 73.57 in July, and 62.11 in August. During the Christmas season the price of Beans (string) in September is 60.46, 60.23 in October, 58.92 in November and 86.08 in December."
        year = 2020
        month = 8
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [82.31, 82.31, 73.57, 62.11, 60.46, 60.23, 58.92, 86.08]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Beans (String)':
        text2 = "The graph shows the prices of Beans (string) last 2020. The price of Beans (string) starts at 94.62 in May. When the rainy season comes, the price of Beans (string) in June is 62.52, 54.03 in July, and 40.85 in August. During the Christmas season the price of Beans (string) in September is 41.42, 54.03 in October, 79.83 in November and 117.52 in December."
        year = 2020
        month = 8
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [94.62, 62.52, 54.03, 40.85, 41.42, 54.03, 79.83,117.52]

    elif loc == 'Laguna, Laguna Market' and com == 'Beans (String)':
        text2 = "The graph shows the prices of Beans (string) last 2020. The price of Beans (string) starts at 85.18 in May. When the rainy season comes, the price of Beans (string) in June is 69.33, 48.11 in July, and 43 in August. During the Christmas season the price of Beans (string) in September is 50.89, 64.67 in October, 112.5 in November and 88.11 in December."
        year = 2020
        month = 8
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data = [85.18, 69.33, 48.11, 43, 50.89, 64.67, 112.5,  88.11]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Beans (String)':
        text2 = "The graph shows the prices of Beans (string) last 2020. The price of Beans (string) starts at 112.07 in May. When the rainy season comes, the price of Beans (string) in June is 71.67, 86.67 in July, and 91.67 in August. During the Christmas season the price of Beans (string) in September is 100.71, 121.89 in October, 183.33 in November and 128.65 in December."
        year = 2020
        month = 8
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [112.07, 71.67, 86.67, 91.67, 100.71, 121.89, 183.33, 128.65]
    
    
    elif loc == 'Cavite, Cavite Market' and com == 'Beans (String)':
        text2 = "The graph shows the prices of Beans (string) last 2020. The price of Beans (string) starts at 95.29 in May. When the rainy season comes, the price of Beans (string) in June is 74.23, 43.2 in July, and 59.25 in August. During the Christmas season the price of Beans (string) in September is 54.53, 74.82 in October, 113.08 in November and 85.36 in December."
        year = 2020
        month = 8
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [95.29, 74.23,43.2, 59.25, 54.53, 74.82, 113.08, 85.36]

    #BITTERMELON
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Bitter Melon':
        text2 = "The graph shows the prices of Bitter melon last 2021. The price of Bitter melon starts at 72.93 in March. During summer season the price of Bitter melon in April is 67.28, and 61.42 in May. When the rainy season begins, the price of Bittermellon in June is 75.4, 82.06 in July and 99.16 in August. During the Christmas season the price of Bitter melon in September is 85.94, 84.47 in October, 64.96 in November and 78.93 in December."
        month = 10
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [72.93,67.28,61.42,75.4,82.06,99.16,85.94,84.47,64.96,78.93]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Bitter Melon':
        text2 = "The graph shows the prices of Bitter melon last 2021. The price of Bitter melon starts at 128 in January, 92.5 in February and 71 in March. During summer season the price of Bitter melon in April is 60 and 50.75 in May. When the rainy season begins, the price of Bitter melon in June is 56.25, 63.5 in July and 123.75 in August. During the Christmas season the price of Bitter melon in September is 66.25, 68.75 in October, 69.5 in November and 67.5 in December"
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [128,92.5,71,60,50.75,56.25,63.5,123.75,66.25,68.75,69.5,67.5]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Bitter Melon':
        text2 = "The graph shows the prices of Bitter melon last 2021. The price of Bitter melon starts at 105 in January, 86.25 in February and 63.13 in March. During summer season the price of Bitter melon in April is 68.38 and 48.13 in May. When the rainy season begins, the price of Bitter melon in June is 52.5, 60 in July and 81.51 in August. During the Christmas season the price of Bitter melon in September is 61.7, 66.23 in October, 62.26 in November and 75.62 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [105,86.25,63.13,68.38,48.13,52.5,60,81.51,61.7,66.23,62.26,75.62]

    elif loc == 'Laguna, Laguna Market' and com == 'Bitter Melon':
        text2 = "The graph shows the prices of Bitter melon last 2021. The price of Bitter melon starts at 135 in January, 96.25 in February and 77.5 in March. During summer season the price of Bitter melon in April is 62.5 and 52.5 in May. When the rainy season begins, the price of Bitter melon in June is 63.75, 70 in July and 104.77 in August. During the Christmas season the price of Bitter melon in September is 86.92, 87.62 in October, 73.25 in November and 63.51 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data =  [135,96.25,77.5,62.5,52.5,63.75,70,104.77,86.92,87.62,73.25,63.51]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Bitter Melon':
        text2 = "The graph shows the prices of Bitter melon last 2021. The price of Bitter melon starts at 168.75 in January, 101.88 in February and 75 in March. During summer season the price of Bitter melon in April is 70.63 and 59.38 in May. When the rainy season begins, the price of Bitter melon in June is 74.38, 78.75 in July and 121.88 in August. During the Christmas season the price of Bitter melon in September is 86.25, 105.38 in October, 73.88 in November and 79.63 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data =  [168.75, 101.88, 75, 70.63, 59.38, 74.38, 78.75, 121.88, 86.25,105.38,73.88,79.63]
    
    elif loc == 'Cavite, Cavite Market' and com == 'Bitter Melon':
        text2 = "The graph shows the prices of Bitter melon last 2021. The price of Bitter melon starts at 156.25 in January, 125 in February and 92.5 in March. During summer season the price of Bitter melon in April is 80.63 and 83.75 in May. When the rainy season begins, the price of Bitter melon in June is 73.13, 77.5 in July and 106.25 in August. During the Christmas season the price of Bitter melon in September is 103.66, 119.65 in October, 88.07 in November and 100.87 in December."
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [156.25, 125, 92.5, 80.63, 83.75, 73.13, 77.5, 106.25, 103.66, 119.65, 88.07, 100.87]

    #BOTTLEGOURD
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Bottle Gourd':
        text2 = "The graph shows the prices of Bottle gourd last 2021. The price of Bottle gourd starts at 49.69 in January, 39.56 in February and 34.36 in March. During summer season the price of Bottle gourd in April is 31.64 and 32.25 in May. When the rainy season begins, the price of Bottle gourd in June is 36.47, 40.11 in July and 45.73 in August. During the Christmas season the price of Bottle gourd in September is 42.34, 35 in October, 29.55 in November and 29.03 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [49.69, 39.56, 34.36, 31.64, 32.25, 36.47, 40.11, 45.73, 42.34, 35, 29.55, 29.03]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Bottle Gourd':
        text2 = "The graph shows the prices of Bottle gourd last 2021. The price of Bottle gourd starts at 45.63 in January, 29.38 in February and 22.25 in March. During summer season the price of Bottle gourd in April is 21.25 and 20.5 in May. When the rainy season begins, the price of Bottle gourd in June is 21.88, 23.75 in July and 31.75 in August. During the Christmas season the price of Bottle gourd in September is 32, 28.75 in October, 28.13 in November and 25 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [45.63, 29.38, 22.25, 21.25, 20.5, 21.88, 23.75, 31.75, 32, 28.75, 28.13, 25]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Bottle Gourd':
        text2 = "The graph shows the prices of Bottle gourd last 2021. The price of Bottle gourd starts at 51.25 in January, 38.63 in February and 29.38 in March. During summer season the price of Bottle gourd in April is 26.25 and 25.63 in May. When the rainy season begins, the price of Bottle gourd in June is 21.25, 22.5 in July and 27.25 in August. During the Christmas season the price of Bottle gourd in September is 30.63, 31.63 in October, 25 in November and 26.88 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [51.25, 38.63, 29.38, 26.25, 25.63, 21.25, 22.5, 27.25, 30.63, 31.63, 25, 26.88]

    elif loc == 'Laguna, Laguna Market' and com == 'Bottle Gourd':
        text2 = "The graph shows the prices of Bottle gourd last 2021. The price of Bottle gourd starts at 34.38 in January, 27.5 in February and 21.88 in March. During summer season the price of Bottle gourd in April is 20.63 and 20.63 in May. When the rainy season begins, the price of Bottle gourd in June is 20, 23.13 in July and 25.79 in August. During the Christmas season the price of Bottle gourd in September is 26.94, 25.61 in October, 26.14 in November and 25.69 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data = [34.38, 27.5, 21.88, 20.63, 20.63, 20, 23.13, 25.79, 26.94, 25.61, 26.14, 25.69]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Bottle Gourd':
        text2 = "The graph shows the prices of Bottle gourd last 2021. The price of Bottle gourd starts at 45.49 in January, 38.93 in February and 29.37 in March. During summer season the price of Bottle gourd in April is 26.4 and 24.58 in May. When the rainy season begins, the price of Bottle gourd in June is 29.83. 34.23 In July and 38.43 in August. During the Christmas season the price of Bottle gourd in September is 40.47, 37.38 in October, 31.56 in November and 28.59 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [45.49, 38.93, 29.37, 26.4, 24.58, 29.83, 34.23, 38.43, 40.47, 37.38, 31.56, 28.59]
    
    elif loc == 'Cavite, Cavite Market' and com == 'Bottle Gourd':
        text2 = "The graph shows the prices of Bottle gourd last 2021. The price of Bottle gourd starts at 33.13 in January, 29.13 in February and 26.25 in March. During summer season the price of Bottle gourd in April is 24.38 and 27.5 in May. When the rainy season begins, the price of Bottle gourd in June is 28.13, 27.5 in July and 33.75 in August. During the Christmas season the price of Bottle gourd in September is 32.59, 26.77 in October, 26.8 in November and 27.36 in December."
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [33.13, 29.13, 26.25, 24.38, 27.5, 28.13, 27.5, 33.75, 32.59, 26.77, 26.89, 27.36]

    #CABBAGE CHINESE
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Cabbage (Chinese)':
        text2 = "Data is not available in Metro Manila Market"
        year = 2020
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [0,0,0,0,0,0,0,0,0,0,0,0]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Cabbage (Chinese)':
        text2 = "The graph shows the prices of Cabbage (Chinese) last 2020. The price of Cabbage (Chinese) starts at 58.46 in May. When the rainy season comes, the price of Cabbage (Chinese) in June is 61.08, 55.57 in July, and 55.15 in August. During the Christmas season the price of Cabbage (Chinese) in September is 56.46, 56 in October, 94.15 in November and 70.08 in December."
        month = 8
        year = 2020
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [58.46, 61.08, 55.57, 55.15, 56.46, 56, 94.15, 70.08]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Cabbage (Chinese)':
        text2 = "The graph shows the prices of Cabbage (Chinese) last 2020. The price of Cabbage (Chinese) starts at 45.69 in May. When the rainy season comes, the price of Cabbage (Chinese) in June is 45.72, 52.31 in July, and 45.28 in August. During the Christmas season the price of Cabbage (Chinese) in September is 42.3, 59.23 in October, 96.53 in November and 47.51 in December."
        month = 8
        year = 2020
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [45.69, 45.72, 52.31, 45.28, 42.3, 59.23 ,96.53, 47.51]

    elif loc == 'Laguna, Laguna Market' and com == 'Cabbage (Chinese)':
        text2 = "The graph shows the prices of Cabbage (Chinese) last 2020. The price of Cabbage (Chinese) starts at 48.12 in May. When the rainy season comes, the price of Cabbage (Chinese) in June is 59.44, 49.89 in July, and 57.75 in August. During the Christmas season the price of Cabbage (Chinese) in September is 57.33, 60.56 in October, 117.38 in November and 86.22 in December."
        month = 8
        year = 2020
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data = [48.12, 59.44, 49.89, 57.75, 57.33, 60.56, 117.38, 86.22]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Cabbage (Chinese)':
        text2 = "The graph shows the prices of Cabbage (Chinese) last 2020. The price of Cabbage (Chinese) starts at 71.67 in May. When the rainy season comes, the price of Cabbage (Chinese) in June is 83.33, 71.11 in July, and 89.17 in August. During the Christmas season the price of Cabbage (Chinese) in September is 77.5, 151.33 in October, 162.5 in November and 88.08 in December."
        month = 8
        year = 2020
        text2 = "Data is not available in Rizal Market"
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [71.67, 83.33, 71.11, 89.17, 77.5, 151.33, 162.5, 88.08]
    
    elif loc == 'Cavite, Cavite Market' and com == 'Cabbage (Chinese)':
        text2 = "The graph shows the prices of Cabbage (Chinese) last 2020. The price of Cabbage (Chinese) starts at 63.02 in May. When the rainy season comes, the price of Cabbage (Chinese) in June is 66.77, 50.92 in July, and 62.2 in August. During the Christmas season the price of Cabbage (Chinese) in September is 44.36, 75 in October, 123.78 in November and 55.3 in December."
        month = 8
        year = 2020
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data =[63.02, 66.77, 50.92, 62.2, 44.36, 75, 123.78, 55.3]
    
    #CALAMANSI
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Calamansi':
        text2 = "The graph shows the prices of Calamansi last 2021. The price of Calamansi starts at 89.04 in March. During summer season the price of Calamansi in April is 90.69, and 101.17 in May. When the rainy season begins, the price of Calamansi in June is 76.16, 66.36 in July and 66.87 in August. During the Christmas season the price of Calamansi in September is 63.3, 61.6 in October, 90.23 in November and 85.14 in December."
        month = 10
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [89.04, 90.69, 101.17, 76.16, 66.36, 66.87, 63.3, 61.6, 90.23, 85.14]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Calamansi':
        text2 = "The graph shows the prices of Calamansi last 2021. The price of Calamansi starts at 63.75 in January, 91.75 in February and 77.5 in March. During summer season the price of Calamansi in April is 70 and 87.5 in May. When the rainy season begins, the price of Calamansi in June is 70. 53.75 In July and 54.46 in August. During the Christmas season the price of Calamansi in September is 48.97, 47.99 in October, 68.67 in November and 65.01 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [63.75, 91.75, 77.5, 70, 87.5, 70, 53.75, 54.46, 48.97, 47.99, 68.67, 65.01]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Calamansi':
        text2 = "The graph shows the prices of Calamansi last 2021. The price of Calamansi starts at 52.5 in January, 44.43 in February and 101.88 in March. During summer season the price of Calamansi in April is 75.63 and 98.75 in May. When the rainy season begins, the price of Calamansi in June is 66.88. 61.88 In July and 55.93 in August. During the Christmas season the price of Calamansi in September is 58.57, 31.56 in October, 48.9 in November and 66.06 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [52.5, 44.43, 101.88, 75.63, 98.75, 66.88, 61.88, 55.93, 58.57, 31.56, 48.9, 66.06]

    elif loc == 'Laguna, Laguna Market' and com == 'Calamansi':
        text2 = "Data is not available in Laguna Market"
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data = [0,0,0,0,0,0,0,0,0,0,0,0]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Calamansi':
        text2 = "Data is not available in Rizal Market"
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [0,0,0,0,0,0,0,0,0,0,0,0]
    
    elif loc == 'Cavite, Cavite Market' and com == 'Calamansi':
        text2 = "Data is not available in Cavite Market"
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [0,0,0,0,0,0,0,0,0,0,0,0]

    #CHOKO
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Choko':
        text2 = "The graph shows the prices of Choko last 2021. The price of Choko starts at 36.94 in January, 35.06 in February and 30.07 in March. During summer season the price of Choko in April is 30.72 and 32.71 in May. When the rainy season begin, the prices of Choko in June is 39.51, 44.97 in July and 50.58 in August. During the Christmas season the price of Choko in September is 45.88, 31.84 in October, 29.48 in November and 30.81 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [36.94, 35.06, 30.07, 30.72, 32.71, 39.51, 44.97, 50.58, 45.88, 31.84, 29.48, 30.81]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Choko':
        text2 = "The graph shows the prices of Choko last 2021. The price of Choko starts at 27.38 in January, 27.25 in February and 20 in March. During summer season the price of Choko in April is 19.75 and 22.63 in May. When the rainy season begin, the prices of Choko in June is 24.38, 32.5 in July and 46.63 in August. During the Christmas season the price of Choko in September is 73.25, 35.75 in October, 35.63 in November and 25 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [27.38, 27.25, 20, 19.75, 22.63, 24.38, 32.5, 46.63, 73.25, 35.75, 35.63, 25]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Choko':
        text2 = "The graph shows the prices of Choko last 2021. The price of Choko starts at 32.5 in January, 47.13 in February and 29.13 in March. During summer season the price of Choko in April is 26.75 and 25.38 in May. When the rainy season begin, the prices of Choko in June is 29.25, 41.88 in July and 51.73 in August. During the Christmas season the price of Choko in September is 76.97, 52.64 in October, 37.98 in November and 37.92 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [32.5, 47.13, 29.13, 26.75, 25.38, 29.25, 41.88, 51.73, 76.97, 52.64, 37.98, 37.92]

    elif loc == 'Laguna, Laguna Market' and com == 'Choko':
        text2 = "The graph shows the prices of Choko last 2021. The price of Choko starts at 35 in January, 33.75 in February and 30 in March. During summer season the price of Choko in April is 25 and 27.5 in May. When the rainy season begin, the prices of Choko in June is 36.25, 41.25 in July and 48.29 in August. During the Christmas season the price of Choko in September is 72.62, 68.91 in October, 48.16 in November and 36.43 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data = [35, 33.75, 30, 25, 27.5, 36.25, 41.25, 48.29, 72.62, 68.91, 48.16, 36.43]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Choko':
        text2 = "The graph shows the prices of Choko last 2021. The price of Choko starts at 40.63 in January, 38.13 in February and 32.5 in March. During summer season the price of Choko in April is 30.63 and 31.25 in May. When the rainy season begin, the prices of Choko in June is 36.25, 48.75 in July and 55.25 in August. During the Christmas season the price of Choko in September is 78.38, 40.5 in October, 36.25 in November and 39 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [40.63, 38.13, 32.5, 30.63, 31.25, 36.25, 48.75, 55.25, 78.38, 40.5, 36.25, 39]
    
    elif loc == 'Cavite, Cavite Market' and com == 'Choko':
        text2 = "The graph shows the prices of Choko last 2021. The price of Choko starts at 42.14 in January, 41.43 in February and 31.25 in March. During summer season the price of Choko in April is 32.63 and 37.13 in May. When the rainy season begin, the prices of Choko in June is 40.25, 48.13 in July and 61.75 in August. During the Christmas season the price of Choko in September is 88.43, 59.28 in October, 45.08 in November and 42.61 in December."
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [42.14, 41.43, 31.25, 32.63, 37.13, 40.25, 48.13, 61.75, 88.43, 59.28, 45.08, 42.61]

    #EGGPLANTS 
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Eggplants':
        text2 = "The graph shows the prices of Eggplants last 2021. The price of Eggplants starts at 71.22 in March. During summer season the price of Eggplants in April is 66.92, and 57.97 in May. When the rainy season begin, the prices of Eggplant in June is 54.84, 62.44 in July and 85.89 in August. During the Christmas season the price of Eggplants in September is 60.67, 72.88 in October, 75.9 in November and 81.11 in December."
        month = 10
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [71.22, 66.92, 57.97, 54.84, 62.44, 85.89, 60.67, 72.88, 75.9, 81.11]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Eggplants':
        text2 = "The graph shows the prices of Eggplants last 2021. The price of Eggplants starts at 140.63 in January, 97 in February and 67.5 in March. During summer season the price of Eggplants in April is 60.13 and 43.13 in May. When the rainy season begin, the prices of Eggplants in June is 42.75, 45 in July and 108.65 in August. During the Christmas season the price of Eggplants in September is 63.65, 85.16 in October, 90 in November and 75.86 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [140.63, 97, 67.5, 60.13, 43.13, 42.75, 45, 108.65, 63.65, 85.16, 90, 75.86]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Eggplants':
        text2 = "The graph shows the prices of Eggplants last 2021. The price of Eggplants starts at 128.13 in January, 86.88 in February and 63.13 in March. During summer season the price of Eggplants in April is 55.63 and 40.63 in May. When the rainy season begin, the prices of Eggplants in June is 40.63, 43.75 in July and 65.05 in August. During the Christmas season the price of Eggplants in September is 44.9, 30.51 in October, 56.99 in November and 71.96 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [128.13, 86.88, 63.13, 55.63, 40.63, 40.63, 43.75, 65.05, 44.9, 30.51, 56.99, 71.96]

    elif loc == 'Laguna, Laguna Market' and com == 'Eggplants':
        text2 = "The graph shows the prices of Eggplants last 2021. The price of Eggplants starts at 147.5 in January, 103.75 in February and 80 in March. During summer season the price of Eggplants in April is 66.25 and 51.25 in May. When the rainy season begin, the prices of Eggplants in June is 50, 43.75 in July and 85.59 in August. During the Christmas season the price of Eggplants in September is 57.13, 67.54 in October, 72.85 in November and 53.85 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data =  [147.5, 103.75, 80, 66.25, 51.25, 50, 43.75, 85.59, 57.13, 67.54, 72.85, 53.85]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Eggplants':
        text2 = "The graph shows the prices of Eggplants last 2021. The price of Eggplants starts at 173.75 in January, 108.75 in February and 80.63 in March. During summer season the price of Eggplants in April is 71.25 and 63.75 in May. When the rainy season begin, the prices of Eggplants in June is 65.63, 56.25 in July and 105.38 in August. During the Christmas season the price of Eggplants in September is 65.5, 90.75 in October, 95 in November and 82 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [173.75, 108.75, 80.63, 71.25, 63.75, 65.63, 56.25, 105.38, 65.5, 90.75, 95, 82]
    
    elif loc == 'Cavite, Cavite Market' and com == 'Eggplants':
        text2 = "The graph shows the prices of Eggplants last 2021. The price of Eggplants starts at 141.88 in January, 110.63 in February and 90 in March. During summer season the price of Eggplants in April is 79.38 and 76.88 in May. When the rainy season begin, the prices of Eggplants in June is 56.88, 51.88 in July and 101.88 in August. During the Christmas season the price of Eggplants in September is 74.82, 98.7 in October, 126.57 in November and 109.06 in December."
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [141.88, 110.63, 90, 79.38, 76.88, 56.88, 51.88, 101.88, 74.82, 98.7, 126.57, 109.06]

    #GINGER
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Ginger':
        text2 = "The graph shows the prices of Ginger last 2021. The price of Ginger starts at 151.35 in January, 157.85 in February and 156.57 in March. During summer season the price of Ginger in April is 154.42 and 156.57 in May. When the rainy season begin, the prices of Ginger in June is 154.42, 156.4 in July and 156 in August. During the Christmas season the price of Ginger in September is 155.24, 148.63 in October, 146.87 in November and 137.18 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [151.35, 157.85, 156.57, 154.42, 156.57, 154.42, 156.4, 156, 155.24, 148.63, 146.87, 137.18]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Ginger':
        text2 = "The graph shows the prices of Ginger last 2021. The price of Ginger starts at 153.75 in January, 138.13 in February and 128.75 in March. During summer season the price of Ginger in April is 128.75 and 128.75 in May. When the rainy season begin, the prices of Ginger in June is 138.75, 118.75 in July and 133.44 in August. During the Christmas season the price of Ginger in September is 116.3, 115.08 in October, 117.53 in November and 109.58 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [153.75, 138.13, 128.75, 128.75, 128.75, 138.75, 118.75, 133.44, 116.3, 115.08, 117.53, 109.58]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Ginger':
        text2 = "The graph shows the prices of Ginger last 2021. The price of Ginger starts at 114.37 in January, 110 in February and 111.88 in March. During summer season the price of Ginger in April is 121.25 and 128.13 in May. When the rainy season begin, the prices of Ginger in June is 123.75, 125.63 in July and 132.68 in August. During the Christmas season the price of Ginger in September is 128.54, 106.15 in October, 93.31 in November and 88.94 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [114.37, 110, 111.88, 121.25, 128.13, 123.75, 125.63, 132.68, 128.54, 106.15, 93.31, 88.94]

    elif loc == 'Laguna, Laguna Market' and com == 'Ginger':
        text2 = "Data is not available in Laguna Market"
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data =  [0,0,0,0,0,0,0,0,0,0,0,0]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Ginger':
        text2 = "Data is not available in Rizal Market"
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [0,0,0,0,0,0,0,0,0,0,0,0]
    
    elif loc == 'Cavite, Cavite Market' and com == 'Ginger':
        text2 = "Data is not available in Cavite Market"
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [0,0,0,0,0,0,0,0,0,0,0,0]

    #PAPAYA
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Papaya':
        year = 2020
        text2 = "Data is not available in Metro Manila"
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [0,0,0,0,0,0,0,0,0,0,0,0]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Papaya':
        text2 = "The graph shows the prices of Papaya last 2020. The price of Papaya starts at 45.69 in May. When the rainy season comes, the prices of Papaya in June is 44.31, 45.5 in July, 44.6 in August. During the Christmas season the price of Papaya in September is 43.23, 43.38 in October, 43.85 in November and 44.62 in December."
        year = 2020
        month = 8
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [45.69, 44.31, 45.5, 44.6, 43.23, 43.38, 43.85, 44.62]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Papaya':
        text2 = "The graph shows the prices of Papaya last 2020. The price of Papaya starts at 65.85 in May. When the rainy season comes, the prices of Papaya in June is 67.12, 65.52 in July, 61.77 in August. During the Christmas season the price of Papaya in September is 61.73, 73.71 in October, 60.88 in November and 64.54 in December."
        year = 2020
        month = 8
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [65.85, 67.12, 65.52, 61.77, 61.73, 73.71, 60.88, 64.54]

    elif loc == 'Laguna, Laguna Market' and com == 'Papaya':
        text2 = "The graph shows the prices of Papaya last 2020. The price of Papaya starts at 52.21 in May. When the rainy season comes, the prices of Papaya in June is 55.63, 55.63 in July, 55.63 in August. During the Christmas season the price of Papaya in September 55.63, 55.63 in October and 55.63 in November."
        year = 2020
        month = 8
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data = [52.21, 55.63, 55.63, 55.63, 55.63, 55.63, 55.63,0]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Papaya':
        text2 = "The graph shows the prices of Papaya last 2020. The price of Papaya starts at 45 in May. When the rainy season comes, the prices of Papaya in June is 44.58, 46.11 in July, 47.5 in August. During the Christmas season the price of Papaya in September is 45, 45 in October, 45 in November and 45 in December."
        year = 2020
        month = 8
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [45, 44.58, 46.11, 47.5, 45, 45, 45, 45]
    
    elif loc == 'Cavite, Cavite Market' and com == 'Papaya':
        text2 = "The graph shows the prices of Papaya last 2020. The price of Papaya starts at 59.17 in May. When the rainy season comes, the prices of Papaya in June is 60, 58.25 in July, 59.57 in August. During the Christmas season the price of Papaya in September is 60.75, 60.59 in October, 59.53 in November and 61.33 in December."
        year = 2020
        month = 8
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [59.17, 60, 58.25, 59.57,60.75, 60.59, 59.53, 61.33]

    #SQUASH
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Squashes':
        text2 = "The graph shows the prices of Squashes last 2021. The price of Squashes starts at 101.81 in January, 81.69 in February and 52.53 in March. During summer season the price of Squashes in April is 39.5 and 35.19 in May. When the rainy season begin, the prices of Squashes in June is 35.93, 38.72 in July and 47.36 in August. During the Christmas season the price of Squashes in September is 49.83, 50.94 in October, 48.51 in November and 44.64 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [101.81, 81.69, 52.53, 39.5, 35.19, 35.93, 38.72, 47.36, 49.83, 50.94, 48.51, 44.64]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Squashes':
        text2 = "Data is not available in Bulacan Market"
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [0,0,0,0,0,0,0,0,0,0,0,0]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Squashes':
        text2 = "Data is not available in Pampanga Market"
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [0,0,0,0,0,0,0,0,0,0,0,0]

    elif loc == 'Laguna, Laguna Market' and com == 'Squashes':
        text2 = "The graph shows the prices of Squashes last 2021. The price of Squashes starts at 83.75 in January, 78.75 in February and 52.5 in March. During summer season the price of Squashes in April is 33.75 and 31.25 in May. When the rainy season begin, the prices of Squashes in June is 25, 31.88 in July and 42.5 in August. During the Christmas season the price of Squashes in September is 41.25, 44.38 in October, 35.63 in November and 34.38 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data = [83.75, 78.75, 52.5, 33.75, 31.25, 25, 31.88, 42.5, 41.25, 44.38, 35.63, 34.38]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Squashes':
        text2 = "Data is not available in Rizal Market"
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [0,0,0,0,0,0,0,0,0,0,0,0]
    
    elif loc == 'Cavite, Cavite Market' and com == 'Squashes':
        text2 = "The graph shows the prices of Squashes last 2021. The price of Squashes starts at 86.25 in January, 93.13 in February and 66.25 in March. During summer season the price of Squashes in April is 41.88 and 45.63 in May. When the rainy season begin, the prices of Squashes in June is 37.5, 34.75 in July and 46.25 in August. During the Christmas season the price of Squashes in September is 51.67, 57.08 in October, 53.75 in November and 49.76 in December"
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [86.25, 93.13, 66.25, 41.88, 45.63, 37.5, 34.75, 46.25, 51.67, 57.08, 53.75, 49.76]

    #SWEET POTATO LEAVES 
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Sweet Potato Leaves':
        text2 = "The graph shows the prices of Sweet Potato Leaves last 2020. The price of Sweet Potato Leaves starts at 56.98 in May. When the rainy season comes, the prices of Sweet Potato Leaves in June is 55.71, 51.96 in July, 52.89 in August. During the Christmas season the price of Sweet Potato Leaves in September is 52.95, 55.27 in October, 72.25in November and 78.29 in December."
        month = 8 
        year = 2020
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [56.98, 55.71, 51.96, 52.89, 52.95, 55.27, 72.25, 78.29]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Sweet Potato Leaves':
        text2 = "The graph shows the prices of Sweet Potato Leaves last 2020. The price of Sweet Potato Leaves starts at 20 in May. When the rainy season comes, the prices of Sweet Potato Leaves in June is 20, 20 in July, 20 in August. During the Christmas season the price of Sweet Potato Leaves in September is 20, 20.15 in October, 20.6 in November and 21.78 in December."
        month = 8 
        year = 2020
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [20, 20, 20, 20, 20, 20.15, 20.6, 21.78]

    elif loc == 'Bulacan, Pampanga Market' and com == 'Sweet Potato Leaves':
        text2 = "The graph shows the prices of Sweet Potato Leaves last 2020. The price of Sweet Potato Leaves starts at 36.31 in May. When the rainy season comes, the prices of Sweet Potato Leaves in June is 34.38, 32.82 in July, 33.98 in August. During the Christmas season the price of Sweet Potato Leaves in September is 37.97, 38.66 in October, 37.88 in November and 36.12 in December."
        month = 8 
        year = 2020
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [36.31, 34.38, 32.82, 33.98, 37.97, 38.66, 37.88, 36.12]

    elif loc == 'Laguna, Laguna Market' and com == 'Sweet Potato Leaves':
        text2= "The graph shows the prices of Sweet Potato Leaves last 2020. The price of Sweet Potato Leaves starts at 47.1 in May. When the rainy season comes, the prices of Sweet Potato Leaves in June is 50, 50 in July, 50 in August. During the Christmas season the price of Sweet Potato Leaves in September is 50, 50 in October, 74.65 in November and 50 in December."
        month = 8 
        year = 2020
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data = [47.1, 50, 50, 50, 50, 50, 74.65, 50, 50]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Sweet Potato Leaves':
        text2 = "The graph shows the prices of Sweet Potato Leaves last 2020. The price of Sweet Potato Leaves starts at 37.2 in May. When the rainy season comes, the prices of Sweet Potato Leaves in June is 31.25, 32.87 in July, 34.73 in August. During the Christmas season the price of Sweet Potato Leaves in September is 33.6, 35.81 in October, 50.96 in November and 75.31 in December."
        month = 8 
        year = 2020
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [37.2, 31.25, 32.87, 34.73, 33.6, 35.81, 50.96, 75.31]
    
    elif loc == 'Cavite, Cavite Market' and com == 'Sweet Potato Leaves':
        text2 = "The graph shows the prices of Sweet Potato Leaves last 2020. The price of Sweet Potato Leaves starts at 70.21 in May. When the rainy season comes, the prices of Sweet Potato Leaves in June is 65.85, 62.02 in July, 60.6 in August. During the Christmas season the price of Sweet Potato Leaves in September is 60.55, 62.22 in October, 74.65 in November and 81.59 in December."
        month = 8 
        year = 2020
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [70.21, 65.85, 62.02, 60.6, 60.55, 62.22, 74.65, 81.59]

    #WATER SPINACH 
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Water Spinach':
        text2 = "The graph shows the prices of Water Spinach last 2020. The price of water spinach starts at 63.85 in May. When the rainy season comes, the price of water spinach in June is 64.27, 57.48 in July, and 56.36 in August. During the Christmas season, the price of water spinach in September is 58.9,  63.85 in October, 97.4 in November, and 103.07 in December."
        month = 8
        year = 2020
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [63.85, 64.27, 57.48, 56.36, 58.9, 63.85, 97.4, 103.07]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Water Spinach':
        text2 = "The graph shows the prices of Water Spinach last 2020. The price of water spinach starts at 30 in May. When the rainy season comes, the price of water spinach in June is 30, 30 in July, and 28.06 in August. During the Christmas season, the price of water spinach in September is 27.6,  27.23 in October, 30.6 in November, and 27.6 in December"
        year = 2020
        month = 8
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [30, 30, 30, 28.06, 27.6, 27.23, 30.6, 27.6]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Water Spinach':
        text2 = "The graph shows the prices of Water Spinach last 2020. The price of water spinach starts at 37.92 in May. When the rainy season comes, the price of water spinach in June is 38.32,  34.6 in July, and 35.75 in August. During the Christmas season, the price of water spinach in September is 37.42,  31.15 in October, 42.12 in November, and 37.42 in December."
        year = 2020
        month = 8
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [37.92, 38.32, 37.42, 34.6, 35.75, 37.42, 31.15, 42.12]

    elif loc == 'Laguna, Laguna Market' and com == 'Water Spinach':
        text2 = "The graph shows the prices of Water Spinach last 2020. The price of water spinach starts at 44 in May. When the rainy season comes, the price of water spinach in June is 50.49, 48.52 in July, and 51.11 in August. During the Christmas season, the price of water spinach in September is 46.79,  54.44 in October, 59.72 in November, and 48.52 in December."
        year = 2020
        month = 8
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data = [44, 50.49, 48.52, 51.11, 46.79, 54.44, 59.72, 48.52]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Water Spinach':
        text2 = "The graph shows the prices of Water Spinach last 2020. The price of water spinach starts at 35.13 in May. When the rainy season comes, the price of water spinach in June is 35.79, 42.46 in July, and 36.4 in August. During the Christmas season, the price of water spinach in September is 34.68,  35.06 in October, 42.56 in November, and 59.8 in December."
        year = 2020
        month = 8
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [35.13, 35.79, 42.46, 36.4, 34.68, 35.06, 42.56, 59.8]
    
    elif loc == 'Cavite, Cavite Market' and com == 'Water Spinach':
        text2 = "The graph shows the prices of Water Spinach last 2020. The price of water spinach starts at 90 in May. When the rainy season comes, the prices of water spinanch in June is 84.46, 80.85 in July, 80.85 in August. During the Christmas season the price of water spinach in September is 73, 71.25 in October, 83.11 in November and 88.4 in December."
        year = 2020
        month = 8
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [90, 84.46, 80.85, 73.8, 73, 71.25, 83.11, 88.4]

    #BANANAS LAKATAN
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Bananas (Lakatan)':
        text2 = "The graph shows the prices of Bananas (Lakatan) last 2021. The price of Bananas (Lakatan) starts at 73.22 in January, 73.48 in February, and 73.11 in March. During the summer season, the price of Bananas (Lakatan) in April is 70.21 and 66.86 in May. When the rainy season begins, the price of Bananas (Lakatan) in June is 65.73, 67.53 in July, and 65.78 in August. During the Christmas season, the price of Bananas (Lakatan) in September is 64.13, 62.27 in October, 73.75 in November, and 72.5 in December."
        month = 10
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [73.22,73.48,73.11,70.21,66.86,65.73,67.53,65.78,64.13,62.27]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Bananas (Lakatan)':
        text2 = "The graph shows the prices of Bananas (Lakatan) last 2021. The price of Bananas (Lakatan) starts at 68.75 in January, 68.75 in February, and 67.5 in March. During the summer season, the price of Bananas (Lakatan) in April is 66.25 and 67.5 in May. When the rainy season begins, the price of Bananas (Lakatan) in June is 66.25 67.5 in July, and 67.5  in August. During the Christmas season, the price of Bananas (Lakatan) in September is 62.97, 65.69 in October, 64.33 in November, and 62.97 in December"
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [68.75,68.75,67.5,67.5,66.25,67.5,67.5,62.97,65.69,65.69,64.33,62.97]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Bananas (Lakatan)':
        text2 = "The graph shows the prices of Bananas (Lakatan) last 2021. The price of Bananas (Lakatan) starts at 93.13 in January, 89.38 in February, and 88.13 in March. During the summer season, the price of Bananas (Lakatan) in April is 88.13 and 86.25 in May. When the rainy season begins, the price of Bananas (Lakatan) in June is 83.13 76.25 in July, and 76.25 in August. During the Christmas season, the price of Bananas (Lakatan) in September is 76.88, 67.5 in October, 66.88 in November, and 68.75 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [93.13,89.38,88.13,88.13,86.25,83.13,76.25,76.88,67.5,66.88,66.88,68.75]

    elif loc == 'Laguna, Laguna Market' and com == 'Bananas (Lakatan)':
        text2 = "The graph shows the prices of Bananas (Lakatan) last 2021. The price of Bananas (Lakatan) starts at 90 in January, 88.75 in February, and 88.13 in March. During the summer season, the price of Bananas (Lakatan) in April is 88.75 and 88.75in May. When the rainy season begins, the price of Bananas (Lakatan) in June is 78.75, 80 in July, and 77.35 in August. During the Christmas season, the price of Bananas (Lakatan) in September is 73.57, 79.42 in October, 68.16 in November, and 67.53 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data = [90,88.75,88.13,88.75,88.75,78.75,80,77.35,73.57,69.42,68.16,67.53]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Bananas (Lakatan)':
        text2 = "The graph shows the prices of Bananas (Lakatan) last 2021. The price of Bananas (Lakatan) starts at 83.13 in January, 77.5 in February, and 78.75 in March. During the summer season, the price of Bananas (Lakatan) in April is 78.13 and 76.25in May. When the rainy season begins, the price of Bananas (Lakatan) in June is 71.88, 71.88 in July, and 74.38 in August. During the Christmas season, the price of Bananas (Lakatan) in September is 75, 75 in October, 73.75 in November, and 72.5 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [83.13,77.5,78.75,78.13,76.25,71.88,71.88,74.38,75,75,73.75,72.5]
    
    elif loc == 'Cavite, Cavite Market' and com == 'Bananas (Lakatan)':
        text2 = "Data is not available in Cavite Market"
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [0,0,0,0,0,0,0,0,0,0,0,0]

    #CARABO MANGO
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Mangoes (Carabao)':
        text2 = "The graph shows the prices of Mango (Carabao) last 2021. The price of Mango (Carabao) starts at 168 in March. During the summer season, the price of Mango (Carabao) in April is 159.1, and 147.44 in May. When the rainy season begins, the price of Mango (Carabao) in June is 137.27, 146.22 in July, and 148.68 in August. During the Christmas season, the price of Mango (Carabao) in September is 156.59, 153.99 in October, 157.2 in November, and 158.87 in December."
        month = 10
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [168, 159.51, 147.44, 139.27, 146.22, 148.68, 156.59, 153.99, 157.2, 158.87]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Mangoes (Carabao)':
        text2 = "The graph shows the prices of Mango (Carabao) last 2021. The price of Mango (Carabao) starts at 140 in January, 148.75 in February, and 135 in March. During the summer season, the price of Mango (Carabao) in April is 127.5 and 97.5 in May. When the rainy season begins, the price of Mango (Carabao) in June is 81.88, 87.5 in July, and 91.48 in August. During the Christmas season, the price of Mango (Carabao) in September is 96.45, 108.88 in October, 115.84 in November, and 127.27 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [140, 148.75, 135, 127.5, 97.5, 81.88, 87.5, 91.48, 96.45, 108.88, 115.84, 127.27]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Mangoes (Carabao)':
        text2 = "The graph shows the prices of Mango (Carabao) last 2021. The price of Mango (Carabao) starts at 200 in January, 148.5 in February, and 180 in March. During the summer season, the price of Mango (Carabao) in April is 165.63 and 150 in May. When the rainy season begins, the price of Mango (Carabao) in June is 128.13, 123.75 in July, and 164.38 in August. During the Christmas season, the price of Mango (Carabao) in September is 159.38, 169.38 in October, 170in November, and 175.63 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [200, 148.75, 180, 165.63, 150, 128.13, 123.75, 164.38, 159.38, 169.38, 170, 175.63]

    elif loc == 'Laguna, Laguna Market' and com == 'Mangoes (Carabao)':
        text2 = "The graph shows the prices of Mango (Carabao) last 2021. The price of Mango (Carabao) starts at 173.75 in January, 190 in February, and 185 in March. During the summer season, the price of Mango (Carabao) in April is 158.75 and 150 in May. When the rainy season begins, the price of Mango (Carabao) in June is 108.75, 125 in July, and 154.1 in August. During the Christmas season, the price of Mango (Carabao) in September is 166.79, 160.44 in October, 172.13 in November, and 167.65 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data = [173.75, 190, 185, 158.75, 150, 108.75, 125, 154.1, 166.79, 160.44, 172.13, 167.65]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Mangoes (Carabao)':
        text2 = "The graph shows the prices of Mango (Carabao) last 2021. The price of Mango (Carabao) starts at 224.38 in January, 190 in February, and 166.25 in March. During the summer season, the price of Mango (Carabao) in April is 167.5 and 146.25 in May. When the rainy season begins, the price of Mango (Carabao) in June is 125, 150 in July, and 159.84 in August. During the Christmas season, the price of Mango (Carabao) in September is 166.97, 166.72 in October, 167.83 in November, and 172.87 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [224.38, 190, 166.25, 167.5, 146.25, 125, 150, 159.84, 166.97, 166.72, 167.83, 172.87]
    
    elif loc == 'Cavite, Cavite Market' and com == 'Mangoes (Carabao)':
        text2 = "The graph shows the prices of Mango (Carabao) last 2021. The price of Mango (Carabao) starts at 192.5 in January, 176.25 in February, and 160 in March. During the summer season, the price of Mango (Carabao) in April is 170 and 148.75 in May. When the rainy season begins, the price of Mango (Carabao) in June is 133.75, 141.25 in July, and 156.25 in August. During the Christmas season, the price of Mango (Carabao) in September is 169.49, 161.55 in October, 161.55 in November, and 160.23 in December."
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [192.5, 176.25, 160, 170, 148.75, 133.75, 141.25, 156.25, 169.49, 161.55, 161.55, 160.23]

    #PIKO MANGO
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Mangoes (Piko)':
        text2= "Data is not available in Metro Manila market"
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [0,0,0,0,0,0,0,0,0,0,0,0]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Mangoes (Piko)':
        text2 = "The graph shows the prices of Mango (Piko) last 2020. The price of Mango (Piko) starts at 107.69 in May. When the rainy season comes, the prices of Mango (Piko) in June is 88, 95.71 in July, 126.49 in August. During the Christmas season the price of Mango (Piko) in September is 122.5, 140 in October, 132.82 in November and 126.41 in December."
        month = 8
        year = 2020
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [107.69, 88, 95.71, 126.49, 122.5, 140, 132.82, 126.41]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Mangoes (Piko)':
        text2 = "Data is not available in Pampanga Market"
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [0,0,0,0,0,0,0,0,0,0,0,0]

    elif loc == 'Laguna, Laguna Market' and com == 'Mangoes (Piko)':
        text2 = "Data is not available in Laguna Market"
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data = [0,0,0,0,0,0,0,0,0,0,0,0]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Mangoes (Piko)':
        text2 = "The graph shows the prices of Mango (Piko) last 2020. The price of Mango (Piko) starts at 138.67 in May. When the rainy season comes, the prices of Mango (Piko) in June is 139.17, 153.33 in July, 160 in August. During the Christmas season the price of Mango (Piko) in September is 183.33, 178.67 in October, 170 in November and 194.17 in December."
        year = 2020
        month = 8
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [138.67, 139.17, 153.33, 160, 183.33, 178.67, 170, 194.17]
    
    elif loc == 'Cavite, Cavite Market' and com == 'Mangoes (Piko)':
        text2 = "Data is not available in Cavite Market"
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [0,0,0,0,0,0,0,0,0,0,0,0]

    #PINEAPPLE
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Pineapples':
        text2 = "The graph shows the prices of Pineapple last 2020. The price of Pineapple starts at 70.94 in May. When the rainy season comes, the price of Pineapple in June is 72.74, 65.11 in July, and 69.86 in August. During the Christmas season, the price of Pineapple in September is 68.85, 65.42 in October, 66.83 in November, and 68.34 in December."
        month = 8
        year = 2020
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [70.94, 72.74, 65.11, 69.86, 68.85, 65.42, 66.83, 68.34]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Pineapples':
        text2 = "The graph shows the prices of Pineapple last 2020. The price of Pineapple starts at 67.46 in May. When the rainy season comes, the price of Pineapple in June is 54.69, 54.07 in July, and 54.75 in August. During the Christmas season, the price of Pineapple in September is 55.31, 56.67 in October, 55.85 in November, and 57.08 in December."
        month = 8
        year = 2020
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [67.46, 54.69, 54.07, 54.75, 55.31, 56.67, 55.85, 57.08]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Pineapples':
        text2 = "The graph shows the prices of Pineapple last 2020. The price of Pineapple starts at 77.46 in May. When the rainy season comes, the price of Pineapple in June is 73.45, 67.75 in July, and 66.75 in August. During the Christmas season, the price of Pineapple in September is 68.45, 80.2 in October, 81.73 in November, and 91.31 in December."
        month = 8
        year = 2020
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [77.46, 73.45, 67.75, 66.75, 68.45, 80.2, 81.73, 91.31]

    elif loc == 'Laguna, Laguna Market' and com == 'Pineapples':
        text2 = "The graph shows the prices of Pineapple last 2020. The price of Pineapple starts at 84.71 in May. When the rainy season comes, the price of Pineapple in June is 72, 66.67 in July, and 66.47 in August. During the Christmas season, the price of Pineapple in September is 67.5,  67.5 in October, 70 in November, and 81.9 in December."
        month = 8
        year = 2020
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data = [84.71, 72, 66.67, 66.47, 67.5, 67.5, 70, 81.9]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Pineapples':
        text2 = "The graph shows the prices of Pineapple last 2020. The price of Pineapple starts at 63 in May. When the rainy season comes, the price of Pineapple in June is 72.5, 67.78 in July, and 65.83 in August. During the Christmas season, the price of Pineapple in September is 65.83, 66 in October, 69.17 in November, and 68.33 in December."
        month = 8
        year = 2020
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [63, 72.5, 67.78, 65.83, 65.83, 66, 69.17, 68.33]
    
    elif loc == 'Cavite, Cavite Market' and com == 'Pineapples':
        text2 = "The graph shows the prices of Pineapple last 2020. The price of Pineapple starts at 55.32 in May. When the rainy season comes, the price of Pineapple in June is 55.54, 55.2 in July, and 54.59 in August. During the Christmas season, the price of Pineapple in September is 55.71,  58.75 in October, 73.5 in November, and 64.47 in December."
        month = 8
        year = 2020
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [55.32, 55.54, 55.2, 54.59, 55.71, 58.75, 73.57, 64.47]

    #MANDARINS
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Mandarins':
        text2 = "The graph shows the prices of Mandarins last 2021. The price of Mandarins starts at 50.99 in January, 51.55 in February, and 51.54 in March. During the summer season, the price of Mandarins in April is 50.36 and 49.86 in May. When the rainy season begins, the price of Mandarins in June is 51.15, 49.02 in July, and 54.88 in August. During the Christmas season, the price of Mandarins in September is 60.93, 59.76 in October, 55.08 in November, and 53.65 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [50.99, 51.55, 51.54, 50.36, 49.86, 51.15, 49.02, 54.88, 60.93, 59.76, 55.08, 53.65]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Mandarins':
        text2 = "The graph shows the prices of Mandarins last 2021. The price of Mandarins starts at 46.25 in January, 43.75 in February, and 47.5 in March. During the summer season, the price of Mandarins in April is 48.75 and 47.5 in May. When the rainy season begins, the price of Mandarins in June is 48.75, 47.5 in July, and 47.5 in August. During the Christmas season, the price of Mandarins in September is 48.75, 52.5 in October, 52.5 in November, and 52.5 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [46.25, 43.75, 47.5, 48.75, 47.5, 48.75, 47.5, 47.5, 48.75, 52.5, 52.5, 52.5]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Mandarins':
        text2 = "The graph shows the prices of Mandarins last 2021. The price of Mandarins starts at 68.75 in January, 61.88 in February, and 58.75 in March. During the summer season, the price of Mandarins in April is 59.38 and, 60 in May. When the rainy season begins, the price of Mandarins in June is 69.38, 68.75 in July, and 78.13 in August. During the Christmas season, the price of Mandarins in September is 69.38, 78.13 in October, 66.25 in November, and 66.25 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [68.75, 61.88, 58.75, 59.38, 60, 69.38, 68.75, 78.13, 69.38, 78.13, 66.25, 66.25]

    elif loc == 'Laguna, Laguna Market' and com == 'Mandarins':
        text2 = "Data is not available in Laguna Market"
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data = [0,0,0,0,0,0,0,0,0,0,0,0]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Mandarins':
        text2 = "The graph shows the prices of Mandarins last 2021. The price of Mandarins starts at 47.5 in January, 46.88 in February, and 50.63 in March. During the summer season, the price of Mandarins in April is 51.25 and 51.88 in May. When the rainy season begins, the price of Mandarins in June is 51.88, 51.88 in July, and 55. in August. During the Christmas season, the price of Mandarins in September is 55, 51.88 in October, 48.75 in November, and 51.25 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [47.5, 46.88, 50.63, 51.25, 51.88, 51.88, 51.88, 55, 55, 51.88, 48.75, 51.25]
    
    elif loc == 'Cavite, Cavite Market' and com == 'Mandarins':
        text2 = "Data is not available in Cavite Market"
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [0,0,0,0,0,0,0,0,0,0,0,0]

    #CARROTS
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Carrots':
        text2 = "The graph shows the prices of Carrots last 2021. The price of Carrots starts at 78.44 in March. During the summer season, the price of Carrots in April is 65.47, and 63 in May. When the rainy season begins, the price of Carrots in June is 62.87, 69.03 in July, and 93.73 in August. During the Christmas season, the price of Carrots in September is 75.63, 71.81 in October, 98.58 in November, and 75.7 in December."
        month = 10
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [78.44, 65.47, 63, 62.87, 69.03, 93.73, 75.63, 71.81, 98.58, 75.7]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Carrots':
        text2 = "The graph shows the prices of Carrots last 2021. The price of Carrots starts at 131.88 in January, 88.38 in February, and 64.13 in March. During the summer season, the price of Carrots in April is 53.75 and 47 in May. When the rainy season begins, the price of Carrots in June is 43.13, 36.75 in July, and 64.02 in August. During the Christmas season, the price of Carrots in September is 88.22, 56.57 in October, 98.58 in November, and 74.11 in December"
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [131.88, 88.38, 64.13, 53.75, 47, 43.13, 36.75, 64.02, 88.22, 56.57, 98.58, 74.11]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Carrots':
        text2 = "The graph shows the prices of Carrots last 2021. The price of Carrots starts at 137.5 in January, 98.13 in February, and 71.25 in March. During the summer season, the price of Carrots in April is 67.13 and 63.38 in May. When the rainy season begins, the price of Carrots in June is 53.75, 61.88 in July, and 108.75 in August. During the Christmas season, the price of Carrots in September is 137.5, 106.88 in October, 109.38 in November, and 103.13 in December"
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [137.5, 98.13, 71.25, 67.13, 63.38, 53.75, 61.88, 108.75, 137.5, 106.88, 109.38, 103.13]

    elif loc == 'Laguna, Laguna Market' and com == 'Carrots':
        text2 = "The graph shows the prices of Carrots last 2021. The price of Carrots starts at 141.25 in January, 113.75 in February, and 82.5 in March. During the summer season, the price of Carrots in April is 63.75 and 55 in May. When the rainy season begins, the price of Carrots in June is 62.5, 62.5 in July, and 93.34 in August. During the Christmas season, the price of Carrots in September is 150.06, 108.35 in October, 132.5 in November, and 122.91 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data = [141.25, 113.75, 82.5, 63.75, 55, 62.5, 62.5, 93.34, 150.06, 108.35, 132.5, 122.91]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Carrots':
        text2 = "The graph shows the prices of Carrots last 2021. The price of Carrots starts at 154.38 in January, 118.75 in February, and 99.38 in March. During the summer season, the price of Carrots in April is 76.25 and 68.75 in May. When the rainy season begins, the price of Carrots in June is 66.25, 71.25 in July, and 102.88 in August. During the Christmas season, the price of Carrots in September is 141, 103.75 in October, 143.75 in November, and 111.88 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [154.38, 118.75, 99.38, 76.25, 68.75, 66.25, 71.25, 102.88, 141, 103.75, 143.75, 111.88]
    
    elif loc == 'Cavite, Cavite Market' and com == 'Carrots':
        text2 = "The graph shows the prices of Carrots last 2021. The price of Carrots starts at 134.38 in January, 124.38 in February, and 105 in March. During the summer season, the price of Carrots in April is 86.25 and 92.5 in May. When the rainy season begins, the price of Carrots in June is 72.88, 75.63 in July, and 106.88 in August. During the Christmas season, the price of Carrots in September is 145.98, 91.24 in October, 129.04 in November, and 125.13 in December."
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [134.38, 124.38, 105, 86.25, 92.5, 72.88, 75.63, 106.88, 145.98, 91.24, 129.04, 125.13]

    #ONION RED
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Onion (Red)':
        month = 10
        text2 = "The graph shows the prices of Onion (Red) last 2021. The price of Onion (Red) start at 102.87 in March. During summer season the price of Onion (Red) in April is 100.4, and 99.33 in May. When the rainy season begin, the prices of Onion in June is 106.62, 109.28 in July and 110.27 in August. During the Christmas season the price of Onions in September is 114.25, 125.82 in October, 147.22 in November and 163.02 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [102.87, 100.4, 99.33, 106.62, 109.28, 110.27, 114.25, 125.82, 147.22, 163.02]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Onion (Red)':
        text2 = "The graph shows the prices of red onions last 2021. The price of coconut start at 151.25 in January, 115 in February and115 in March. During summer season the price of Onion (Red) in April is 105, and 105 in May. When the rainy season begin, the prices of Onion (Red) in June is 101.25, 98.75 in July and 106.02 in August. During the Christmas season the price of Onion (Red) in September is 107.5, 110.79 in October, 128.53 in November and 153.55 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [151.25, 115, 115, 105, 105, 101.25, 98.75, 106.02, 107.5, 110.79, 128.53, 153.55]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Onion (Red)':
        text2 = "The graph shows the prices of red onions last 2021. The price of Onion (Red) start at 100 in January, 80.63 in February and 78.13 in March. During summer season the price of Onion (Red) in April is 80.38, and 85 in May. When the rainy season begin, the prices of Onion (Red) in June is 76.88, 93.13 in July and 116.42 in August. During the Christmas season the price of Onion (Red) in September is 112.01, 129.01 in October, 132.15 in November and 159.21 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [100, 80.63, 78.13, 80.38, 85, 76.88, 93.13, 116.42, 112.01, 129.01, 132.15, 159.21]

    elif loc == 'Laguna, Laguna Market' and com == 'Onion (Red)':
        text2 = "Data is not available in Laguna Market"
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data = [0,0,0,0,0,0,0,0,0,0,0]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Onion (Red)':
        text2 = "Data is not available in Rizal Market"
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [0,0,0,0,0,0,0,0,0,0,0]
    
    elif loc == 'Cavite, Cavite Market' and com == 'Onion (Red)':
        text2 = "The graph shows the prices of Onion (Red) last 2021. The price of Onion (Red) start at 116.88 in January, 119.38 in February and 125 in March. During summer season the price of Onion (Red) in April is 103.13, and 109.38 in May. When the rainy season begin, the prices of Onion (Red) in June is 106.25, 105 in July and 115 in August. During the Christmas season the price of Onion (Red) in September is 124.7, 143.43 in October, 148.999 in November and 186.98 in December."
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [116.88, 119.38, 125, 103.13, 109.38, 106.25, 105, 115, 124.7, 143.43, 148.99, 186.98]

    #GARLIC
    elif loc == 'Metropolitan Manila, Metro Manila Market' and com == 'Garlic':
        text2 = "The graph shows the prices of garlics last 2021. The price of garlic start at 301.67 in January, 297.5 in February and 290.83 in March. During summer season the price of Garlic in April is 287.08 and 287.08 in May. When the rainy season begin, the prices of Coconuts in June is 285.75, 294.48 in July and 295.42 in August. During the Christmas season the price of Garlic in September is 277.23, 305.64 in October, 343.51 in November and 345.97 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Metro Manila Market "
        data = [301.67, 297.5, 290.83, 287.08, 287.08, 285.75, 294.48, 295.42, 277.23, 305.64, 343.51, 345.97]

    elif loc == 'Bulacan, Bulacan Market' and com == 'Garlic':
        text2 = "The graph shows the prices of garlics last 2021. The price of garlic start at 136.5 in January, 139 in February and 112.13 in March. During summer season the price of Garlic in April is 113.75, and 115 in May. When the rainy season begin, the prices of Coconuts in June is 113.75, 113.75 in July and 125.46 in August. During the Christmas season the price of Garlic in September is 121.28, 118.77  in October, 110.41 in November and 112.92 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Bulacan Market "
        data = [136.5, 139, 112.13, 113.75, 115, 113.75, 113.75, 125.46, 121.28, 118.77, 110.41, 112.92]
    
    elif loc == 'Bulacan, Pampanga Market' and com == 'Garlic':
        text2 = "The graph shows the prices of garlics last 2021. The price of garlic start at 109.38 in January, 101.88 in February and 101.88 in March. During summer season the price of Garlic in April is 110.63, and 103.75 in May. When the rainy season begin, the prices of Coconuts in June is 103.13, 103.13 in July and 118.94 in August. During the Christmas season the price of Garlic in September is 126.53, 131.59 in October, 127.79 in November and 129.69 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Pampanga Market "
        data = [109.38, 101.88, 101.88, 110.63, 103.75, 103.13, 103.13, 118.94, 126.53, 131.59, 127.79, 129.69]

    elif loc == 'Laguna, Laguna Market' and com == 'Garlic':
        text2 = "Data is not available in Laguna Market"
        text = " Price in "
        text1 = "Year "
        mrkt = " Laguna Market "
        data = [0,0,0,0,0,0,0,0,0,0,0,0]
    
    elif loc == 'Rizal, Rizal Market' and com == 'Garlic':
        text2 = "The graph shows the prices of garlics last 2021. The price of garlic start at 281.67 in January, 290 in February and 296.67 in March. During summer season the price of Garlic in April is 288.33, and 296.67 in May. When the rainy season begin, the prices of Coconuts in June is 296.67, 291.67 in July and 300 in August. During the Christmas season the price of Garlic in September is 285, 301.67 in October, 301.67 in November and 301.67 in December."
        text = " Price in "
        text1 = "Year "
        mrkt = " Rizal Market "
        data = [281.67, 290, 296.67, 288.33, 296.67, 296.67, 291.67, 300, 285, 301.67, 301.67, 301.67]
    
    elif loc == 'Cavite, Cavite Market' and com == 'Garlic':
        text2 = "Data is not available in Rizal Market"
        text = " Price in Year"
        text1 = "Year "
        mrkt = " Cavite Market "
        data = [0,0,0,0,0,0,0,0,0,0,0,0]
    
    print(text2)
    return jsonify({
        'success': True,
        'com': com,
        'loc': loc,
        'data': data,
        'month': month,
        'mrkt': mrkt,
        'text2': text2
    })
    
@app.route('/year_forecast', methods=['GET', 'POST'])
def year_forecast_page():
    
    if 'user' in session:
        user = session['user']
        return render_template('year_forecast.html', user=user)
    else:
        return render_template('login_page.html')
   


# @app.route('/yearfc', methods=['GET', 'POST'])
# @login_required
# def year_page():
#     return render_template('year.html')

@app.route('/ypredict', methods=['POST'])
def yearpredict():
    veg = request.form.get("veg")
    year = request.form.get("year")
    getlocation = "Metropolitan Manila, Metro Manila Market"

    #commodities
    Cabbage = 0             
    Carrots = 0              
    Garlic = 0             
    OnionsR = 0         
    Tomatoes = 0            
    OnionsW = 0          
    Lantundan = 0      
    Saba = 0           
    GBeans = 0    
    SBeans = 0          
    Bittermelon = 0            
    Bottlegourd = 0            
    CabbageC = 0        
    Calamansi = 0            
    Choko = 0           
    Coconut = 0               
    Eggplants = 0             
    Ginger = 0          
    Papaya = 0               
    Squashes = 0              
    SweetPotatoLeaves = 0      
    Waterspinach = 0            
    Lakatan = 0       
    MangoesC = 0       
    MangoesP = 0           
    Pineapples = 0             
    Mandarins = 0

    #market
    Metro_Manila = 0
    Santa_Cruz = 0
    Bulacan = 0
    Pampanga = 0
    Cavite = 0
    Laguna  = 0
    Rizal = 0  

    #grid values
    latitude = 0
    longtitude = 0

    #provinces
    metro_manila = 0
    bulacan = 0
    laguna = 0 
    rizal = 0
    cavite = 0
    
    #region
    ncr = 0
    region_iii = 0
    region_iv = 0

    #month
    January = 0                   
    February = 0          
    March = 0                    
    April = 0                    
    May = 0                        
    June = 0                    
    July = 0                      
    August = 0                 
    September = 0              
    October = 0                    
    November = 0                   
    December = 0

    if getlocation == 'Metropolitan Manila, Metro Manila Market':
        ncr = 1
        metro_manila = 1
        Metro_Manila = 1
        latitude = 14.604167
        longtitude = 120.982222

    elif getlocation == 'Rizal, Santa Cruz Market':
        region_iv = 1
        rizal = 1
        Santa_Cruz = 1
        latitude = 14.6089
        longtitude = 121.1712

    elif getlocation == 'Bulacan, Bulacan Market':
        region_iii = 1
        bulacan = 1
        Bulacan = 1
        latitude = 14.843102
        longtitude = 120.814215

    elif getlocation == 'Rizal, Rizal Market':
        region_iv = 1
        rizal = 1
        Rizal = 1
        latitude = 14.594806
        longtitude = 121.171055

    elif getlocation == 'Bulacan, Pampanga Market':
        region_iii = 1
        bulacan = 1
        Pampanga = 1
        latitude = 15.02486
        longtitude = 121.086142

    elif getlocation == 'Laguna, Laguna Market':
        region_iv = 1
        laguna = 1
        Laguna = 1
        latitude = 14.286267
        longtitude = 121.41211

    elif getlocation == 'Cavite, Cavite Market':
        region_iv = 1
        cavite = 1
        Cavite = 1
        latitude = 14.422901
        longtitude = 120.94107

    if veg == 'Garlic':
        Garlic = 1
    elif veg == 'Carrot':
        Carrots = 1
    elif veg == 'Cabbage':
        Cabbage = 1
    elif veg == 'Onion (Red)':
        OnionsR = 1
    elif veg == 'Tomatoes':
        Tomatoes = 1
    elif veg == 'Onions (white)':
        OnionsW = 1
    elif veg == 'Bananas (Latundan)':
        Lantundan = 1
    elif veg == 'Bananas (saba)':
        Saba = 1
    elif veg == 'Beans (green, fresh)':
        GBeans = 1
    elif veg == 'Beans (string)':
        SBeans = 1
    elif veg == 'Bitter melon':
        Bittermelon = 1
    elif veg == 'Bottle gourd':
        Bottlegourd = 1
    elif veg == 'Cabbage (chinese)':
        CabbageC = 1
    elif veg == 'Calamansi':
        Calamansi = 1
    elif veg == 'Choko':
        Choko = 1
    elif veg == 'Eggplants':
        Eggplants = 1
    elif veg == 'Ginger':
        Ginger = 1
    elif veg == 'Papaya':
        Papaya = 1
    elif veg == 'Squashes':
        Squashes = 1
    elif veg == 'Sweet Potato leaves':
        SweetPotatoLeaves = 1
    elif veg == 'Water spinach':
        Waterspinach = 1
    elif veg == 'Bananas (lakatan)':
        Lakatan = 1
    elif veg == 'Mangoes (carabao)':
        MangoesC = 1
    elif veg == 'Mangoes (piko)':
        MangoesP = 1
    elif veg == 'Pineapples':
        Pineapples = 1
    elif veg == 'Mandarins':
        Mandarins = 1
    elif veg == 'Coconuts':
        Coconut = 1
    

    mtr_pred_prices = []
    for i in range(12):
        i = i+1
        if i == 1:
            January = 1                   
            February = 0          
            March = 0                    
            April = 0                    
            May = 0                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        elif i == 2:
            January = 0                   
            February = 1          
            March = 0                    
            April = 0                    
            May = 0                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        elif i == 3:
            January = 0                   
            February = 0          
            March = 1                    
            April = 0                    
            May = 0                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        elif i==4:
            January = 0                   
            February = 0          
            March = 0                    
            April = 1                    
            May = 0                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        elif i == 5:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                    
            May = 1                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0

        elif i == 6:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 1                   
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0

        elif i == 7:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 1                    
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        
        elif i == 8:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 1                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0

        elif i == 9:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 0                 
            September = 1              
            October = 0                    
            November = 0                   
            December = 0

        elif i == 10:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 0                 
            September = 0              
            October = 1                    
            November = 0                   
            December = 0
        
        elif i == 11:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 1                   
            December = 0

        elif i == 12:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 1
       

        mtr_int_features = [float(latitude),float(longtitude),int(year),int(Lakatan),int(Lantundan),int(Saba),
                    int(GBeans),int(SBeans),int(Bittermelon),int(Bottlegourd),int(Cabbage),int(CabbageC),int(Calamansi),
                    int(Carrots),int(Choko),int(Coconut),int(Eggplants),int(Garlic),int(Ginger),int(Mandarins),int(MangoesC),
                    int(MangoesP),int(OnionsR),int(OnionsW),int(Papaya),int(Pineapples),int(Squashes),int(SweetPotatoLeaves),
                    int(Tomatoes),int(Waterspinach),int(bulacan),int(cavite),int(laguna),int(metro_manila),int(rizal),int(Bulacan),
                    int(Cavite),int(Laguna),int(Metro_Manila),int(Pampanga),int(Rizal),int(Santa_Cruz),int(January),int(February),
                    int(March),int(April),int(May),int(June),int(July),int(August),int(September),int(October),int(November),
                    int(December),int(ncr),int(region_iii),int(region_iv)]

        #priceforecasting
        mtr_final_features = [np.array(mtr_int_features)]
        mtr_pred_price = model.predict(mtr_final_features)
        mtr_output = round(mtr_pred_price[0],2)

        mtr_pred_prices.append(mtr_output)
    
    mtr_min_val = min(mtr_pred_prices)
    mtr_max_val = max(mtr_pred_prices)

    getlocation = "Bulacan, Bulacan Market"

    #commodities
    Cabbage = 0             
    Carrots = 0              
    Garlic = 0             
    OnionsR = 0         
    Tomatoes = 0            
    OnionsW = 0          
    Lantundan = 0      
    Saba = 0           
    GBeans = 0    
    SBeans = 0          
    Bittermelon = 0            
    Bottlegourd = 0            
    CabbageC = 0        
    Calamansi = 0            
    Choko = 0           
    Coconut = 0               
    Eggplants = 0             
    Ginger = 0          
    Papaya = 0               
    Squashes = 0              
    SweetPotatoLeaves = 0      
    Waterspinach = 0            
    Lakatan = 0       
    MangoesC = 0       
    MangoesP = 0           
    Pineapples = 0             
    Mandarins = 0

    #market
    Metro_Manila = 0
    Santa_Cruz = 0
    Bulacan = 0
    Pampanga = 0
    Cavite = 0
    Laguna  = 0
    Rizal = 0  

    #grid values
    latitude = 0
    longtitude = 0

    #provinces
    metro_manila = 0
    bulacan = 0
    laguna = 0 
    rizal = 0
    cavite = 0
    
    #region
    ncr = 0
    region_iii = 0
    region_iv = 0

    #month
    January = 0                   
    February = 0          
    March = 0                    
    April = 0                    
    May = 0                        
    June = 0                    
    July = 0                      
    August = 0                 
    September = 0              
    October = 0                    
    November = 0                   
    December = 0

    if getlocation == 'Metropolitan Manila, Metro Manila Market':
        ncr = 1
        metro_manila = 1
        Metro_Manila = 1
        latitude = 14.604167
        longtitude = 120.982222

    elif getlocation == 'Rizal, Santa Cruz Market':
        region_iv = 1
        rizal = 1
        Santa_Cruz = 1
        latitude = 14.6089
        longtitude = 121.1712

    elif getlocation == 'Bulacan, Bulacan Market':
        region_iii = 1
        bulacan = 1
        Bulacan = 1
        latitude = 14.843102
        longtitude = 120.814215

    elif getlocation == 'Rizal, Rizal Market':
        region_iv = 1
        rizal = 1
        Rizal = 1
        latitude = 14.594806
        longtitude = 121.171055

    elif getlocation == 'Bulacan, Pampanga Market':
        region_iii = 1
        bulacan = 1
        Pampanga = 1
        latitude = 15.02486
        longtitude = 121.086142

    elif getlocation == 'Laguna, Laguna Market':
        region_iv = 1
        laguna = 1
        Laguna = 1
        latitude = 14.286267
        longtitude = 121.41211

    elif getlocation == 'Cavite, Cavite Market':
        region_iv = 1
        cavite = 1
        Cavite = 1
        latitude = 14.422901
        longtitude = 120.94107

    if veg == 'Garlic':
        Garlic = 1
    elif veg == 'Carrot':
        Carrots = 1
    elif veg == 'Cabbage':
        Cabbage = 1
    elif veg == 'Onion (Red)':
        OnionsR = 1
    elif veg == 'Tomatoes':
        Tomatoes = 1
    elif veg == 'Onions (white)':
        OnionsW = 1
    elif veg == 'Bananas (Latundan)':
        Lantundan = 1
    elif veg == 'Bananas (saba)':
        Saba = 1
    elif veg == 'Beans (green, fresh)':
        GBeans = 1
    elif veg == 'Beans (string)':
        SBeans = 1
    elif veg == 'Bitter melon':
        Bittermelon = 1
    elif veg == 'Bottle gourd':
        Bottlegourd = 1
    elif veg == 'Cabbage (chinese)':
        CabbageC = 1
    elif veg == 'Calamansi':
        Calamansi = 1
    elif veg == 'Choko':
        Choko = 1
    elif veg == 'Eggplants':
        Eggplants = 1
    elif veg == 'Ginger':
        Ginger = 1
    elif veg == 'Papaya':
        Papaya = 1
    elif veg == 'Squashes':
        Squashes = 1
    elif veg == 'Sweet Potato leaves':
        SweetPotatoLeaves = 1
    elif veg == 'Water spinach':
        Waterspinach = 1
    elif veg == 'Bananas (lakatan)':
        Lakatan = 1
    elif veg == 'Mangoes (carabao)':
        MangoesC = 1
    elif veg == 'Mangoes (piko)':
        MangoesP = 1
    elif veg == 'Pineapples':
        Pineapples = 1
    elif veg == 'Mandarins':
        Mandarins = 1
    elif veg == 'Coconuts':
        Coconut = 1
    

    bul_pred_prices = []
    for i in range(12):
        i = i+1
        if i == 1:
            January = 1                   
            February = 0          
            March = 0                    
            April = 0                    
            May = 0                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        elif i == 2:
            January = 0                   
            February = 1          
            March = 0                    
            April = 0                    
            May = 0                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        elif i == 3:
            January = 0                   
            February = 0          
            March = 1                    
            April = 0                    
            May = 0                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        elif i==4:
            January = 0                   
            February = 0          
            March = 0                    
            April = 1                    
            May = 0                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        elif i == 5:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                    
            May = 1                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0

        elif i == 6:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 1                   
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0

        elif i == 7:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 1                    
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        
        elif i == 8:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 1                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0

        elif i == 9:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 0                 
            September = 1              
            October = 0                    
            November = 0                   
            December = 0

        elif i == 10:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 0                 
            September = 0              
            October = 1                    
            November = 0                   
            December = 0
        
        elif i == 11:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 1                   
            December = 0

        elif i == 12:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 1
       

        bul_int_features = [float(latitude),float(longtitude),int(year),int(Lakatan),int(Lantundan),int(Saba),
                    int(GBeans),int(SBeans),int(Bittermelon),int(Bottlegourd),int(Cabbage),int(CabbageC),int(Calamansi),
                    int(Carrots),int(Choko),int(Coconut),int(Eggplants),int(Garlic),int(Ginger),int(Mandarins),int(MangoesC),
                    int(MangoesP),int(OnionsR),int(OnionsW),int(Papaya),int(Pineapples),int(Squashes),int(SweetPotatoLeaves),
                    int(Tomatoes),int(Waterspinach),int(bulacan),int(cavite),int(laguna),int(metro_manila),int(rizal),int(Bulacan),
                    int(Cavite),int(Laguna),int(Metro_Manila),int(Pampanga),int(Rizal),int(Santa_Cruz),int(January),int(February),
                    int(March),int(April),int(May),int(June),int(July),int(August),int(September),int(October),int(November),
                    int(December),int(ncr),int(region_iii),int(region_iv)]

        #priceforecasting
        bul_final_features = [np.array(bul_int_features)]
        bul_pred_price = model.predict(bul_final_features)
        bul_output = round(bul_pred_price[0],2)

        bul_pred_prices.append(bul_output)
    
    bul_min_val = min(bul_pred_prices)
    bul_max_val = max(bul_pred_prices)

    getlocation = "Rizal, Rizal Market"

    #commodities
    Cabbage = 0             
    Carrots = 0              
    Garlic = 0             
    OnionsR = 0         
    Tomatoes = 0            
    OnionsW = 0          
    Lantundan = 0      
    Saba = 0           
    GBeans = 0    
    SBeans = 0          
    Bittermelon = 0            
    Bottlegourd = 0            
    CabbageC = 0        
    Calamansi = 0            
    Choko = 0           
    Coconut = 0               
    Eggplants = 0             
    Ginger = 0          
    Papaya = 0               
    Squashes = 0              
    SweetPotatoLeaves = 0      
    Waterspinach = 0            
    Lakatan = 0       
    MangoesC = 0       
    MangoesP = 0           
    Pineapples = 0             
    Mandarins = 0

    #market
    Metro_Manila = 0
    Santa_Cruz = 0
    Bulacan = 0
    Pampanga = 0
    Cavite = 0
    Laguna  = 0
    Rizal = 0  

    #grid values
    latitude = 0
    longtitude = 0

    #provinces
    metro_manila = 0
    bulacan = 0
    laguna = 0 
    rizal = 0
    cavite = 0
    
    #region
    ncr = 0
    region_iii = 0
    region_iv = 0

    #month
    January = 0                   
    February = 0          
    March = 0                    
    April = 0                    
    May = 0                        
    June = 0                    
    July = 0                      
    August = 0                 
    September = 0              
    October = 0                    
    November = 0                   
    December = 0

    if getlocation == 'Metropolitan Manila, Metro Manila Market':
        ncr = 1
        metro_manila = 1
        Metro_Manila = 1
        latitude = 14.604167
        longtitude = 120.982222

    elif getlocation == 'Rizal, Santa Cruz Market':
        region_iv = 1
        rizal = 1
        Santa_Cruz = 1
        latitude = 14.6089
        longtitude = 121.1712

    elif getlocation == 'Bulacan, Bulacan Market':
        region_iii = 1
        bulacan = 1
        Bulacan = 1
        latitude = 14.843102
        longtitude = 120.814215

    elif getlocation == 'Rizal, Rizal Market':
        region_iv = 1
        rizal = 1
        Rizal = 1
        latitude = 14.594806
        longtitude = 121.171055

    elif getlocation == 'Bulacan, Pampanga Market':
        region_iii = 1
        bulacan = 1
        Pampanga = 1
        latitude = 15.02486
        longtitude = 121.086142

    elif getlocation == 'Laguna, Laguna Market':
        region_iv = 1
        laguna = 1
        Laguna = 1
        latitude = 14.286267
        longtitude = 121.41211

    elif getlocation == 'Cavite, Cavite Market':
        region_iv = 1
        cavite = 1
        Cavite = 1
        latitude = 14.422901
        longtitude = 120.94107

    if veg == 'Garlic':
        Garlic = 1
    elif veg == 'Carrot':
        Carrots = 1
    elif veg == 'Cabbage':
        Cabbage = 1
    elif veg == 'Onion (Red)':
        OnionsR = 1
    elif veg == 'Tomatoes':
        Tomatoes = 1
    elif veg == 'Onions (white)':
        OnionsW = 1
    elif veg == 'Bananas (Latundan)':
        Lantundan = 1
    elif veg == 'Bananas (saba)':
        Saba = 1
    elif veg == 'Beans (green, fresh)':
        GBeans = 1
    elif veg == 'Beans (string)':
        SBeans = 1
    elif veg == 'Bitter melon':
        Bittermelon = 1
    elif veg == 'Bottle gourd':
        Bottlegourd = 1
    elif veg == 'Cabbage (chinese)':
        CabbageC = 1
    elif veg == 'Calamansi':
        Calamansi = 1
    elif veg == 'Choko':
        Choko = 1
    elif veg == 'Eggplants':
        Eggplants = 1
    elif veg == 'Ginger':
        Ginger = 1
    elif veg == 'Papaya':
        Papaya = 1
    elif veg == 'Squashes':
        Squashes = 1
    elif veg == 'Sweet Potato leaves':
        SweetPotatoLeaves = 1
    elif veg == 'Water spinach':
        Waterspinach = 1
    elif veg == 'Bananas (lakatan)':
        Lakatan = 1
    elif veg == 'Mangoes (carabao)':
        MangoesC = 1
    elif veg == 'Mangoes (piko)':
        MangoesP = 1
    elif veg == 'Pineapples':
        Pineapples = 1
    elif veg == 'Mandarins':
        Mandarins = 1
    elif veg == 'Coconuts':
        Coconut = 1
    

    riz_pred_prices = []
    for i in range(12):
        i = i+1
        if i == 1:
            January = 1                   
            February = 0          
            March = 0                    
            April = 0                    
            May = 0                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        elif i == 2:
            January = 0                   
            February = 1          
            March = 0                    
            April = 0                    
            May = 0                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        elif i == 3:
            January = 0                   
            February = 0          
            March = 1                    
            April = 0                    
            May = 0                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        elif i==4:
            January = 0                   
            February = 0          
            March = 0                    
            April = 1                    
            May = 0                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        elif i == 5:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                    
            May = 1                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0

        elif i == 6:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 1                   
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0

        elif i == 7:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 1                    
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        
        elif i == 8:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 1                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0

        elif i == 9:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 0                 
            September = 1              
            October = 0                    
            November = 0                   
            December = 0

        elif i == 10:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 0                 
            September = 0              
            October = 1                    
            November = 0                   
            December = 0
        
        elif i == 11:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 1                   
            December = 0

        elif i == 12:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 1
       

        riz_int_features = [float(latitude),float(longtitude),int(year),int(Lakatan),int(Lantundan),int(Saba),
                    int(GBeans),int(SBeans),int(Bittermelon),int(Bottlegourd),int(Cabbage),int(CabbageC),int(Calamansi),
                    int(Carrots),int(Choko),int(Coconut),int(Eggplants),int(Garlic),int(Ginger),int(Mandarins),int(MangoesC),
                    int(MangoesP),int(OnionsR),int(OnionsW),int(Papaya),int(Pineapples),int(Squashes),int(SweetPotatoLeaves),
                    int(Tomatoes),int(Waterspinach),int(bulacan),int(cavite),int(laguna),int(metro_manila),int(rizal),int(Bulacan),
                    int(Cavite),int(Laguna),int(Metro_Manila),int(Pampanga),int(Rizal),int(Santa_Cruz),int(January),int(February),
                    int(March),int(April),int(May),int(June),int(July),int(August),int(September),int(October),int(November),
                    int(December),int(ncr),int(region_iii),int(region_iv)]

        #priceforecasting
        riz_final_features = [np.array(riz_int_features)]
        riz_pred_price = model.predict(riz_final_features)
        riz_output = round(riz_pred_price[0],2)

        riz_pred_prices.append(riz_output)
    
    riz_min_val = min(riz_pred_prices)
    riz_max_val = max(riz_pred_prices)

    getlocation = "Bulacan, Pampanga Market"

    #commodities
    Cabbage = 0             
    Carrots = 0              
    Garlic = 0             
    OnionsR = 0         
    Tomatoes = 0            
    OnionsW = 0          
    Lantundan = 0      
    Saba = 0           
    GBeans = 0    
    SBeans = 0          
    Bittermelon = 0            
    Bottlegourd = 0            
    CabbageC = 0        
    Calamansi = 0            
    Choko = 0           
    Coconut = 0               
    Eggplants = 0             
    Ginger = 0          
    Papaya = 0               
    Squashes = 0              
    SweetPotatoLeaves = 0      
    Waterspinach = 0            
    Lakatan = 0       
    MangoesC = 0       
    MangoesP = 0           
    Pineapples = 0             
    Mandarins = 0

    #market
    Metro_Manila = 0
    Santa_Cruz = 0
    Bulacan = 0
    Pampanga = 0
    Cavite = 0
    Laguna  = 0
    Rizal = 0  

    #grid values
    latitude = 0
    longtitude = 0

    #provinces
    metro_manila = 0
    bulacan = 0
    laguna = 0 
    rizal = 0
    cavite = 0
    
    #region
    ncr = 0
    region_iii = 0
    region_iv = 0

    #month
    January = 0                   
    February = 0          
    March = 0                    
    April = 0                    
    May = 0                        
    June = 0                    
    July = 0                      
    August = 0                 
    September = 0              
    October = 0                    
    November = 0                   
    December = 0


    if getlocation == 'Metropolitan Manila, Metro Manila Market':
        ncr = 1
        metro_manila = 1
        Metro_Manila = 1
        latitude = 14.604167
        longtitude = 120.982222

    elif getlocation == 'Rizal, Santa Cruz Market':
        region_iv = 1
        rizal = 1
        Santa_Cruz = 1
        latitude = 14.6089
        longtitude = 121.1712

    elif getlocation == 'Bulacan, Bulacan Market':
        region_iii = 1
        bulacan = 1
        Bulacan = 1
        latitude = 14.843102
        longtitude = 120.814215

    elif getlocation == 'Rizal, Rizal Market':
        region_iv = 1
        rizal = 1
        Rizal = 1
        latitude = 14.594806
        longtitude = 121.171055

    elif getlocation == 'Bulacan, Pampanga Market':
        region_iii = 1
        bulacan = 1
        Pampanga = 1
        latitude = 15.02486
        longtitude = 121.086142

    elif getlocation == 'Laguna, Laguna Market':
        region_iv = 1
        laguna = 1
        Laguna = 1
        latitude = 14.286267
        longtitude = 121.41211

    elif getlocation == 'Cavite, Cavite Market':
        region_iv = 1
        cavite = 1
        Cavite = 1
        latitude = 14.422901
        longtitude = 120.94107

    if veg == 'Garlic':
        Garlic = 1
    elif veg == 'Carrot':
        Carrots = 1
    elif veg == 'Cabbage':
        Cabbage = 1
    elif veg == 'Onion (Red)':
        OnionsR = 1
    elif veg == 'Tomatoes':
        Tomatoes = 1
    elif veg == 'Onions (white)':
        OnionsW = 1
    elif veg == 'Bananas (Latundan)':
        Lantundan = 1
    elif veg == 'Bananas (saba)':
        Saba = 1
    elif veg == 'Beans (green, fresh)':
        GBeans = 1
    elif veg == 'Beans (string)':
        SBeans = 1
    elif veg == 'Bitter melon':
        Bittermelon = 1
    elif veg == 'Bottle gourd':
        Bottlegourd = 1
    elif veg == 'Cabbage (chinese)':
        CabbageC = 1
    elif veg == 'Calamansi':
        Calamansi = 1
    elif veg == 'Choko':
        Choko = 1
    elif veg == 'Eggplants':
        Eggplants = 1
    elif veg == 'Ginger':
        Ginger = 1
    elif veg == 'Papaya':
        Papaya = 1
    elif veg == 'Squashes':
        Squashes = 1
    elif veg == 'Sweet Potato leaves':
        SweetPotatoLeaves = 1
    elif veg == 'Water spinach':
        Waterspinach = 1
    elif veg == 'Bananas (lakatan)':
        Lakatan = 1
    elif veg == 'Mangoes (carabao)':
        MangoesC = 1
    elif veg == 'Mangoes (piko)':
        MangoesP = 1
    elif veg == 'Pineapples':
        Pineapples = 1
    elif veg == 'Mandarins':
        Mandarins = 1
    elif veg == 'Coconuts':
        Coconut = 1


    pam_pred_prices = []
    for i in range(12):
        i = i+1
        if i == 1:
            January = 1                   
            February = 0          
            March = 0                    
            April = 0                    
            May = 0                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        elif i == 2:
            January = 0                   
            February = 1          
            March = 0                    
            April = 0                    
            May = 0                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        elif i == 3:
            January = 0                   
            February = 0          
            March = 1                    
            April = 0                    
            May = 0                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        elif i==4:
            January = 0                   
            February = 0          
            March = 0                    
            April = 1                    
            May = 0                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        elif i == 5:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                    
            May = 1                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0

        elif i == 6:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 1                   
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0

        elif i == 7:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 1                    
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        
        elif i == 8:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 1                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0

        elif i == 9:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 0                 
            September = 1              
            October = 0                    
            November = 0                   
            December = 0

        elif i == 10:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 0                 
            September = 0              
            October = 1                    
            November = 0                   
            December = 0
        
        elif i == 11:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 1                   
            December = 0

        elif i == 12:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 1
       

        pam_int_features = [float(latitude),float(longtitude),int(year),int(Lakatan),int(Lantundan),int(Saba),
                    int(GBeans),int(SBeans),int(Bittermelon),int(Bottlegourd),int(Cabbage),int(CabbageC),int(Calamansi),
                    int(Carrots),int(Choko),int(Coconut),int(Eggplants),int(Garlic),int(Ginger),int(Mandarins),int(MangoesC),
                    int(MangoesP),int(OnionsR),int(OnionsW),int(Papaya),int(Pineapples),int(Squashes),int(SweetPotatoLeaves),
                    int(Tomatoes),int(Waterspinach),int(bulacan),int(cavite),int(laguna),int(metro_manila),int(rizal),int(Bulacan),
                    int(Cavite),int(Laguna),int(Metro_Manila),int(Pampanga),int(Rizal),int(Santa_Cruz),int(January),int(February),
                    int(March),int(April),int(May),int(June),int(July),int(August),int(September),int(October),int(November),
                    int(December),int(ncr),int(region_iii),int(region_iv)]

        #priceforecasting
        pam_final_features = [np.array(pam_int_features)]
        pam_pred_price = model.predict(pam_final_features)
        pam_output = round(pam_pred_price[0],2)

        pam_pred_prices.append(pam_output)
    
    pam_min_val = min(pam_pred_prices)
    pam_max_val = max(pam_pred_prices)

    getlocation = "Cavite, Cavite Market"

    #commodities
    Cabbage = 0             
    Carrots = 0              
    Garlic = 0             
    OnionsR = 0         
    Tomatoes = 0            
    OnionsW = 0          
    Lantundan = 0      
    Saba = 0           
    GBeans = 0    
    SBeans = 0          
    Bittermelon = 0            
    Bottlegourd = 0            
    CabbageC = 0        
    Calamansi = 0            
    Choko = 0           
    Coconut = 0               
    Eggplants = 0             
    Ginger = 0          
    Papaya = 0               
    Squashes = 0              
    SweetPotatoLeaves = 0      
    Waterspinach = 0            
    Lakatan = 0       
    MangoesC = 0       
    MangoesP = 0           
    Pineapples = 0             
    Mandarins = 0

    #market
    Metro_Manila = 0
    Santa_Cruz = 0
    Bulacan = 0
    Pampanga = 0
    Cavite = 0
    Laguna  = 0
    Rizal = 0  

    #grid values
    latitude = 0
    longtitude = 0

    #provinces
    metro_manila = 0
    bulacan = 0
    laguna = 0 
    rizal = 0
    cavite = 0
    
    #region
    ncr = 0
    region_iii = 0
    region_iv = 0

    #month
    January = 0                   
    February = 0          
    March = 0                    
    April = 0                    
    May = 0                        
    June = 0                    
    July = 0                      
    August = 0                 
    September = 0              
    October = 0                    
    November = 0                   
    December = 0


    if getlocation == 'Metropolitan Manila, Metro Manila Market':
        ncr = 1
        metro_manila = 1
        Metro_Manila = 1
        latitude = 14.604167
        longtitude = 120.982222

    elif getlocation == 'Rizal, Santa Cruz Market':
        region_iv = 1
        rizal = 1
        Santa_Cruz = 1
        latitude = 14.6089
        longtitude = 121.1712

    elif getlocation == 'Bulacan, Bulacan Market':
        region_iii = 1
        bulacan = 1
        Bulacan = 1
        latitude = 14.843102
        longtitude = 120.814215

    elif getlocation == 'Rizal, Rizal Market':
        region_iv = 1
        rizal = 1
        Rizal = 1
        latitude = 14.594806
        longtitude = 121.171055

    elif getlocation == 'Bulacan, Pampanga Market':
        region_iii = 1
        bulacan = 1
        Pampanga = 1
        latitude = 15.02486
        longtitude = 121.086142

    elif getlocation == 'Laguna, Laguna Market':
        region_iv = 1
        laguna = 1
        Laguna = 1
        latitude = 14.286267
        longtitude = 121.41211

    elif getlocation == 'Cavite, Cavite Market':
        region_iv = 1
        cavite = 1
        Cavite = 1
        latitude = 14.422901
        longtitude = 120.94107

    if veg == 'Garlic':
        Garlic = 1
    elif veg == 'Carrot':
        Carrots = 1
    elif veg == 'Cabbage':
        Cabbage = 1
    elif veg == 'Onion (Red)':
        OnionsR = 1
    elif veg == 'Tomatoes':
        Tomatoes = 1
    elif veg == 'Onions (white)':
        OnionsW = 1
    elif veg == 'Bananas (Latundan)':
        Lantundan = 1
    elif veg == 'Bananas (saba)':
        Saba = 1
    elif veg == 'Beans (green, fresh)':
        GBeans = 1
    elif veg == 'Beans (string)':
        SBeans = 1
    elif veg == 'Bitter melon':
        Bittermelon = 1
    elif veg == 'Bottle gourd':
        Bottlegourd = 1
    elif veg == 'Cabbage (chinese)':
        CabbageC = 1
    elif veg == 'Calamansi':
        Calamansi = 1
    elif veg == 'Choko':
        Choko = 1
    elif veg == 'Eggplants':
        Eggplants = 1
    elif veg == 'Ginger':
        Ginger = 1
    elif veg == 'Papaya':
        Papaya = 1
    elif veg == 'Squashes':
        Squashes = 1
    elif veg == 'Sweet Potato leaves':
        SweetPotatoLeaves = 1
    elif veg == 'Water spinach':
        Waterspinach = 1
    elif veg == 'Bananas (lakatan)':
        Lakatan = 1
    elif veg == 'Mangoes (carabao)':
        MangoesC = 1
    elif veg == 'Mangoes (piko)':
        MangoesP = 1
    elif veg == 'Pineapples':
        Pineapples = 1
    elif veg == 'Mandarins':
        Mandarins = 1
    elif veg == 'Coconuts':
        Coconut = 1


    cav_pred_prices = []
    for i in range(12):
        i = i+1
        if i == 1:
            January = 1                   
            February = 0          
            March = 0                    
            April = 0                    
            May = 0                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        elif i == 2:
            January = 0                   
            February = 1          
            March = 0                    
            April = 0                    
            May = 0                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        elif i == 3:
            January = 0                   
            February = 0          
            March = 1                    
            April = 0                    
            May = 0                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        elif i==4:
            January = 0                   
            February = 0          
            March = 0                    
            April = 1                    
            May = 0                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        elif i == 5:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                    
            May = 1                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0

        elif i == 6:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 1                   
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0

        elif i == 7:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 1                    
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        
        elif i == 8:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 1                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0

        elif i == 9:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 0                 
            September = 1              
            October = 0                    
            November = 0                   
            December = 0

        elif i == 10:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 0                 
            September = 0              
            October = 1                    
            November = 0                   
            December = 0
        
        elif i == 11:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 1                   
            December = 0

        elif i == 12:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 1
       

        cav_int_features = [float(latitude),float(longtitude),int(year),int(Lakatan),int(Lantundan),int(Saba),
                    int(GBeans),int(SBeans),int(Bittermelon),int(Bottlegourd),int(Cabbage),int(CabbageC),int(Calamansi),
                    int(Carrots),int(Choko),int(Coconut),int(Eggplants),int(Garlic),int(Ginger),int(Mandarins),int(MangoesC),
                    int(MangoesP),int(OnionsR),int(OnionsW),int(Papaya),int(Pineapples),int(Squashes),int(SweetPotatoLeaves),
                    int(Tomatoes),int(Waterspinach),int(bulacan),int(cavite),int(laguna),int(metro_manila),int(rizal),int(Bulacan),
                    int(Cavite),int(Laguna),int(Metro_Manila),int(Pampanga),int(Rizal),int(Santa_Cruz),int(January),int(February),
                    int(March),int(April),int(May),int(June),int(July),int(August),int(September),int(October),int(November),
                    int(December),int(ncr),int(region_iii),int(region_iv)]

        #priceforecasting
        cav_final_features = [np.array(cav_int_features)]
        cav_pred_price = model.predict(cav_final_features)
        cav_output = round(cav_pred_price[0],2)

        cav_pred_prices.append(cav_output)
    
    cav_min_val = min(cav_pred_prices)
    cav_max_val = max(cav_pred_prices)

    getlocation = "Laguna, Laguna Market"

    #commodities
    Cabbage = 0             
    Carrots = 0              
    Garlic = 0             
    OnionsR = 0         
    Tomatoes = 0            
    OnionsW = 0          
    Lantundan = 0      
    Saba = 0           
    GBeans = 0    
    SBeans = 0          
    Bittermelon = 0            
    Bottlegourd = 0            
    CabbageC = 0        
    Calamansi = 0            
    Choko = 0           
    Coconut = 0               
    Eggplants = 0             
    Ginger = 0          
    Papaya = 0               
    Squashes = 0              
    SweetPotatoLeaves = 0      
    Waterspinach = 0            
    Lakatan = 0       
    MangoesC = 0       
    MangoesP = 0           
    Pineapples = 0             
    Mandarins = 0

    #market
    Metro_Manila = 0
    Santa_Cruz = 0
    Bulacan = 0
    Pampanga = 0
    Cavite = 0
    Laguna  = 0
    Rizal = 0  

    #grid values
    latitude = 0
    longtitude = 0

    #provinces
    metro_manila = 0
    bulacan = 0
    laguna = 0 
    rizal = 0
    cavite = 0
    
    #region
    ncr = 0
    region_iii = 0
    region_iv = 0

    #month
    January = 0                   
    February = 0          
    March = 0                    
    April = 0                    
    May = 0                        
    June = 0                    
    July = 0                      
    August = 0                 
    September = 0              
    October = 0                    
    November = 0                   
    December = 0


    if getlocation == 'Metropolitan Manila, Metro Manila Market':
        ncr = 1
        metro_manila = 1
        Metro_Manila = 1
        latitude = 14.604167
        longtitude = 120.982222

    elif getlocation == 'Rizal, Santa Cruz Market':
        region_iv = 1
        rizal = 1
        Santa_Cruz = 1
        latitude = 14.6089
        longtitude = 121.1712

    elif getlocation == 'Bulacan, Bulacan Market':
        region_iii = 1
        bulacan = 1
        Bulacan = 1
        latitude = 14.843102
        longtitude = 120.814215

    elif getlocation == 'Rizal, Rizal Market':
        region_iv = 1
        rizal = 1
        Rizal = 1
        latitude = 14.594806
        longtitude = 121.171055

    elif getlocation == 'Bulacan, Pampanga Market':
        region_iii = 1
        bulacan = 1
        Pampanga = 1
        latitude = 15.02486
        longtitude = 121.086142

    elif getlocation == 'Laguna, Laguna Market':
        region_iv = 1
        laguna = 1
        Laguna = 1
        latitude = 14.286267
        longtitude = 121.41211

    elif getlocation == 'Cavite, Cavite Market':
        region_iv = 1
        cavite = 1
        Cavite = 1
        latitude = 14.422901
        longtitude = 120.94107

    if veg == 'Garlic':
        Garlic = 1
    elif veg == 'Carrot':
        Carrots = 1
    elif veg == 'Cabbage':
        Cabbage = 1
    elif veg == 'Onion (Red)':
        OnionsR = 1
    elif veg == 'Tomatoes':
        Tomatoes = 1
    elif veg == 'Onions (white)':
        OnionsW = 1
    elif veg == 'Bananas (Latundan)':
        Lantundan = 1
    elif veg == 'Bananas (saba)':
        Saba = 1
    elif veg == 'Beans (green, fresh)':
        GBeans = 1
    elif veg == 'Beans (string)':
        SBeans = 1
    elif veg == 'Bitter melon':
        Bittermelon = 1
    elif veg == 'Bottle gourd':
        Bottlegourd = 1
    elif veg == 'Cabbage (chinese)':
        CabbageC = 1
    elif veg == 'Calamansi':
        Calamansi = 1
    elif veg == 'Choko':
        Choko = 1
    elif veg == 'Eggplants':
        Eggplants = 1
    elif veg == 'Ginger':
        Ginger = 1
    elif veg == 'Papaya':
        Papaya = 1
    elif veg == 'Squashes':
        Squashes = 1
    elif veg == 'Sweet Potato leaves':
        SweetPotatoLeaves = 1
    elif veg == 'Water spinach':
        Waterspinach = 1
    elif veg == 'Bananas (lakatan)':
        Lakatan = 1
    elif veg == 'Mangoes (carabao)':
        MangoesC = 1
    elif veg == 'Mangoes (piko)':
        MangoesP = 1
    elif veg == 'Pineapples':
        Pineapples = 1
    elif veg == 'Mandarins':
        Mandarins = 1
    elif veg == 'Coconuts':
        Coconut = 1


    lag_pred_prices = []
    for i in range(12):
        i = i+1
        if i == 1:
            January = 1                   
            February = 0          
            March = 0                    
            April = 0                    
            May = 0                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        elif i == 2:
            January = 0                   
            February = 1          
            March = 0                    
            April = 0                    
            May = 0                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        elif i == 3:
            January = 0                   
            February = 0          
            March = 1                    
            April = 0                    
            May = 0                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        elif i==4:
            January = 0                   
            February = 0          
            March = 0                    
            April = 1                    
            May = 0                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        elif i == 5:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                    
            May = 1                        
            June = 0                    
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0

        elif i == 6:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 1                   
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0

        elif i == 7:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 1                    
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0
        
        elif i == 8:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 1                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 0

        elif i == 9:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 0                 
            September = 1              
            October = 0                    
            November = 0                   
            December = 0

        elif i == 10:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 0                 
            September = 0              
            October = 1                    
            November = 0                   
            December = 0
        
        elif i == 11:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 1                   
            December = 0

        elif i == 12:
            January = 0                   
            February = 0          
            March = 0                    
            April = 0                
            May = 0                        
            June = 0                   
            July = 0                      
            August = 0                 
            September = 0              
            October = 0                    
            November = 0                   
            December = 1
       

        lag_int_features = [float(latitude),float(longtitude),int(year),int(Lakatan),int(Lantundan),int(Saba),
                    int(GBeans),int(SBeans),int(Bittermelon),int(Bottlegourd),int(Cabbage),int(CabbageC),int(Calamansi),
                    int(Carrots),int(Choko),int(Coconut),int(Eggplants),int(Garlic),int(Ginger),int(Mandarins),int(MangoesC),
                    int(MangoesP),int(OnionsR),int(OnionsW),int(Papaya),int(Pineapples),int(Squashes),int(SweetPotatoLeaves),
                    int(Tomatoes),int(Waterspinach),int(bulacan),int(cavite),int(laguna),int(metro_manila),int(rizal),int(Bulacan),
                    int(Cavite),int(Laguna),int(Metro_Manila),int(Pampanga),int(Rizal),int(Santa_Cruz),int(January),int(February),
                    int(March),int(April),int(May),int(June),int(July),int(August),int(September),int(October),int(November),
                    int(December),int(ncr),int(region_iii),int(region_iv)]

        #priceforecasting
        lag_final_features = [np.array(lag_int_features)]
        lag_pred_price = model.predict(lag_final_features)
        lag_output = round(lag_pred_price[0],2)

        lag_pred_prices.append(lag_output)
    
    lag_min_val = min(lag_pred_prices)
    lag_max_val = max(lag_pred_prices)

    print(mtr_pred_prices)
    print(bul_pred_prices)
    print(riz_pred_prices)
    print(pam_pred_prices)
    print(cav_pred_prices)
    
    mtr = "{} ~ {}".format(mtr_min_val,mtr_max_val)
    bul = "{} ~ {}".format(bul_min_val,bul_max_val)
    riz = "{} ~ {}".format(riz_min_val,riz_max_val)
    pam = "{} ~ {}".format(pam_min_val,pam_max_val)
    cav = "{} ~ {}".format(cav_min_val,cav_max_val)
    lag = "{} ~ {}".format(lag_min_val,lag_max_val)

    ranges = [mtr,bul,riz,pam,cav,lag]
    market = ["Metro Manila","Bulacan","Rizal","Pampanga","Cavite","Laguna"]
    month = ["Jan","Feb","Mar","Apr","May","June","July","Aug","Sep","Oct","Nov","Dec"]
    # return render_template('year.html',ranges=ranges,veg=veg,market=market,lag_min_val=lag_min_val, lag_max_val=lag_max_val, 
    # lag_data=lag_pred_prices,cav_min_val=cav_min_val, cav_max_val=cav_max_val, cav_data=cav_pred_prices,pam_min_val=pam_min_val, 
    # pam_max_val=pam_max_val, pam_data=pam_pred_prices,riz_min_val=riz_min_val, riz_max_val=riz_max_val,riz_data=riz_pred_prices,
    # bul_min_val=bul_min_val, bul_max_val=bul_max_val, bul_data=bul_pred_prices,mtr_min_val=mtr_min_val, mtr_max_val=mtr_max_val, 
    # mtr_data=mtr_pred_prices,year=year,month=month)
    
    mtr_ave = statistics.mean(mtr_pred_prices)
    pam_ave = statistics.mean(pam_pred_prices)
    riz_ave = statistics.mean(riz_pred_prices)
    lag_ave = statistics.mean(lag_pred_prices)
    cav_ave = statistics.mean(cav_pred_prices)
    bul_ave = statistics.mean(bul_pred_prices)
    
    
    market_arr = [mtr_ave, pam_ave, lag_ave, cav_ave, bul_ave, riz_ave]
    market_name_arr = ['Metro Manila', 'Pampanga', 'Laguna', 'Cavite', 'Bulacan', 'Rizal']
    best_ave = min(market_arr)
    
    for i in range(6):
        if market_arr[i] == best_ave:
            best_market = market_name_arr[i]
    
    
    pred_prices_data = mtr_pred_prices+pam_pred_prices+riz_pred_prices+lag_pred_prices+cav_pred_prices+cav_pred_prices+bul_pred_prices
    min_pred_price = min(pred_prices_data)
    max_pred_price = max(pred_prices_data)
    prices_ave = statistics.mean(pred_prices_data)
    return jsonify({
        'mtr_data': mtr_pred_prices,
        'mtr_min': mtr_min_val,
        'mtr_max': mtr_max_val,
        'mtr_ave': mtr_ave,
        'pam_data': pam_pred_prices,
        'pam_min': pam_min_val,
        'pam_max': pam_max_val,
        'pam_ave': pam_ave,
        'riz_data': riz_pred_prices,
        'riz_min': riz_min_val,
        'riz_max': riz_max_val,
        'riz_ave': riz_ave,
        'cav_data': cav_pred_prices,
        'cav_min': cav_min_val,
        'cav_max': cav_max_val,
        'cav_ave': cav_ave,
        'lag_data': lag_pred_prices,
        'lag_min': lag_min_val,
        'lag_max': lag_max_val,
        'lag_ave': lag_ave,
        'bul_data': bul_pred_prices,
        'bul_min': bul_min_val,
        'bul_max': bul_max_val,
        'bul_ave': bul_ave,
        'min_pred_price': min_pred_price,
        'max_pred_price': max_pred_price,
        'prices_ave': prices_ave,
        'best_ave': best_ave,
        'best_market': best_market
    })
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()