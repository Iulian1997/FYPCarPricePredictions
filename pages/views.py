from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

# Imports for ML
import pandas as pd
#import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OrdinalEncoder
from sklearn import metrics
import pickle
import json

def index(request):

    carDataset = pd.read_csv(r"C:\Users\Julian\Documents\4th Year\FYP\Dataset\CarDatasetRanUpdated.csv")
    make = sorted(carDataset['make'].unique())
    model = sorted(carDataset['model'].unique())
    transmission = sorted(carDataset['transmission'].unique())
    tax = sorted(carDataset['tax'].unique())
    
    context = {
        'make':make,
        'model':model,
        'model2': json.dumps(model),
        'transmission':transmission,
        'tax':tax,
    }

    return render(request, 'pages/index.html', context)

def about(request):
    return render(request, 'pages/about.html')

def prediction(request):

    if request.method == 'POST':
        # GET FORM VALUES
        make = request.POST['make']
        model = request.POST['car_model']
        year = request.POST['year'] 
        transmission = request.POST['transmission']
        if request.POST["mileage"] == "":
            mileage = "default"
        else:
            mileage = request.POST['mileage']
        tax = request.POST['tax']
        if request.POST["mpg"] == "":
            mpg = "default"
        else:
            mpg = request.POST['mpg']
        if request.POST["engine_size"] == "":
            engine_size = "default"
        else:
            engine_size = request.POST['engine_size']

        if request.POST["make"] == "" or request.POST["year"] == "" or request.POST['car_model'] == "":
            messages.error(request, 'Please enter Make, Model and Year!')
            return redirect("index")
        else:
            # Data for Bar Chart
            list_prices = []

            # Data for Grouped Bar Chart
            list_price_man = []
            list_price_auto = []

            # Read dataset
            carData = pd.read_csv(r"C:\Users\Julian\Documents\4th Year\FYP\Dataset\CarDatasetRanUpdated.csv")

            # Range of year
            year_range = carData.loc[carData["model"]  == model, "year"].unique()
            year_range.sort()
            year_range_values = []

            # CSV filter query
            filter_query = carData[(carData["make"]==make) & (carData["model"]==model) & (carData["year"]==year)]
            filter_query_no_year = carData[(carData["make"]==make) & (carData["model"]==model)]

            # Most popular transmission
            try:
                pop_transmission = filter_query
                pop_transmission = pop_transmission['transmission'].value_counts().idxmax()
                print(pop_transmission)
            except ValueError:
                pop_transmission = filter_query_no_year
                pop_transmission = pop_transmission['transmission'].value_counts().idxmax()
                print(pop_transmission)

            # Average mileage
            avg_mileage = filter_query
            avg_mileage = avg_mileage['mileage'].mean()
            #avg_mileage = int(avg_mileage)
            if(pd.isna(avg_mileage)):
                avg_mileage = filter_query_no_year
                avg_mileage = avg_mileage['mileage'].mean()
                avg_mileage = int(avg_mileage)
                print(avg_mileage)

            # Most popular tax bracket
            try:
                pop_tax = filter_query
                pop_tax = pop_tax['tax'].value_counts().idxmax()
                pop_tax = int(pop_tax)
                print(pop_tax)
            except ValueError:
                pop_tax = filter_query_no_year
                pop_tax = pop_tax['tax'].value_counts().idxmax()
                print(pop_tax)

            # Average MPG
            avg_mpg = filter_query
            avg_mpg = avg_mpg['mpg'].mean()
            #avg_mpg = int(avg_mpg)
            if(pd.isna(avg_mpg)):
                avg_mpg = filter_query_no_year
                avg_mpg = avg_mpg['mpg'].mean()
                avg_mpg = int(avg_mpg)
                print(avg_mpg)

            # Most popular Engine Size
            try:
                pop_engine_size = filter_query
                pop_engine_size = pop_engine_size['engineSize'].value_counts().idxmax()
                print(pop_engine_size)
            except ValueError:
                pop_engine_size = filter_query_no_year
                pop_engine_size = pop_engine_size['engineSize'].value_counts().idxmax()
                print(pop_engine_size)

            if transmission == "default":
                transmission = pop_transmission

            if mileage == "default":
                mileage = avg_mileage
                print(mileage)

            if tax == "default":
                tax = pop_tax

            if mpg == "default":
                mpg = avg_mpg

            if engine_size == "default":
                engine_size = pop_engine_size
            
            mlModelRF = pickle.load(open(r"C:\Users\Julian\Documents\4th Year\FYP\Model\CarPricePredictionModelRandomForest.pkl", "rb"))
            prediction = mlModelRF.predict(pd.DataFrame([[make, model, year, transmission, float(mileage), float(tax), float(mpg), float(engine_size)]], 
            columns=['make', 'model', 'year', 'transmission', 'mileage', 'tax', 'mpg', 'engineSize']))

            for n in year_range:
                x = mlModelRF.predict(pd.DataFrame([[make, model, n, transmission, mileage, tax, mpg, engine_size]], columns=['make', 'model', 'year', 'transmission', 'mileage', 'tax', 'mpg', 'engineSize']))
                xMan = mlModelRF.predict(pd.DataFrame([[make, model, n, "Manual", mileage, tax, mpg, engine_size]], columns=['make', 'model', 'year', 'transmission', 'mileage', 'tax', 'mpg', 'engineSize']))
                xAuto = mlModelRF.predict(pd.DataFrame([[make, model, n, "Automatic", mileage, tax, mpg, engine_size]], columns=['make', 'model', 'year', 'transmission', 'mileage', 'tax', 'mpg', 'engineSize']))
                if(x[0] >= 500 and xMan[0] >= 500):
                    list_prices.append(x[0])
                    list_price_man.append(xMan[0])
                    list_price_auto.append(xAuto[0])
                    year_range_values.append(int(n))

            price = prediction[0]
            price = round(price, 2)

            eurPrice = round(price * 1.15, 2)

            context = {
                'make':make,
                'model':model,
                'year':int(year),
                'transmission':transmission,
                'mileage':mileage,
                'tax':tax,
                'mpg':mpg,
                'engine_size':engine_size,
                'price':price,
                'eurPrice': eurPrice,
                'list_prices': json.dumps(list_prices),
                'year_range': json.dumps(year_range_values),
                'list_price_man': json.dumps(list_price_man),
                'list_pice_auto': json.dumps(list_price_auto),
            }

            if(prediction <= 500):
                messages.error(request, 'Please check input parameters and trying again!')
                return redirect('index')
            else:
                return render(request, 'pages/prediction.html', context)
    else:
        return redirect('index')

    