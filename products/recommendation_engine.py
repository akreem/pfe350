# app/recommendation_engine.py
import pandas as pd
from surprise import Dataset, Reader, SVD
from products.models import  Product
from orders.models import OrderDetails


def get_recommendations_for_user(user_id, top_n=5):
    # Get user-product interactions from orders
    if not user_id:
        return Product.objects.order_by('?')[:5]  # 👈 Random fallback
    rows = []
    for detail in OrderDetails.objects.select_related('order', 'product'):
        if detail.order.user_id and detail.product_id:
            rows.append((detail.order.user_id, detail.product_id, 1))  # Implicit rating

    if not rows:
        return Product.objects.none()

    df = pd.DataFrame(rows, columns=["user_id", "product_id", "rating"])
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df, reader)
    trainset = data.build_full_trainset()

    model = SVD()
    model.fit(trainset)

    all_products = Product.objects.all()
    predictions = []

    for product in all_products:
        pred = model.predict(user_id, product.id)
        predictions.append((product, pred.est))

    # Sort and return top N
    recommendations = sorted(predictions, key=lambda x: x[1], reverse=True)
    return [prod for prod, _ in recommendations[:top_n]]
