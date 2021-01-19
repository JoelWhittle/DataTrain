import csv, io
import uuid
from django.contrib import messages
import keras
import random
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.utils import np_utils
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from .models import Orders
from django.http import StreamingHttpResponse
from sklearn.preprocessing import StandardScaler
import pandas as pd
from django.urls import reverse
import stripe
from django.shortcuts import redirect


class NGram:
	def __init__(self):
		self.name = ""
		self.children = []

	def f(self):
		return 'hello world'


def customerjourneyupload(request):
	context = {
		'posts' : Post.objects.all(),
	
		'stripe_public_key' : ''
	}

	if request.method == "POST":


		session__id = request.GET.get('session_id')

		myfile = request.FILES['file']

		file_data = myfile.read().decode("utf-8")


		lines = file_data.split('/n')
		
		ngrams = []
		for line in lines:
			splitLine = line.split(',')

			for i in range(0,len(splitLine)):
				metric = splitLine[i]
				foundMatch = False
				for ng in ngrams:
					if foundMatch == False:
						if ng.name == metric:
							foundMatch = True

							if(i < len(splitLine) -1):
								nameOfTargetGram = splitLine[i + 1]
								foundTargetMatch = False
								for tg in ngrams:
									if tg.name == nameOfTargetGram:
										foundTargetMatch = True
										ng.children.append(tg)
								if foundTargetMatch == False:
									newTG = NGram()
									newTG.name = nameOfTargetGram
									ng.children.append(newTG)
									ngrams.append(newTG)		

				if foundMatch == False:
					ng = NGram()
					ng.name = metric
					ngrams.append(ng)			

					if(i < len(splitLine) -1):
								nameOfTargetGram = splitLine[i + 1]
								foundTargetMatch = False
								for tg in ngrams:
									if tg.name == nameOfTargetGram:
										foundTargetMatch = True
										ng.children.append(tg)
								if foundTargetMatch == False:
									newTG = NGram()
									newTG.name = nameOfTargetGram
									ng.children.append(newTG)
									ngrams.append(newTG)

		for gram in ngrams:
			print(gram.name)




	return render(request, 'landing/customerjourneyupload.html', context)


def upload(request):
	context = {
		'posts' : Post.objects.all(),
	
		'stripe_public_key' : ''
	}

	session__id = request.GET.get('session_id')

	if session__id is None:
		 return redirect('/')

	payment = Orders.objects.filter(paymentCode=session__id, completed = True)
	
	if len(payment) > 0:
		  	return redirect('/')



	if request.method == "POST":


		session__id = request.GET.get('session_id')

#check database

	

#run data shiz

		myfile = request.FILES['file']

		df = pd.read_csv(myfile)
		feats = []
		
		
		print (df.dtypes)
		dataTypeDict = dict(df.dtypes)
		for (columnName, columnData) in df.iteritems():
			if df.dtypes[columnName] == np.object:
				feats.append(columnName)
			print('Colunm Name : ', columnName)
			print('Column Contents : ', columnData.values)

		variableToTrainFor = request.POST.get('colName')
		df_final = pd.get_dummies(df,columns=feats,drop_first=True)
		X = df_final.drop([variableToTrainFor],axis=1).values
		y = df_final[variableToTrainFor].values
		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
		sc = StandardScaler()
		X_train = sc.fit_transform(X_train)
		X_test = sc.transform(X_test)
		
	

		response = HttpResponse(content_type="text/csv")
		fileName = myfile.name + 'Scored'
		responseArg = 'attachment; filename="' + fileName + '".csv' 
		response['Content-Disposition'] = responseArg
		writer = csv.writer(response)
	
		#for x in range(0, len(lines)):
			#n = lines[x].split(",")
			#writer.writerow(n)
		def baseline_model():
			inputCount = ((len(df_final.columns) -1))
			model = Sequential()
			model.add(Dense((int)(inputCount / 2), kernel_initializer = "uniform", input_dim= inputCount, activation='relu'))
			model.add(Dense(1, kernel_initializer = "uniform", activation='sigmoid'))
			model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
			return model
		model = baseline_model()
		model.fit(X_train, y_train, epochs=500, batch_size=200, verbose=2)


		predictionOnX = sc.fit_transform(X)
		prediction = model.predict(predictionOnX)
		

		df['Score'] = prediction
		writer.writerow(df)
		for index, row in df.iterrows():
			#print(index, row)
			writer.writerow(row)


#Update database

		Orders.objects.filter(paymentCode=session__id, completed = False).update(completed = True)


		#print(prediction)
		return response
		return render(request, 'landing/landing.html', context)



# Get area

	
#check paymanet
	stripe.api_key = 'sk_test_51HH6Y4LlQYLbPvG7f4ZkVRVoxDW2yEGKfjBol0uX17ykmVI454tsn1EmdgHXHfF0RxtU4t9GxEF80D2oNJeNQvR400rDQu0hK9'

	try:
		CheckPayment = stripe.checkout.Session.retrieve(session__id)
		print('<-------------------------------------------------------------------------------------------------------------------->')
		print('payment check success')
	except:
		return redirect('/')

	if CheckPayment is None:
		return redirect('/')
	print(CheckPayment)

#add to database 
  
	payment = Orders.objects.filter(paymentCode=session__id)

	if len(payment) == 0:
		newPayment = Orders.objects.create(paymentCode=session__id, completed = False)
		Orders.save(newPayment)

	return render(request, 'landing/upload.html', context)


def landing(request):

	context = {
		'posts' : Post.objects.all(),
		
		'stripe_public_key' : ''
	}



	stripe.api_key = 'sk_test_51HH6Y4LlQYLbPvG7f4ZkVRVoxDW2yEGKfjBol0uX17ykmVI454tsn1EmdgHXHfF0RxtU4t9GxEF80D2oNJeNQvR400rDQu0hK9'

	
	print('dafuq')	
	session = stripe.checkout.Session.create(
  			payment_method_types=['card'],
  			line_items=[{
    			'price' : 'price_1HH6a7LlQYLbPvG7BEI2dLNE',
    			'quantity': 1,
  			}],
  			mode='payment',
  			success_url=request.build_absolute_uri(reverse('upload')) + '?session_id={CHECKOUT_SESSION_ID}',
  			cancel_url=request.build_absolute_uri(reverse('landing')),
	)
	

	context = {
		'posts' : Post.objects.all(),
		'session_id' : session.id,
		'stripe_public_key' : 'pk_test_51HH6Y4LlQYLbPvG7XpLwRwUE1GRKnjpIqvCouuKb6pWCxdbZawF8Mbj6oATIeKlhosGg1NasvOOzzYbtJg4VW9ct00x82f56S7'
	}
	return render(request, 'landing/landing.html', context)






