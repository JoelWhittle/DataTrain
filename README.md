# DataTrain
A SaaS machine learning learning website, utilising Django, Tensorflow and the Stripe API to receive payments.

Once a customer pays using the stripe API, they are able to upload a CSV file. After specifying a column to predict for, this algorithm will sanitise the users data, including quantifying any qualititive data provided, before running regression classificaton to predict
the category of an item.

This technology may be used to score sales leads or evaluate staff-customer retention, amongst many other uses.

I have since decided to implement this technology inside a larger package, perhaps an ecommerce store or CRM.
